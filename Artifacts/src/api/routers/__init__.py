"""API routers"""

from .predict import router as predict_router
from .explain import router as explain_router
from .metrics import router as metrics_router
from .explainability import router as explainability_router
from .network import router as network_router

__all__ = ["predict_router", "explain_router", "metrics_router", "explainability_router", "network_router"]

