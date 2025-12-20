"""
Dashboard CRM API - FastAPI Application
Main entry point for the backend API server.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes.dashboard import router as dashboard_router
from routes.chatbot import router as chatbot_router
from config import settings
import logging
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Dashboard CRM API",
    description="REST API for CRM Dashboard - Integração com Databricks",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dashboard_router)
app.include_router(chatbot_router)

# Serve static files (frontend build)
# Look for frontend/dist relative to backend directory
BACKEND_DIR = Path(__file__).parent
FRONTEND_DIST = BACKEND_DIR.parent / "frontend" / "dist"

if FRONTEND_DIST.exists():
    logger.info(f"Serving frontend from: {FRONTEND_DIST}")

    # Mount static assets (JS, CSS, etc)
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="assets")

    # Serve index.html for all non-API routes (SPA fallback)
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve frontend for all non-API routes."""
        # If path starts with /api or /docs, let FastAPI handle it
        if full_path.startswith(("api/", "docs", "redoc")):
            return {"error": "Not found"}

        # Serve index.html for all other routes
        return FileResponse(str(FRONTEND_DIST / "index.html"))
else:
    logger.warning(f"Frontend dist folder not found at: {FRONTEND_DIST}")
    logger.warning("API-only mode. Frontend must be served separately.")

    @app.get("/")
    async def root():
        """Root endpoint (API-only mode)."""
        return {
            "service": "Dashboard CRM API",
            "version": "1.0.0",
            "status": "running",
            "mode": "API-only",
            "docs": "/docs",
            "health": "/api/health"
        }


@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    logger.info("=" * 60)
    logger.info("Dashboard CRM API - Starting")
    logger.info(f"Databricks Host: {settings.databricks_host}")
    logger.info(f"Frontend URL: {settings.frontend_url}")
    logger.info(f"API will be available at: http://{settings.api_host}:{settings.api_port}")
    logger.info(f"API Documentation: http://{settings.api_host}:{settings.api_port}/docs")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    logger.info("Dashboard CRM API - Shutting down")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level="info"
    )
