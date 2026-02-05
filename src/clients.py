"""Classes to implement the batch generation of the dataset
"""

from anthropic import Anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

from mistralai import Mistral
from dotenv import load_dotenv
from abc import ABC, abstractmethod
import os
from typing import List, Dict
from tqdm import tqdm
import json
import time
from src.utils import write_jsonl

load_dotenv()

class BaseClient(ABC):

    def __init__(self, client, config):
        self.client = client
        self.config = config

    @abstractmethod
    def batch_generate(self, input_prompts : List[str], **kwargs):
        pass

    @abstractmethod
    def get_batch_status(self, batch_id : str) -> Dict:
        pass

    @abstractmethod
    def get_batch_results(self, *args, **kwargs) -> Dict:
        pass

    @abstractmethod
    def dump_stories(self, results : List[str]) -> None:
        pass

    @abstractmethod
    def check_batch_execution(self):
        pass

class AnthropicClient(BaseClient):

    def __init__(self, client : Anthropic | Mistral, config : Dict):
        super().__init__(client, config)

    def dump_stories(self, results : List[str]):
        with open(self.config['data']['output'], 'w') as outfile:
            for entry in results:
                e = {
                    'custom_id' : entry.custom_id,
                    'message_id' : entry.result.message.id,
                    'text' : entry.result.message.content[0].text
                }
                json.dump(e, outfile)
                outfile.write('\n')

    def batch_generate(self, input_prompts : List[str], **kwargs):
        message_batch = self.client.messages.batches.create(
            requests=[
                Request(
                    custom_id=str(id),
                    params=MessageCreateParamsNonStreaming(
                        model=self.config["models"]["default_models"]["generator_anthropic"],
                        max_tokens=self.config["generation"]["max_len"],
                        messages=[{
                            "role": "user",
                            "content": input,
                        }]
                    )
                ) for id, input in enumerate(input_prompts)
            ]
        )
        return message_batch

    def get_batch_status(self, batch_id : str) -> Dict:
        message_batch = self.client.messages.batches.retrieve(
            batch_id
        )
        return message_batch

    def get_batch_results(self, batch_id : str):
        succesful_results = []
        for result in tqdm(self.client.messages.batches.results(
            batch_id,
        )):
            match result.result.type:
                case "succeeded":
                    succesful_results.append(result)
                case "errored":
                    if result.result.error.type == "invalid_request":
                        print(f"Validation error {result.custom_id}")
                    else:
                        print(f"Server error {result.custom_id}")
                case "expired":
                    print(f"Request expired {result.custom_id}")
            self.dump_stories(succesful_results)
        return succesful_results

    def check_batch_execution(self, batch_id : str):
        while True:
            message_batch = self.get_batch_status(batch_id)
            if message_batch.processing_status == "ended":
                break
            print(f"Batch {batch_id} is still processing...")
            time.sleep(60)
    
class MistralClient(BaseClient):

    def __init__(self, client, config):
        super().__init__(client, config)

    def dump_stories(self, results):
        final_data = [{
            "id" : result["custom_id"],
            "text" : result["response"]["body"]["choices"][0]["message"]["content"],
            "model" : result["response"]["body"]["model"],
            "prompt_tokens" : result["response"]["body"]["usage"]["prompt_tokens"],
            "output_tokens" : result["response"]["body"]["usage"]["completion_tokens"],
            "total_tokens" : result["response"]["body"]["usage"]["total_tokens"],
        } for result in results]
        write_jsonl(final_data, self.config["data"]["output"])
            #f.write(results.read())

    def batch_generate(self, input_prompts, file : bool = False, **kwargs):
        batch_data = [
            {
                "custom_id": str(id), 
                "body": {
                    "max_tokens": self.config["generation"]["max_len"], 
                    "messages": [{"role": "user", "content": input}]
                }
            } for id,input in enumerate(input_prompts)
        ]
        if file:
            write_jsonl(batch_data, self.config["data"]["batch_input"])
            batch_data = self.send_file(self.config["data"]["batch_input"])

        if not file:
            message_batch = self.client.batch.jobs.create(
                requests=batch_data,
                model=self.config["models"]["default_models"]["generator_mistral"],
                endpoint="/v1/chat/completions",
            )
        else:
            message_batch = self.client.batch.jobs.create(
                input_files=[batch_data.id],
                model=self.config["models"]["default_models"]["generator_mistral"],
                endpoint="/v1/chat/completions",
            )
        return message_batch
    
    def get_batch_status(self, batch_id : str) -> Dict:
        message_batch = self.client.batch.jobs.get(job_id=batch_id)
        return message_batch
    
    def get_batch_results(self, batch_id : Dict):
        results = self.check_batch_execution(batch_id)
        output_file_stream = self.client.files.download(file_id=results.output_file)
        self.dump_stories(output_file_stream)
        return output_file_stream
    
    def check_batch_execution(self, batch_id : str):
        while True:
            message_batch = self.get_batch_status(batch_id)
            if message_batch.status == "SUCCESS":
                break
            print(f"Batch {batch_id} is still processing...")
            time.sleep(60)
        return message_batch
    
    def send_file(self, filename : str):
        batch_data = self.client.files.upload(
            file={
                "file_name": filename,
                "content": open(filename, "rb")
            },
            purpose = "batch"
        )
        return batch_data

class ClientFactory():

    @staticmethod
    def get_client(provider : str, config : Dict):
        if provider == "anthropic":
            client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
            return AnthropicClient(client, config)
        elif provider == "mistral":
            client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))
            return MistralClient(client, config)
        else:
            raise ValueError('Invalid provider')