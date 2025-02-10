import os
import requests
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env (opcional)
load_dotenv()

# Obtén la clave API desde las variables de entorno
api_key = os.getenv("GROQ_API_KEY")

# Verifica si la clave API está configurada
if not api_key:
    raise ValueError("La clave API no está configurada. Asegúrate de definir GROQ_API_KEY en el entorno.")

# URL de la API de Groq para generar resúmenes
url = "https://api.groq.com/openai/v1/chat/completions"

def generar_contestacion(intencion, entidades, lenguaje="es"):
    # Información fija de la tienda
    tienda_info = {
        "nombre": "Gymstore",
        "web": "www.gymstore.com",
        "telefono": "666555777",
        "email": "gymstoresupport@gmail.com",
        "productos": ["camisetas", "pesas", "proteina", "creatina", "pantalones", "vitaminas", "straps", "muñequeras", "cinturones", "botellas"]
    }

    # Respuestas para cada tipo de intención
    mensaje_intencion = {
        "comprar": "El usuario desea saber cómo realizar compras en la tienda. Indica el proceso de compra en línea.",
        "contactar": "El usuario quiere saber cómo contactar con el soporte de la tienda. Proporciona el número de contacto y el correo.",
        "devolver": "El usuario tiene preguntas sobre cómo devolver un producto. Describe el proceso de devolución.",
        "envio": "El usuario quiere saber sobre el proceso de envío. Indica los tiempos y métodos de envío disponibles.",
        "instrucciones": "El usuario está buscando instrucciones sobre el uso de productos de gimnasio. Proporciona una guía general.",
        "metodos de pago": "El usuario quiere conocer los métodos de pago disponibles. Explica qué opciones hay para pagar."
    }

    # Datos para el modelo
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Eres un chatbot experto en responder preguntas frecuentes para una tienda de material de gimnasio llamada Gymstore. "
                    "Usa la información proporcionada para generar respuestas útiles y claras sobre la tienda. Si no conoces una respuesta específica, "
                    "invéntatela de manera coherente y mantén siempre la profesionalidad. Usa el nombre de la tienda, su número de contacto y su página web cuando sea necesario."
                )
            },
            {
                "role": "user",
                "content": (
                    f"El usuario tiene la intención de {intencion}. Las entidades que se mencionan son: {entidades}. "
                    f"Responde de manera profesional y usa la información sobre la tienda Gymstore. "
                    f"Recuerda que la tienda se llama Gymstore, su página web es www.gymstore.com, "
                    f"el teléfono de contacto es 666555777 y el email es gymstoresupport@gmail.com."
                )
            }
        ],
        "temperature": 0.7,  # Controla el nivel de creatividad (ajustado para respuestas profesionales)
    }

    # Respuesta inventada para las instrucciones
    if intencion == "instrucciones":
        # Lista de productos con respuestas inventadas
        respuestas_inventadas = {
            "camisetas": "Para cuidar tus camisetas de gimnasio, te recomendamos lavarlas a mano o en el ciclo más suave de la lavadora para evitar que se deformen. Evita usar blanqueadores o secarlas al sol directamente.",
            "pesas": "Las pesas deben almacenarse en un lugar seco y limpio. Si son de metal, límpialas regularmente con un paño seco para evitar la oxidación.",
            "proteina": "Para obtener los mejores resultados, mezcla una porción de proteína con agua o leche fría. Se recomienda tomarla después de tus entrenamientos para maximizar la recuperación muscular.",
            "creatina": "La creatina se debe tomar con agua o jugo antes o después del entrenamiento. Se recomienda hacer un ciclo de 4-6 semanas con descanso de 2 semanas entre ciclos.",
            "pantalones": "Los pantalones deben ser lavados a máquina con agua fría y secados al aire para evitar que pierdan elasticidad.",
            "vitaminas": "Las vitaminas se deben tomar según las instrucciones del producto. Generalmente, se recomienda tomarlas con las comidas para una mejor absorción.",
            "straps": "Para el cuidado de straps y muñequeras, se debe lavar a mano con detergente suave y dejarlos secar al aire.",
            "muñequeras": "Las muñequeras deben limpiarse con un paño húmedo y dejarse secar al aire para mantenerlas en buen estado.",
            "cinturones": "Los cinturones deben limpiarse con un paño húmedo y, si es de cuero, utilizar un acondicionador especial para mantener su flexibilidad.",
            "botellas": "Limpia tu botella después de cada uso con agua y jabón. Si es de acero inoxidable, evita usar limpiadores abrasivos."
        }
        # Crear un mensaje con las instrucciones para los productos mencionados
        instrucciones = []
        for producto in entidades:
            if producto in respuestas_inventadas:
                instrucciones.append(f"{producto.capitalize()}: {respuestas_inventadas[producto]}")

        # Construir la respuesta final
        respuesta_instrucciones = "\n".join(instrucciones)
        return respuesta_instrucciones

    # Si no es la intención de instrucciones, proceder con la API de Groq
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            # Respuesta exitosa
            return response.json().get("choices")[0].get("message").get("content") 
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"Error al generar la respuesta: {e}")
        return None
