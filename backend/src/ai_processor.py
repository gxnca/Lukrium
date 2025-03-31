import os
from dotenv import load_dotenv
from google import genai

# Carregar variáveis do ficheiro .env
load_dotenv()

# Obter a API key do ambiente
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY não encontrada. Verifica o ficheiro .env")

client = genai.Client(api_key=api_key)

def generate_statistics(PROMPT):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=PROMPT,
    )
    return response