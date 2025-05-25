
import cv2
import os
import numpy as np
from pathlib import Path
from tqdm import tqdm

# Ruta de entrada y salida
ruta_original = "entrenamiento"
ruta_salida = "entrenamiento_preprocesado"

# Crear carpetas si no existen
Path(ruta_salida).mkdir(parents=True, exist_ok=True)

# Recorrer las carpetas de emociones
for clase in os.listdir(ruta_original):
    ruta_clase = os.path.join(ruta_original, clase)
    
    if not os.path.isdir(ruta_clase) or clase.startswith('.'):
        continue  # Saltar .DS_Store y archivos no válidos

    # Crear subcarpeta en la salida
    Path(os.path.join(ruta_salida, clase)).mkdir(parents=True, exist_ok=True)

    # Procesar cada imagen
    for nombre_imagen in tqdm(os.listdir(ruta_clase), desc=f"Procesando {clase}"):
        ruta_img = os.path.join(ruta_clase, nombre_imagen)
        img = cv2.imread(ruta_img)

        if img is None:
            continue

        # Reescalar imagen a 128x128
        img = cv2.resize(img, (128, 128))

        # Convertir a escala de grises
        gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Reducción de ruido (puedes usar uno u otro)
        gris = cv2.medianBlur(gris, 3)  # O cv2.bilateralFilter(gris, 9, 75, 75)

        # Realce de contraste con CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        mejorada = clahe.apply(gris)

        # Guardar la imagen preprocesada
        ruta_guardar = os.path.join(ruta_salida, clase, nombre_imagen)
        cv2.imwrite(ruta_guardar, mejorada)
