from huggingface_hub import InferenceClient, ChatCompletionOutputMessage

client = InferenceClient(
    provider="novita",
    api_key="",
)

def call_llm(messages):
    # This is for local work, when deployed, use the model directly or official API to not be limited by the number of tokens or requests
    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1", 
        messages=messages, 
        max_tokens=1000,
    )

    return completion.choices[0].message

def get_message_output(message: ChatCompletionOutputMessage):
    return message.content.split("</think>").pop().strip()
