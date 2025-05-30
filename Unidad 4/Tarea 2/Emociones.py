import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Obtener ruta absoluta del archivo actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "entrenamiento_preprocesado")


EMOCIONES = sorted(os.listdir(DATA_DIR))


def cargar_datos():
    print("Cargando imágenes...")
    X, y = [], []
    for idx, clase in enumerate(EMOCIONES):
        carpeta = os.path.join(DATA_DIR, clase)
        for archivo in os.listdir(carpeta):
            ruta = os.path.join(carpeta, archivo)
            img = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            img = img / 255.0
            X.append(img)
            y.append(idx)
    X = np.array(X).reshape(-1, 128, 128, 1)
    y = to_categorical(y, num_classes=len(EMOCIONES))
    return train_test_split(X, y, test_size=0.2, random_state=42)

def construir_modelo():
    model = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=(128,128,1)),
        MaxPooling2D(2,2),
        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Conv2D(128, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(len(EMOCIONES), activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def entrenar_modelo():
    X_train, X_test, y_train, y_test = cargar_datos()
    model = construir_modelo()
    model.fit(X_train, y_train, epochs=25, batch_size=32, validation_data=(X_test, y_test))
    model.save("modelo_emociones.h5")
    print("Modelo entrenado y guardado como 'modelo_emociones.h5'.")

def predecir_imagen():
    modelo = load_model("modelo_emociones.h5")
    ruta = input("Ruta de la imagen: ").strip()
    img = cv2.imread(ruta)
    if img is None:
        print("No se pudo cargar la imagen.")
        return
    img = cv2.resize(img, (128,128))
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gris = cv2.medianBlur(gris, 3)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    procesada = clahe.apply(gris)
    procesada = procesada / 255.0
    procesada = np.expand_dims(procesada, axis=(0,-1))
    pred = modelo.predict(procesada)
    emocion = EMOCIONES[np.argmax(pred)]
    print(f"Emoción detectada: {emocion}")
    cv2.putText(img, emocion, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.imshow("Resultado", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def camara_web():
    modelo = load_model("modelo_emociones.h5")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No se pudo acceder a la cámara.")
        return
    print("Presiona 'q' para salir.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        img = cv2.resize(frame, (128,128))
        gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gris = cv2.medianBlur(gris, 3)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        procesada = clahe.apply(gris)
        procesada = procesada / 255.0
        procesada = np.expand_dims(procesada, axis=(0,-1))
        pred = modelo.predict(procesada)
        emocion = EMOCIONES[np.argmax(pred)]
        cv2.putText(frame, emocion, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.imshow("Webcam - Detector de emociones", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def menu():
    while True:
        print("\n--- DETECTOR DE EMOCIONES ---")
        print("1. Entrenar modelo")
        print("2. Probar con imagen")
        print("3. Usar cámara web")
        print("4. Salir")
        opcion = input("Elige una opción: ")

        if opcion == '1':
            entrenar_modelo()
        elif opcion == '2':
            predecir_imagen()
        elif opcion == '3':
            camara_web()
        elif opcion == '4':
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()
