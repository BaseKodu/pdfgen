from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.auth import auth_backend, fastapi_users
from core.config import ALLOWED_ORIGINS
from schemas import UserCreate, UserRead, UserUpdate
from features.pdf_generation.services.playwright_manager import PlaywrightManager

# Import API routes
from api.v1 import templates, api_keys, external
from features.oauth import oauth_router

# Create FastAPI instance
app = FastAPI(
    title="pdfGen api",
    description="The api for the pdfGen application",
    version="1.0.0"
)

#---------------------------------------start middleware--------------------------------------------

from fastapi import Request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_event():
    playwright_manager = await PlaywrightManager.get_instance()
    await playwright_manager.cleanup() 

#@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    logger.info(f"Headers: {request.headers}")
    
    if request.method == "POST" and ("auth/jwt/login" in str(request.url) or "auth/register" in str(request.url)):
        body = await request.body()
        logger.info(f"Raw body: {body.decode()}")  # Log raw request body
    
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

#--------------------------------end middleware------------------------------------------------------------------------

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend), 
    prefix="/api/v1/auth/jwt", 
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/v1/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/api/v1/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/api/v1/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/api/v1/users",
    tags=["users"],
)

# Include OAuth routes
app.include_router(oauth_router, prefix="/api/v1/auth", tags=["oauth"])

# Include API routes
app.include_router(templates.router, prefix="/api/v1", tags=["templates"])
app.include_router(api_keys.router, prefix="/api/v1", tags=["api-keys"])
app.include_router(external.router, prefix="/api/v1/external", tags=["external"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Boilerplate with Authentication!"}

# Health check endpoint
@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)