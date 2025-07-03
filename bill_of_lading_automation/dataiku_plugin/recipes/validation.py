# Validation Recipe
# Validates extracted fields and applies business rules
import yaml
from datetime import datetime

def validate_fields(fields, validation_conf):
    errors = []
    for req in validation_conf['required_fields']:
        if not fields.get(req):
            errors.append(f"Missing required field: {req}")
    # Date format check
    date_field = fields.get('date')
    if date_field:
        try:
            datetime.strptime(date_field, validation_conf['date_format'])
        except Exception:
            errors.append(f"Invalid date format: {date_field}")
    # Placeholder: duplicate check, business rules
    return errors

def run_validation(config_path, extracted):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    validation_conf = config['validation']
    validated = []
    for result in extracted:
        errors = validate_fields(result['fields'], validation_conf)
        validated.append({'s3_key': result['s3_key'], 'fields': result['fields'], 'errors': errors})
    return validated

# Example usage:
# validated = run_validation('config/sample_config.yaml', extracted)
# print(validated) 