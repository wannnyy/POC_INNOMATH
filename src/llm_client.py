import json
from openai import OpenAI
from .config import settings
from .prompt import SYSTEM_INSTRUCTIONS_TH, build_user_prompt

client = OpenAI(api_key=settings.openai_api_key)

def generate_parent_report_json(input_payload: dict) -> dict:
    resp = client.responses.create(
        model=settings.openai_model,
        reasoning={"effort": "low"},
        instructions=SYSTEM_INSTRUCTIONS_TH,
        input=build_user_prompt(input_payload)
    )

    # The SDK aggregates all text outputs here
    raw_text = resp.output_text.strip()

    # Defensive JSON extraction (in case model adds whitespace)
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            "LLM did not return valid JSON. Raw output:\n"
            + raw_text
        ) from e
