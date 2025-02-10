import os
from dotenv import load_dotenv


from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

load_dotenv()
ls_prediction_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
ls_prediction_key = os.getenv('AI_SERVICE_KEY')


cls_project = 'GYMSTORE_UNDERSTANDING'
deployment_slot = 'intencionesentidades'

def analyze_conversation(text):
    
    client = ConversationAnalysisClient(
        ls_prediction_endpoint, AzureKeyCredential(ls_prediction_key))

    result = client.analyze_conversation(
        task={
            "kind": "Conversation",
            "analysisInput": {
                "conversationItem": {
                    "participantId": "1",
                    "id": "1",
                    "modality": "text",
                    "language": "es",
                    "text": text
                },
                "isLoggingEnabled": False
            },
            "parameters": {
                "projectName": cls_project,
                "deploymentName": deployment_slot,
                "verbose": True
            }
        }
    )

    top_intent = result["result"]["prediction"]["topIntent"]
    entities = result["result"]["prediction"]["entities"]
    return top_intent, entities