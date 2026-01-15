"""Test Backend - Version DEBUG"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    conversation_history: list = []

class ChatResponse(BaseModel):
    response: str
    playlist: dict = None
    error: str = None

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Test ultra-simple"""
    print(f"\n📩 Message reçu: {request.message}")
    
    # Toujours retourner le même message court
    response_text = f"✨ Test ! Tu as dit: '{request.message}'"
    
    print(f"📝 Réponse envoyée: {response_text}")
    
    return ChatResponse(
        response=response_text,
        playlist=None,
        error=None
    )

if __name__ == "__main__":
    import uvicorn
    print("\n🧪 SERVEUR TEST")
    print("=" * 70)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")