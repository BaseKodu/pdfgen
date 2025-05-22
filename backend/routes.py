from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db
from auth import current_active_user

# Create router
router = APIRouter()



# Protected route example - get current user info
@router.get("/me", response_model=schemas.UserRead)
def get_current_user(user: models.User = Depends(current_active_user)):
    return user