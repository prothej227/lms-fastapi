import json
import os
from app.core.config import get_settings
from app.core import state


def load_reference_mappings_config(
    file_path=get_settings().ref_value_mappings_path,
) -> dict:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Reference mappings file not found: {file_path}")

    if os.path.getsize(file_path) == 0:
        raise ValueError(f"Reference mappings file is empty: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in {file_path}: {e}")


def get_raw_ref_mappings(category: str) -> dict | None:
    return getattr(state.ReferenceValueMappings, category, None)


def get_ref_mappings(category: str) -> list[dict]:
    mappings = getattr(state.ReferenceValueMappings, category, {})
    return [{"label": label, "value": key} for key, label in mappings.items()]
