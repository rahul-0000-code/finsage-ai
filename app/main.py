from fastapi import FastAPI
from app.api.v1 import auth, user, documents, advisor, logs, admin, health

app = FastAPI(title="FinSage AI", version="1.0.0")

# Routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(advisor.router, prefix="/advisor", tags=["advisor"])
app.include_router(logs.router, prefix="/logs", tags=["logs"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(health.router, prefix="/healthcheck", tags=["healthcheck"])
