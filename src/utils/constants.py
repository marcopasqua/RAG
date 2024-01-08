from pathlib import Path

from dotenv import load_dotenv
import os

file_path = Path(__file__).parent.resolve()
env_path = file_path.parent.parent.joinpath(".env")
load_dotenv(env_path)

UNSTRUCTURED_API_KEY = os.getenv("UNSTRUCTURED_API_KEY")
LOCAL_STORAGE_PATH = file_path.parent.parent.joinpath("files")
if not LOCAL_STORAGE_PATH.exists():
    LOCAL_STORAGE_PATH.mkdir(parents=True)
INDEX_PATH = file_path.parent.parent.joinpath("index")
if not INDEX_PATH.exists():
    INDEX_PATH.mkdir(parents=True)

MONGO_URI = os.environ.get("MONGO_URI")

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")


