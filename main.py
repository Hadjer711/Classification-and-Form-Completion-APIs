from fastapi import FastAPI
import os
from baml_client import b
from fastapi.responses import StreamingResponse
import asyncio


app = FastAPI()

@app.get("/classify")
async def classify():
    input = """
    {
    "text": "I am calling because I have a problem with my internet connection",
    "themes": [
        {
            "title": "Technical support",
            "description": "The customer is calling for technical support"
        },
        {
            "title": "Billing",
            "description": "The customer is calling for billing issues"
        },
        {
            "title": "Refund",
            "description": "The customer is calling for a refund"
        }
    ]
}
    """

    async def stream_class(input):
        stream = b.stream.Classify(input)
        for chunk in stream:
            print(f"Got chunk: {chunk}")
            yield (str(chunk.model_dump_json()) + "\n")
            await asyncio.sleep(
                0
            )  
    return StreamingResponse(stream_class(input), media_type="text/event-stream")

@app.get("/form_completion")
async def extract_complete_form():
    input = """
    {
    "text": "Agent: Good morning! Thank you for reaching out. I’ll need to collect some basic details to assist you better. Could you please provide your first and last name? Customer: Sure! My name is John Doe. Agent: Thank you, John. May I also ask for your gender? Customer: I'd prefer not to share that at the moment. Agent: No problem at all. Now, for contact purposes, could you share your email address? Customer: Yes, my email is johndoe@example.com. Agent: Great! Do you have a phone number where we can reach you? Customer: I’d rather not provide that right now. Agent: That’s completely fine. How would you prefer us to contact you—by email or phone? Customer: Please contact me via Email. Agent: Understood! Lastly, can you share the reason for your call today? Customer: I’m not ready to specify that just yet. Agent: That’s okay, John! I’ve noted everything down. If you need any further assistance, feel free to reach out. Have a great day!"
}
    """

    async def stream_form(input):
        stream = b.stream.Form_Completetion(input)
        for chunk in stream:
            print(f"Got chunk: {chunk}")
            yield (str(chunk.model_dump_json()) + "\n")
            await asyncio.sleep(
                0
            )  
    return StreamingResponse(stream_form(input), media_type="text/event-stream")