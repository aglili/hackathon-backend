from app.routers.user_authentication import router as user_auth_router
from app.routers.transactions import router as transactions_router

V1_ROUTES = [user_auth_router, transactions_router]
