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
        logger.info(f"[CHATBOT] Starting request - User: {request.user_id}, Query: {request.query[:50]}...")

        # Get token using SDK Config (same pattern as database.py)
        logger.info("[CHATBOT] Authenticating with Databricks SDK...")
        cfg = Config()
        auth_headers = cfg.authenticate()  # Returns dict with Authorization header
        logger.info("[CHATBOT] Authentication successful")

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

        logger.info(f"[CHATBOT] Payload prepared: {payload}")
        logger.info(f"[CHATBOT] Calling endpoint: connect_bot_dev")

        # Request para Databricks MLFlow endpoint
        async with httpx.AsyncClient() as client:
            logger.info("[CHATBOT] Sending POST request...")
            response = await client.post(
                "https://adb-116288240407984.4.azuredatabricks.net/serving-endpoints/connect_bot_dev/invocations",
                headers=headers,
                json=payload,
                timeout=90.0  # Increased from 30s to 90s
            )
            logger.info(f"[CHATBOT] Response status: {response.status_code}")
            response.raise_for_status()

        data = response.json()
        logger.info(f"[CHATBOT] Response data structure: {list(data.keys())}")
        logger.info(f"[CHATBOT] Full response data: {data}")

        # Databricks retorna {"predictions": {"content": "...", "feedback_required": bool}}
        predictions = data.get("predictions", {})
        content = predictions.get("content", "")

        logger.info(f"[CHATBOT] Extracted content length: {len(content)} chars")
        logger.info(f"[CHATBOT] Success for user {request.user_id}")

        return ChatResponse(response=content)

    except httpx.HTTPStatusError as e:
        # Log full error response for debugging
        error_body = e.response.text if hasattr(e.response, 'text') else str(e)
        logger.error(f"[CHATBOT] HTTPStatusError - Status: {e.response.status_code}")
        logger.error(f"[CHATBOT] Error response body: {error_body}")
        logger.error(f"[CHATBOT] Request URL: {e.request.url}")
        logger.error(f"[CHATBOT] Request headers: {dict(e.request.headers)}")
        raise HTTPException(
            status_code=502,
            detail=f"Error communicating with chatbot service: {error_body}"
        )
    except httpx.HTTPError as e:
        logger.error(f"[CHATBOT] HTTPError: {str(e)}")
        logger.error(f"[CHATBOT] Error type: {type(e).__name__}")
        raise HTTPException(
            status_code=502,
            detail=f"Error communicating with chatbot service: {str(e)}"
        )
    except Exception as e:
        logger.error(f"[CHATBOT] Unexpected error: {str(e)}")
        logger.error(f"[CHATBOT] Error type: {type(e).__name__}")
        import traceback
        logger.error(f"[CHATBOT] Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
