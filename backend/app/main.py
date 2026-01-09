from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserMessage(BaseModel):
    text: str

@app.post("/chat")
async def chat_endpoint(message: UserMessage):
    return {"reply": f"Backend reçu : {message.text}"}