"""
Guardian FastAPI Main Application
Fraud detection REST API
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .config import settings
from .database import init_db, check_db_connection
from .cache import cache
from .schemas import HealthResponse
from .routers import predict_router, explain_router, metrics_router, explainability_router, network_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ===== Lifespan Events =====

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events for startup and shutdown.
    Initialize database and cache at startup.
    """
    # Startup
    logger.info("🚀 Guardian API Starting Up...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Version: {settings.api_version}")
    
    # Initialize database
    try:
        init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
    
    # Check cache connection
    if cache.is_connected():
        logger.info("✅ Redis cache connected")
    else:
        logger.warning("⚠️  Redis cache not available (caching disabled)")
    
    # TODO: Load model after Chat 2 completes
    logger.info("⚠️  Model not loaded (waiting for Chat 2 completion)")
    
    logger.info("✅ API Ready!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Guardian API Shutting Down...")
    logger.info("✅ Cleanup Complete")


# ===== FastAPI Application =====

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
    lifespan=lifespan,
)


# ===== Middleware =====

# CORS Middleware
if settings.cors_enabled:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info(f"CORS enabled for origins: {settings.cors_origins}")


# Request ID Middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add unique request ID to each request for tracking"""
    import uuid
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id
    
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# ===== Exception Handlers =====

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body
        }
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


# ===== Routes =====

@app.get("/", tags=["Root"])
async def root():
    """API root endpoint"""
    return {
        "name": "Guardian Fraud Detection API",
        "version": settings.api_version,
        "status": "operational",
        "docs": "/docs" if settings.debug else None,
        "endpoints": {
            "predict": "/api/v1/predict",
            "predict_batch": "/api/v1/predict/batch",
            "explain": "/api/v1/explain",
            "metrics": "/api/metrics/model-performance",
            "explainability": "/api/explainability/explain",
            "network": "/api/network/fraud-ring/{account_id}",
            "health": "/health"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    Returns service status and component health.
    """
    db_connected = check_db_connection()
    redis_connected = cache.is_connected()
    
    # TODO: Check model loaded status after Chat 2 completes
    model_loaded = False  # Placeholder until Chat 2
    
    status_str = "healthy" if (db_connected or not settings.debug) else "degraded"
    
    return HealthResponse(
        status=status_str,
        version=settings.api_version,
        model_loaded=model_loaded,
        database_connected=db_connected,
        redis_connected=redis_connected
    )


# Include routers
app.include_router(predict_router, prefix="/api/v1", tags=["Prediction"])
app.include_router(explain_router, prefix="/api/v1", tags=["Explainability"])
app.include_router(metrics_router, tags=["Metrics"])
app.include_router(explainability_router, tags=["Explainability"])
app.include_router(network_router, tags=["Network"])


# ===== Main Entry Point =====

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )

