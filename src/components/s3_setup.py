import os
import sys
from zipfile import ZipFile
import shutil
from src.exception import CustomException


# https://www.kaggle.com/datasets/imbikramsaha/caltech-101 [ Get data from kaggle and put it into data folder ]

class DataStore:
    def __init__(self):
        self.root = os.path.join(os.getcwd(), "data")
        self.zip = os.path.join(self.root, "archive.zip")
        self.images = os.path.join(self.root, "caltech-101")
        self.list_unwanted = ["BACKGROUND_Google"]

    def prepare_data(self):
        try:
            print(" Extracting Data ")
            with ZipFile(self.zip, 'r') as files:
                files.extractall(path=self.root)

            files.close()
            print(" Process Completed ")
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}

    def remove_unwanted_classes(self):
        try:
            print(" Removing unwanted classes ")
            for label in self.list_unwanted:
                path = os.path.join(self.images,label)
                shutil.rmtree(path, ignore_errors=True)
            print(" Process Completed ")
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}

    def sync_data(self):
        try:
            print("\n====================== Starting Data sync ==============================\n")
            os.system(f"aws s3 sync { self.images } s3://image-search-data/images/ ")
            print("\n====================== Data sync Completed ==========================\n")

        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}

    def run_step(self):
        try:
            self.prepare_data()
            self.remove_unwanted_classes()
            self.sync_data()
            return True
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}


if __name__ == "__main__":
    store = DataStore()
    store.run_step()
