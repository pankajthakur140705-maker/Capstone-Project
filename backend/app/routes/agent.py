from fastapi import APIRouter
from pydantic import BaseModel
from app.brain.agent import run_agent

router = APIRouter()


class AgentRequest(BaseModel):
    user_id: str
    message: str


@router.post("/agent")
def agent(req: AgentRequest):

    return run_agent(
        user_id=req.user_id,
        message=req.message
    )