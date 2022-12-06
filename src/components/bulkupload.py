import os
import base64
from from_root import from_root
from tqdm import tqdm


# Upload data using boto3 [ Takes a lot of time ]
def upload_bulk_data(root="caltech-101"):
    labels = os.listdir(root)
    for label in tqdm(labels):
        data = []
        images = os.listdir(root + "/" + label)
        for img in tqdm(images):
            path = os.path.join(from_root(), root, label, img)
            with open(rf'{path}', "rb") as img:
                data.append(base64.b64encode(img.read()).decode())

    print("/nCompleted")


upload_bulk_data(root="caltech-101")
