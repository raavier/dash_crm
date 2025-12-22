"""
Chatbot API routes - Proxy para Databricks MLFlow Serving Endpoint
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
from databricks.sdk.core import Config
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chatbot"])


class ChatRequest(BaseModel):
    """Request model for chat message"""
    user_id: str
    query: str


class ChatResponse(BaseModel):
    """Response model from Databricks chatbot"""
    response: str


@router.post("/message", response_model=ChatResponse)
async def send_chat_message(request: ChatRequest):
    """
    Proxy para Databricks MLFlow serving endpoint.

    Args:
        request: ChatRequest com user_id e query

    Returns:
        ChatResponse com a resposta do chatbot
    """
    try:
        logger.info(f"Chat message - User: {request.user_id}, Query: {request.query[:50]}...")

        # Get token using SDK Config (same pattern as database.py)
        cfg = Config()
        auth_headers = cfg.authenticate()  # Returns dict with Authorization header

        # Headers com token Databricks
        headers = {
            **auth_headers,  # Merge auth headers (already has Authorization)
            "Content-Type": "application/json"
        }

        # Payload para Databricks - DEVE ser wrapped em "inputs"
        payload = {
            "inputs": {
                "user_id": request.user_id,
                "query": request.query
            }
        }

        logger.info(f"Sending payload to Databricks: {payload}")

        # Request para Databricks MLFlow endpoint
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://adb-116288240407984.4.azuredatabricks.net/serving-endpoints/connect_bot_prd/invocations",
                headers=headers,
                json=payload,
                timeout=90.0  # Increased from 30s to 90s
            )
            response.raise_for_status()

        data = response.json()
        logger.info(f"Chat response received for user {request.user_id}")

        # Databricks retorna {"predictions": {"content": "...", "feedback_required": bool}}
        predictions = data.get("predictions", {})
        content = predictions.get("content", "")

        return ChatResponse(response=content)

    except httpx.HTTPError as e:
        logger.error(f"Error calling Databricks endpoint: {str(e)}")
        raise HTTPException(
            status_code=502,
            detail=f"Error communicating with chatbot service: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in chat: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
