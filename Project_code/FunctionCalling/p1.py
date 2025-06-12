import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import json

load_dotenv()

endpoint = os.getenv("ENDPOINT_URL")
deployment = os.getenv("DEPLOYMENT_NAME")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)

chat_prompt = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are an helpfull AI assistant that helps people find information."
            }
        ]
    }
]

functions = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to get the weather for"
                }
            },
            "required": ["city"]
        }
    }
]

messages = chat_prompt + [
    {
        "role": "user",
        "content": "What's the weather in London?"
    }
]

def get_weather(city):      #Dummy function to simulate weather retrieval
    return f"The weather in {city} is sunny and 25°C."

completion = client.chat.completions.create(
    model=deployment,
    messages=messages,
    functions=functions,
    function_call="auto",
    max_tokens=200,
    temperature=1,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False
)

#print(completion.to_json())
response = completion.to_dict()
message = response["choices"][0]["message"]

if "function_call" in message:
    func_name = message["function_call"]["name"]
    args = json.loads(message["function_call"]["arguments"])
    if func_name == "get_weather":
        weather = get_weather(args["city"])
        print(weather)
else:
    print(message.get("content", "No content returned."))
