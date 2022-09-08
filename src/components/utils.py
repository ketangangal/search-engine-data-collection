import uuid
import yaml


def image_unique_name():
    return "img-" + str(uuid.uuid1())


def read_config(config_path="config.yaml"):
    with open(config_path) as config_file:
        content = yaml.safe_load(config_file)

    return content
