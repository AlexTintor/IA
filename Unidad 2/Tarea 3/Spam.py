import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Cargar dataset
data = pd.read_csv("spam_assassin.csv")

# Preprocesamiento del texto
def preprocesar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-z0-9]', ' ', texto)
    palabras = texto.split()
    return " ".join(palabras)

# Aplicar preprocesamiento
data["text"] = data["text"].astype(str).apply(preprocesar_texto)

# Vectorizar texto con TF-IDF
vectorizador = TfidfVectorizer()
X = vectorizador.fit_transform(data["text"])
y = data["target"].values  # Etiquetas (1 = spam, 0 = no spam)

# Dividir datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelo de Naïve Bayes
modelo = MultinomialNB()
modelo.fit(X_train, y_train)

# Evaluar modelo
predicciones = modelo.predict(X_test)
print(f"Precisión del modelo: {accuracy_score(y_test, predicciones):.4f}\n")

def razonamiento_monotono(correo):
    """Aplica reglas manuales para detectar spam."""
    print("\n--- Razonamiento MONÓTONO ---")
    cont = 0  # Contador de detecciones de spam
    
    # Reglas
    reglas = [
        (r'(builtit4unow\.com|wiildaccess\.com)', "Enlace sospechoso encontrado."),
        (r'(gratis|hazlo ahora|sin compromiso|oferta especial)', "Frase persuasiva encontrada."),
        (r'[!?]{3,}', "Exceso de signos de exclamación o interrogación."),
        (r'(has ganado|dinero fácil|transferencia bancaria|bitcoin|premio garantizado)', "Frases relacionadas con dinero o premios encontradas."),
        (r'@[a-zA-Z0-9-]+\.(xyz|top|click|info)', "Dirección de correo con dominio sospechoso.")
    ]
    
    for patron, mensaje in reglas:
        if re.search(patron, correo, re.IGNORECASE):
            print(f"Posible spam: {mensaje}")
            cont += 1
    
    if cont == 0:
        print("El correo NO contiene spam.")
    else:
        print(f"Total de detecciones de spam: {cont}")

def razonamiento_no_monotono(correo):
    """Usa un modelo de aprendizaje automático para clasificar el correo."""
    print("\n--- Razonamiento NO-MONÓTONO ---")
    correo_proc = preprocesar_texto(correo)
    correo_tfidf = vectorizador.transform([correo_proc])
    prediccion = modelo.predict(correo_tfidf)
    print("Spam" if prediccion[0] == 1 else "No Spam")

if __name__ == "__main__":
    while True:  
        print("\n   Técnica a utilizar: ")
        print("[1] Razonamiento Monótono")
        print("[2] Razonamiento No-Monótono")
        print("[0] Salir")
        opc = input("Opción: ")
        
        try:
            opc = int(opc)
        except ValueError:
            print("Por favor ingresa un número válido")
            exit()
        
        if opc == 1:
            correo = input("Ingrese el correo a analizar: ")
            razonamiento_monotono(correo)
        elif opc == 2:
            correo = input("Ingrese el correo a analizar: ")
            razonamiento_no_monotono(correo)
        elif opc == 0:
            break
        else:
            print("Opción no válida")
