"""
Dashboard CRM API - FastAPI Application
Main entry point for the backend API server.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.dashboard import router as dashboard_router
from config import settings
import logging

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


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Dashboard CRM API",
        "version": "1.0.0",
        "status": "running",
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
