import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Cargar dataset desde un archivo CSV
data = pd.read_csv("spam_assassin.csv")
#data = pd.read_csv("ej2.csv")

# Función para preprocesar el texto
# Convierte el texto a minúsculas, elimina caracteres no alfanuméricos y tokeniza.
def preprocesar_texto(texto):
    texto = texto.lower()  # Convertir todo el texto a minúsculas
    texto = re.sub(r'[^a-z0-9]', ' ', texto)  # Reemplazar caracteres no alfanuméricos con espacios
    palabras = texto.split()  # Tokenizar el texto dividiéndolo en palabras
    return " ".join(palabras)  # Volver a unir las palabras en una sola cadena

# Aplicar preprocesamiento a la columna de texto
data["text"] = data["text"].astype(str).apply(preprocesar_texto)

# Vectorizar el texto utilizando el modelo TF-IDF
vectorizador = TfidfVectorizer()
X = vectorizador.fit_transform(data["text"])
y = data["target"].values  # Etiquetas (1 = spam, 0 = no spam)

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar un modelo de Naïve Bayes para clasificación de spam
modelo = MultinomialNB() 
modelo.fit(X_train, y_train)

# Evaluar el modelo con datos de prueba
predicciones = modelo.predict(X_test)
print(f"Precisión del modelo: {accuracy_score(y_test, predicciones):.4f}\n")

# Función que aplica reglas predefinidas para detectar spam (razonamiento monótono)
def razonamiento_monotono(correo):
    """Aplica reglas manuales para detectar spam en un correo."""
    print("\n--- Razonamiento MONÓTONO ---")
    cont = 0  # Contador de detecciones de spam
    
    correo = correo.lower()  # Convertir a minúsculas para evitar problemas con mayúsculas

    # 1 Detectar enlaces sospechosos
    if "builtit4unow.com" in correo or "wiildaccess.com" in correo:
        print("Posible spam: Enlace sospechoso encontrado.")
        cont += 1

    # 2 Detectar frases persuasivas
    if "gratis" in correo or "hazlo ahora" in correo or  "oferta especial" in correo:
        print("Posible spam: Frase persuasiva encontrada.")
        cont += 1

    # 3 Detectar exceso de signos de exclamación o interrogación
    if "!!!" in correo or "???" in correo:
        print("Posible spam: Exceso de signos de exclamación o interrogación.")
        cont += 1

    # 4 Detectar frases relacionadas con dinero o premios
    if "has ganado" in correo or "dinero fácil" in correo or "transferencia bancaria" in correo or "bitcoin" in correo or "premio garantizado" in correo:
        print("Posible spam: Frases relacionadas con dinero o premios encontradas.")
        cont += 1

    # 5 Detectar direcciones de correo con dominios sospechosos
    if "@xyz" in correo or "@top" in correo or "@click" in correo or "@info" in correo:
        print("Posible spam: Dirección de correo con dominio sospechoso.")
        cont += 1

    # 6 Demasiadas palabras en MAYÚSCULAS
    palabras = correo.split()
    mayusculas = sum(1 for palabra in palabras if palabra.isupper())
    if mayusculas > 3:  # Si hay más de 3 palabras en mayúsculas, podría ser spam
        print("Posible spam: Exceso de palabras en MAYÚSCULAS.")
        cont += 1

    # 7 Uso de emojis relacionados con dinero/regalos/ofertas
    if "💰" in correo or "🔥" in correo or "💵" in correo or "🎁" in correo:
        print("Posible spam: Uso de emojis llamativos.")
        cont += 1

    # 8 Palabras que crean urgencia
    if "urgente" in correo or "acción inmediata" in correo or "solo hoy" in correo or "última oportunidad" in correo:
        print("Posible spam: Uso de palabras que generan urgencia.")
        cont += 1

    # 9 Correos electrónicos con números extraños o caracteres raros
    if re.search(r'[a-zA-Z]+[0-9]{3,}@', correo) or re.search(r'[a-zA-Z]+@[a-zA-Z0-9-]+\.(xyz|top|click|info)', correo):
        print("Posible spam: Dirección de correo con demasiados números o caracteres sospechosos.")
        cont += 1

    # 10 Demasiados enlaces en el correo (más de 3)
    enlaces = correo.count("http")
    if enlaces > 3:
        print("Posible spam: Demasiados enlaces en el correo.")
        cont += 1

    # Resultado final
    if cont == 0:
        print("El correo NO contiene spam.")
    else:
        print(f"Total de detecciones de spam: {cont}")

# Función que usa el modelo de aprendizaje automático para detectar spam (razonamiento no monótono)
def razonamiento_no_monotono(correo):
    """Usa un modelo de aprendizaje automático para clasificar el correo y mostrar palabras relevantes."""
    print("\n--- Razonamiento NO-MONÓTONO ---")
    
    # Preprocesar y vectorizar el correo ingresado
    correo_proc = preprocesar_texto(correo)
    correo_tfidf = vectorizador.transform([correo_proc])
    
    # Obtener la predicción
    prediccion = modelo.predict(correo_tfidf)
    
    # Obtener los pesos de las palabras en el correo
    pesos = correo_tfidf.toarray()[0]  # Convertir a un array (solo hay un correo analizado)
    palabras = vectorizador.get_feature_names_out()  # Obtener las palabras del vocabulario TF-IDF
    # Filtrar palabras con pesos significativos (> 0) y ordenarlas por peso descendente
    palabras_pesadas = [(palabras[i], pesos[i]) for i in range(len(pesos)) if pesos[i] > 0]
    palabras_pesadas.sort(key=lambda x: x[1], reverse=True)  # Ordenar por peso descendente
    
    # Mostrar resultado
    if prediccion[0] == 1:
        print("¡El correo es SPAM!")
        print("\nPalabras clave que influyeron en la detección:")
        for palabra, peso in palabras_pesadas[:10]:  # Mostrar las 10 palabras más relevantes
            print(f" - {palabra}: {peso:.4f}")
    else:
        print("El correo NO es spam.")


# Programa principal con un menú interactivo
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
