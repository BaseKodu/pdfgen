from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import routes
from auth import auth_backend, fastapi_users
from schemas import UserCreate, UserRead, UserUpdate

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
    allow_origins=["*"],  # Configure this properly for production
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

# Include application routes
app.include_router(routes.router, prefix="/api/v1", tags=["templates"])

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