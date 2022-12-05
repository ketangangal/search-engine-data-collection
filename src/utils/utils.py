import uuid


# Generate Unique Names for all the images
def image_unique_name():
    return "img-" + str(uuid.uuid1())
