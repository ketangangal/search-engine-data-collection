# Create a simple API-based webpage to upload images to the s3 bucket.
# Single upload and Bulk upload.
# Nginx's authentication user to upload images.
# Single upload API will be used while inference to collect data at runtime.
from typing import Dict
from src.Exception.exception import IntegrityError
import boto3.session
import boto3
from src.components.utils import read_config, image_unique_name
import os


# Create aws cred secure config - GitHub actions

class S3Connection:
    """ Data Class for reverse image search engine."""

    def __init__(self):
        self.s3 = boto3.resource("s3")
        self.bucket = self.s3.Bucket("image-database-system")
        self.header = r"https://image-database-system.s3.ap-south-1.amazonaws.com"

    def add_label(self, label: str) -> Dict:
        """
         This Function is responsible for adding label in s3 bucket.
         :param label: label Name
         :return: json Response of state message (success or failure)
         """
        try:
            key = f"images/{label}/"
            response = self.bucket.put_object(Body='', Key=key)
            return {"Created": True, "Path": response.key}
        except Exception as e:
            return {"Created": False, "Reason": e}

    def single_upload(self, image_path, label: str):
        """
        This Function is responsible for uploading single image in the predefined
        location in the s3 bucket.
        :param label: label Name
        :param image_path: Path to the image to upload
        :return: json Response of state message (success or failure)
        """
        try:
            self.bucket.upload_fileobj(image_path, f'images/{label}/{image_unique_name()}.jpeg',
                                       ExtraArgs={'ACL': 'public-read'})
            return {"Created": True}
        except Exception as e:
            return {"Created": False, "Reason": e}

    def bulk_upload(self, folder_path: str, label: str):
        """
        This Function is responsible for uploading bulk images in the predefined
        location in the s3 bucket.
        :param label: label Name
        :param folder_path: Path to the folder to upload
        :return: json Response of state message (success or failure)
        """


if __name__ == "__main__":
    dc = S3Connection()
    print(dc.add_label("test"))
