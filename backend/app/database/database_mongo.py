from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

print("ENV PATH:", env_path)
print("MONGO_URI:", MONGO_URI)
print("DB_NAME:", DB_NAME)

if not MONGO_URI or not DB_NAME:
    raise Exception("Variables de entorno MONGO_URI o DB_NAME no definidas")
