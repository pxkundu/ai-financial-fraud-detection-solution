# Field Extraction Recipe
# Extracts structured fields from cleaned text using regex
import re
import yaml

def extract_fields(cleaned_text, field_patterns):
    fields = {}
    for field, conf in field_patterns.items():
        if conf.get('table'):
            # Placeholder: implement table extraction logic
            fields[field] = []
        else:
            pattern = conf['pattern']
            match = re.search(pattern, '\n'.join(cleaned_text))
            fields[field] = match.group(1) if match else None
    return fields

def run_field_extraction(config_path, cleaned_results):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    field_patterns = config['fields']
    extracted = []
    for result in cleaned_results:
        fields = extract_fields(result['cleaned_text'], field_patterns)
        extracted.append({'s3_key': result['s3_key'], 'fields': fields})
    return extracted

# Example usage:
# extracted = run_field_extraction('config/sample_config.yaml', cleaned)
# print(extracted) 