"""This module contains the definition of the script to generate the synthetic data for Alexandria
"""

from src.setups import all_setups
from src.prompts import prompts
import json
import random
from tqdm import tqdm
from src.utils import ConfigManager

config = ConfigManager("config.yaml").config

total_stories = config["generation"]["total_stories"]
vocabulary_path = config["data"]["vocabulary"]
output_path = config["data"]["prompt_templates"]
generation_prompt = prompts[config["generation"]["prompt"]]
stories = []

with open(vocabulary_path, "r") as file:
    vocabulary = json.load(file)

verbs = vocabulary["verbs"]
nouns = vocabulary["nouns"]
adjectives = vocabulary["adjectives"]
places = vocabulary["places"]
features = vocabulary["features"]

if config["generation"]["story_setups"][0] == "all":
    story_setups = list(all_setups.values())
else:
    story_setups = [all_setups[setup] for setup in config["generation"]["story_setups"]]

for i in tqdm(range(total_stories)):
    verb = verbs[random.randint(0,len(verbs)-1)]
    noun = nouns[random.randint(0,len(nouns)-1)]
    adjective = adjectives[random.randint(0,len(adjectives)-1)]
    story_setup = story_setups[random.randint(0,len(story_setups)-1)]
    place = places[random.randint(0,len(places)-1)]

    if config["generation"]["story_setups"][0] == "basic_setup":
        feature = [f for f in features if random.randint(0,1) == 1]
        if not feature:
            feature = features[random.randint(0,len(features)-1)]
        prompt = generation_prompt.format(
            verb=verb,
            noun=noun,
            adjective=adjective,
            place=place,
            story_setup=story_setup.format(features=str(feature)),
        )
    else:
        prompt = generation_prompt.format(
            verb=verb,
            noun=noun,
            adjective=adjective,
            place=place,
            story_setup=story_setup,
        )

    input = {
        "template" : prompt.strip(),
        "verb" : verb,
        "noun" : noun,
        "adjective" : adjective,
        "setup" : story_setup
    }

    stories.append(input)

with open(output_path, 'w') as outfile:
    for entry in stories:
        json.dump(entry, outfile)
        outfile.write('\n')
