# tiny-stories-generator

A tool to generate a synthetic data based on the structured presented in TinyStories (Eldan & Li, 2023), with some tweaks to make it generalizable to other formats. 

Currently compatible with Mistral and Claude batch APIs.

tiny-stories-generator has been implemented with extensibility in mind. At the moment, the main goal is to integrate with the batch APIs from different providers, as often synthetic data generation is not a task that requires low latency and usually needs large volumes of results. Using batch APIs is the best way to retrieve this while cutting costs for your data generation task.

## Quickstart

This project uses uv to manage dependencies.

```bash
uv sync
uv pip install -e .
```

### Integrations

Currently supports connection with batch APIs from **Mistral** with the official library at version 1.11.1 and also **Claude** client at version 0.76.0

## Design

This tool has implemented different functionality that might be useful to generate synthetic data at different stages. You can run only the one that is relevant for your task at a given time. 

The components available in the generator are:

1. A prompt generator, that fills up templates to instruct a given model on which story to create.
2. A data generator, that triggers the call on compatible batch APIs from a selected provider to generate the data with the prompts from step 1.
3. A dataset evaluator. Based on LLM-as-a-judge methodology, but extensible to custom metrics, implemented using mlflow.
4. An additional results downloader. In general, once a batch is ready the code in step 2 would be able to retrieve it, but you can still perform as many downloads you want with this specific script.

## The configuration file

The preferences for each component can be customized directly in the config.yaml file, it is divided in sections and everything is adequately commented for easy onboarding.

```yaml
# Section to configure all the models and providers for generation
models:
  generator_provider : mistral # The main provider to use to generate the data
  default_models: # Models called for generation. Dependent on generator_provider value. E.g: provider 'mistral' will use generator_mistral model
    generator_anthropic : claude-haiku-4-5-20251001
    generator_mistral : mistral-small-2506

# Options to control data generation
generation:
  max_len : 300 # Max tokens used for output
  total_stories : 10000 # Max stories to produce in total
  batch_size : 10000 # Size of the batch
  prompt: general-es # Name of the prompt used to generate synthetic data. As in src/prompts.py
  story_setups: # Indicates which setups to use for the stories. As in src/setups.py. If 'all' it will use all in src/setups.py
    - basic_setup

# Options to control evaluation
evaluation:
  judge_model : anthropic:/claude-sonnet-4-5 # Model used as LLM-as-a-judge for data evaluation
  run_name : mistral_evaluation # Name of the run name for mlflow
  metrics: # Indicates the metrics to use to evaluate the data. As in src/metrics.py. If 'all' it will use all in src/metrics.py
  - is_gramatically_correct
  - is_understandable

# Indicates the files required for the different scripts
data:
  vocabulary: data/vocabulary.json # File with verbs, nouns and adjectives to use to forest diversification
  prompt_templates : data/templates_base.jsonl # The file where the input prompts will be stored for posterior generation. Used in generate_prompts.py
  output: data/stories_mistral_v2_base.jsonl # File where synthetic data will be stored. Used by main.py
  batch_input: data/batch_input_base.jsonl # File where batch data will be held prior to generation. Currently supported only for Mistral format. Used in clients.py


```

## Prepare input prompts

### Define your vocabulary 

Generating prompts requires a definition of a vocabulary. In general, you can create any vocabulary you want in a json file to indicate the words you want to use. 

As an example in this repo, you'll find a json file with words for allowed verbs, nouns, adjectives and places where stories could occur.

### Define the prompt template to use as basis for your data

This vocabulary file will be used to fill up templates of a prompt you define at **src/prompts.py** at random selection. 

In general, you can use any prompt pattern you want, and after that you must register it into the **prompts** dictionary located at the end of that file.

To indicate which prompt you want to use for the generation of your data change the **prompt** value in the **generation** section of the config file. Use the name used in the registration section of src/prompts.py

Custom setups to guide the narratives can also be defined in the **src/setups.py** file and referenced in the config file after register them.

```bash
uv run src/generate_prompts.py
```

Running this command will save a file in the path indicated at **prompt_templates** section in tha config file. Each line represents a different version of the prompt filled up with the vocabulary data.

## Generate your data

The **main.py** file triggers a call to the batch API of the provider indicated in the **generator_provider** section in the configuration. Using the model listed given the provider.

It actually uses the official client, prepares the input from the prompts generated in the previous step, uploads it and triggers a batch run. The client keeps the connection open to download the results once the batch is finished.

However, you can retrieve results later with the **src/get_results.py** file.

```bash
uv run main.py
```

## Evaluate your synthetic data

For evaluation, mlflow is used to log everything to your local machine. In general, tiny-stories-generator comes with a LLM-as-a-judge approach but you can extend to any other custom metrics required to evaluate the quality of the synthetic data.

You can define the metrics you want to use in the **src/metrics.py**. The implementation follows the [mlflow evaluate](https://mlflow.org/docs/latest/genai/eval-monitor/quickstart/) way of working.

Once you have implemented your custom metric, register it in the scorers dict in the same file. Then it can be referenced in the **evaluation/metrics** section in the configuration file.

The model used as a judge during evaluation can also be defined in the **evaluation/judge_model** section in config.

```bash
uv run src/evaluate.py
```