"""Prompts for data generation
"""

cooperation_es = """
Write a story of less than 250 words in Spanish using only words that a 3-4 year old would likely understand.
The story needs to follow a structure of a fable if possible. Remember to only use simple words! And never use emojis

Include the next verb : {verb}, noun: {noun} and adjective: {adjective}

You can conjugate the verb in different times to make the stories more diverse.

You must follow the next setup to create the story:

Context of the place: {place}

<setup>
{story_setup}
</setup>

The setup includes subjects A and B, you can select whatever subjects you want to replace generic A and B.
"""

cooperation_en = """
Write a story of less than 250 words in English using only words that a 3-4 year old would likely understand.
The story needs to follow a structure of a fable if possible. Remember to only use simple words! And never use emojis

Include the next verb : {verb}, noun: {noun} and adjective: {adjective}

You can conjugate the verb in different times to make the stories more diverse.

You must follow the next setup to create the story:

Context of the place: {place}

<setup>
{story_setup}
</setup>

The setup includes subjects A and B, you can select whatever subjects you want to replace generic A and B.
"""

general_es = """
Write a story of less than 250 words in Spanish using only words that a 3-4 year old would likely understand.
Remember to only use simple words! And never use emojis

Include the next verb : {verb}, noun: {noun} and adjective: {adjective}

You can conjugate the verb in different times to make the stories more diverse.

You must follow the next setup to create the story:

Context of the place: {place}

<setup>
{story_setup}
</setup>
"""

prompts = {
    "cooperation-es" : cooperation_es,
    "cooperation-en" : cooperation_en,
    "general-es" : general_es,
}
