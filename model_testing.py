import openai
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI Client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# List Available Models
models = client.models.list()

# Print Model IDs
print([m.id for m in models])
