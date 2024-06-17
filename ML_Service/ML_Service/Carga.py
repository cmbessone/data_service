from pymongo import MongoClient
from django.conf import settings

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from django.conf import settings

database='mydatabase'
# Conexión a MongoDB
client = MongoClient('localhost', 27017)
db = client[database]
collection_name = 'SPOContenido1'  # Reemplaza con el nombre de tu colección
collection = db[collection_name]

# Convertir los datos de MongoDB a un DataFrame de Pandas
cursor = collection.find()
df = pd.DataFrame(list(cursor))

features = ['¿Aceptas Canje?', 'Rubros de marcas', 'Beneficios a la Marca', 'Valores del Proyecto']
# Filtrar las columnas relevantes
df_filtered = df[features]

le = LabelEncoder()
df_filtered['¿Aceptas Canje?'] = le.fit_transform(df_filtered['¿Aceptas Canje?'].astype(str))

print(df_filtered)

print('Carga Exitosa')
# Cerrar la conexión a MongoDB
client.close()

