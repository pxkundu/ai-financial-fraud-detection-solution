# Integration Recipe
# Outputs validated data to database, CSV, or API
import yaml
import csv

def output_to_csv(validated, csv_path):
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['s3_key'] + list(validated[0]['fields'].keys()) + ['errors']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in validated:
            out = {'s3_key': row['s3_key'], **row['fields'], 'errors': ';'.join(row['errors'])}
            writer.writerow(out)

def run_integration(config_path, validated):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    integration_conf = config['integration']
    if integration_conf['output_type'] == 'csv':
        output_to_csv(validated, integration_conf['csv_path'])
    elif integration_conf['output_type'] == 'database':
        # Placeholder: implement DB integration
        pass
    elif integration_conf['output_type'] == 'api':
        # Placeholder: implement API integration
        pass
    else:
        raise ValueError('Unsupported output type')

# Example usage:
# run_integration('config/sample_config.yaml', validated) 