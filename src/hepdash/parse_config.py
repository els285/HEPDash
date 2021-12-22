import yaml

def parse_config(yaml_file):
    with open(yaml_file, 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    return data_loaded
