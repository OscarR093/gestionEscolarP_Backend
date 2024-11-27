from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# URL de conexión a MongoDB Atlas
MONGO_URI = os.getenv("DATABASE_URL")

# Inicializar cliente de MongoDB
client = MongoClient(MONGO_URI)

# Base de datos
db = client.gestion_escolar
