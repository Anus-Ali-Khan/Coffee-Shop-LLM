from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent_controller import AgentController
import uvicorn

app = FastAPI(title="Coffee Shop LLM API", description="API for interacting with the coffee shop LLM agents")

agent_controller = AgentController()

# In-memory storage for conversation sessions
sessions = {}

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    session_id = request.session_id
    user_message = request.message

    # Get or create session messages
    if session_id not in sessions:
        sessions[session_id] = []

    messages = sessions[session_id]

    # Add user message
    messages.append({"role": "user", "content": user_message})

    try:
        # Get agent response
        response = agent_controller.get_response({"input": {"messages": messages}})

        # Add response to messages
        messages.append(response)

        return ChatResponse(response=response["content"], session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.get("/health")
# async def health():
#     return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)