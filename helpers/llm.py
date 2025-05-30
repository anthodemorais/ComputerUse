import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient, ChatCompletionOutputMessage

load_dotenv()

client = InferenceClient(
    provider="novita",
    api_key=os.getenv("HF_API_KEY"),
)

def call_llm(messages):
    # This is for local work, when deployed, use the model directly or official API to not be limited by the number of tokens or requests
    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3-0324", 
        messages=messages, 
        max_tokens=1000,
    )

    return completion.choices[0].message

def get_message_output(message: ChatCompletionOutputMessage):
    return message.content.split("</think>").pop().strip()
