"""Custom metrics for the LLM as a judge evaluation approach
"""

from mlflow.genai import make_judge
import yaml

with open('syntetic_data_config.yaml', 'r', encoding='utf8') as f:
    config = yaml.safe_load(f)

judge_model = config["judge_model"]

is_gramatically_correct = make_judge(
    
)
