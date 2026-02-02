from src.clients import ClientFactory
from src.utils import ConfigManager
import json

cm = ConfigManager('config.yaml')

client = ClientFactory().get_client(
    provider=cm.config['models']['generator_provider'],
    config=cm.config
)

input_prompts = []
with open(cm.config['data']["prompt_templates"], 'r', encoding='utf-8') as f:
    for line in f:
        try:
            input_prompts.append(json.loads(line)["template"])
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON on line: {e}")
            continue

batch_status = client.batch_generate(input_prompts, file=True)

print(batch_status)

MESSAGE_BATCH_ID = batch_status.id

client.check_batch_execution(MESSAGE_BATCH_ID)

results = client.get_batch_results(MESSAGE_BATCH_ID)

print('Outputs written in ', cm.config['data']["output"])
