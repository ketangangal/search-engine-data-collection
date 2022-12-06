import os, sys
import boto3
import boto3.session

from typing import Dict

from src.utils.utils import image_unique_name
from src.exception import CustomException


class S3Connection:
    """Data Class for reverse image search engine."""

    def __init__(self):
        session = boto3.Session(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        )
        self.s3 = session.resource("s3")
        self.bucket = self.s3.Bucket(os.environ["AWS_BUCKET_NAME"])

    def add_label(self, label: str) -> Dict:
        """
         This Function is responsible for adding label in s3 bucket.
         param label: label Name
         :return: json Response of state message (success or failure)
         """
        try:
            key = f"images/{label}/"
            response = self.bucket.put_object(Body="", Key=key)
            return {"Created": True, "Path": response.key}
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}

    def upload_to_s3(self, image_path, label: str):
        """
        This Function is responsible for uploading images in the predefined
        location in the s3 bucket.
        param label: label Name
        :param image_path: Path to the image to upload
        :return: json Response of state message (success or failure)
        """
        try:
            self.bucket.upload_fileobj(
                image_path,
                f"images/{label}/{image_unique_name()}.jpeg",
                ExtraArgs={"ACL": "public-read"},
            )
            return {"Created": True}
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}
