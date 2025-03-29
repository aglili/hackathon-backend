from app.routers.user_authentication import router as user_auth_router
from app.routers.transactions import router as transactions_router
from app.routers.transactions import dashboard_router as transactions_dashboard_router
from app.routers.uploads import router as uploads_router

V1_ROUTES = [user_auth_router, transactions_router, transactions_dashboard_router, uploads_router]
