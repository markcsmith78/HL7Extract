import json
from pathlib import Path
from jsonschema import Draft202012Validator

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"{path}: invalid JSON at line {e.lineno}, column {e.colno}: {e.msg}")
    except OSError as e:
        raise ValueError(f"{path}: could not read file: {e}")


def validate_schema(config, schema):
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(config), key=lambda e: e.path)

    if errors:
        messages = []
        for error in errors:
            location = ".".join(str(p) for p in error.path) or "<root>"
            messages.append(f"{location}: {error.message}")
        raise ValueError("Config schema errors:\n" + "\n".join(messages))


def validate_hl7_rules(config):
    names = set()

    for field in config:
        name = field["name"]

        if name in names:
            raise ValueError(f"Duplicate output field name: {name}")

        names.add(name)

        for source in field["source"]:
            segment = source["segment"]
            if len(segment) != 3:
                raise ValueError(f"Invalid HL7 segment in path: {path}")

        # Add deeper HL7Extract-specific checks here.


def validate_rules(rules_path, schema_path):
    rules = load_json(rules_path)
    schema = load_json(schema_path)

    validate_schema(rules, schema)
    validate_hl7_rules(rules)

    return rules

def validate_config(config_path, schema_path):
    config = load_json(config_path)
    schema = load_json(schema_path)

    validate_schema(config, schema)
    #TODO: deeper config validation (file location, 
    # net access, etc) here
    #validate_system_config(config)

    return config 
 
