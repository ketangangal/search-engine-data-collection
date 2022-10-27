import os
import requests
import base64
from io import BytesIO
import io
from PIL import Image
from from_root import from_root
from tqdm import tqdm


def test_fetch_api():
    url = "http://localhost:8080/fetch"
    x = requests.get(url)
    print(x.content)


def test_add_label(label):
    res = requests.post("http://localhost:8080/add_label",
                        headers={
                            'Content-type': 'application/json'
                        },
                        json={"label_name": label},
                        )
    print(res.content)


def test_single_upload(data):
    res = requests.post("http://localhost:8080/single_upload",
                        headers={
                            'Content-type': 'application/json'
                        },
                        json={"label": "test1", "image": data.decode()},
                        )
    print(res.content)


def test_bulk_upload(label, data):
    res = requests.post("http://localhost:8080/bulk_upload",
                        headers={
                            'Content-type': 'application/json'
                        },
                        json={"label": label, "images": data},
                        )
    print(res.content)


def upload_bulk_data(root="caltech-101"):
    labels = os.listdir(root)
    test_fetch_api()
    for label in tqdm(labels):
        data = []
        images = os.listdir(root + "/" + label)
        for img in tqdm(images):
            path = os.path.join(from_root(), root, label, img)
            with open(rf'{path}', "rb") as img:
                data.append(base64.b64encode(img.read()).decode())
        test_bulk_upload(label, data)

    print("/nCompleted")


upload_bulk_data(root="caltech-101")
