import requests


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


# Write your test case here
if __name__ == "__main__":
    test_fetch_api()