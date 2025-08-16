from .auth import auth_router
from .root import root_router
from .loan_management import loan_router
from .records import record_router
from .utils import utils_router

__all__ = ["auth_router", "root_router", "loan_router", "record_router", "utils_router"]
