from modules.intententity import analyze_conversation
from modules.contestador import generar_contestacion

def unirentities(entities):
    texto=""
    for entity in entities:
        texto+=entity["text"]+" "
    return texto


def comprension(texto):
    intent, enties=analyze_conversation(texto)
    entidades=unirentities(enties)

    if intent=="Comprar":

        contestacion=generar_contestacion("comprar", entidades)
        return (contestacion)
    
    elif intent=="Contactar":
        
        contestacion=generar_contestacion("contactar", entidades)
        return (contestacion)

    elif intent=="Devolver":
    
        contestacion=generar_contestacion("devolver", entidades)
        return (contestacion)

    elif intent=="Envio":
       
        contestacion=generar_contestacion("envio", entidades)
        return (contestacion)

    elif intent=="Instrucciones":
        
        contestacion=generar_contestacion("instrucciones", entidades)
        return (contestacion)

    elif intent=="Metodos de Pago":

        contestacion=generar_contestacion("metodos de pago", entidades)
        return (contestacion)
    
    else:
        return("Ha ocurrido un fallo en la app, no se ha encontrado la intencion de la pregunta")    

