"""This module contains the definition of the script to generate the synthetic data for Alexandria
"""

from anthropic import Anthropic
from groq import Groq
from mistralai import Mistral
from dotenv import load_dotenv
import os
from data_generation_config import setups
import json
import random
import mlflow
from tqdm import tqdm

load_dotenv()

client_claude = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
client_llama = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
client_mistral = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))

# Prepare batch : 100 stories

total_stories = 100
stories = []

with open("data/vocabulary.json", "r") as file:
    vocabulary = json.load(file)

verbs = vocabulary["verbs"]
nouns = vocabulary["nouns"]
adjectives = vocabulary["adjectives"]
places = vocabulary["places"]
story_setups = [
    setups.altruism,
    setups.communication_coordination,
    setups.complementary_skills,
    setups.conflict_resolution,
    setups.failed_cooperation_adjustment,
    setups.fair_competition,
    setups.joint_problem_solving,
    setups.resource_sharing,
    setups.tradeoffs_and_exchange,
    setups.non_cooperative_agent,
    setups.turn_taking,
    setups.win_lose_inevitable
]

for i in tqdm(range(total_stories)):
    verb = verbs[random.randint(0,len(verbs)-1)]
    noun = nouns[random.randint(0,len(nouns)-1)]
    adjective = adjectives[random.randint(0,len(adjectives)-1)]
    story_setup = story_setups[random.randint(0,len(story_setups)-1)]
    place = places[random.randint(0,len(places)-1)]

    generation_prompt = f"""
    Write a story of less than 250 words in Spanish using only words that a 3-4 year old would likely understand.
    The story needs to follow a structure of a fable if possible. Remember to only use simple words! And never use emojis

    Include the next verb : {verb}, noun: {noun} and adjective: {adjective}

    You can conjugate the verb in different times to make the stories more diverse.

    You must follow the next setup to create the story:

    Context of the place: {place}

    {story_setup}

    The setup includes subjects A and B, you can select whatever subjects you want to replace generic A and B.
    """

    prompt = generation_prompt.format(
        verb=verb,
        noun=noun,
        adjective=adjective,
        place=place,
        story_setup=story_setup,
    )

    stories.append(prompt)

with open("data/stories.json", "w") as file:
    json.dump(stories, file, indent=4)

mlflow.set_experiment("Story Generation Mistral")

def generator(input : str) -> str:
    chat_response = client_mistral.chat.complete(
        model = "mistral-small-latest",
        messages = [
                {
                    "role": "user",
                    "content": input,
                },
            ]
    )
    return chat_response.choices[0].message.content

def qa_predict_fn(input: str) -> str:
    """Wrapper function for evaluation using ``my_agent``."""
    return generator(input)

eval_dataset = [
]

"""
chat_completion = client_llama.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="meta-llama/llama-4-scout-17b-16e-instruct",
)

print(chat_completion.choices[0].message.content)
"""
# Probemos las historias pequeñas sin batch y luego preparemos todo para tener los batches y abaratar mas el costo