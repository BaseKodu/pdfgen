from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
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



@router.get("/templates", response_model=List[schemas.Template], status_code=status.HTTP_200_OK)
async def get_user_templates(
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_active_user)):
    
    try:
        result = await db.execute(select(models.Template).where(models.Template.user_id == user.id))
        templates = result.scalars().all()
        return templates
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/templates", response_model=schemas.TemplateCreate, status_code=status.HTTP_201_CREATED)
async def create_new_template(
    template_data: schemas.TemplateCreate,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_active_user)):
    
    try:
        # The enum conversion is already handled by Pydantic in template_data!
        # No need to manually convert it again
        new_template = models.Template(
            **template_data.model_dump(),
            user_id=user.id
        )

        db.add(new_template)
        await db.commit()
        await db.refresh(new_template)
        return new_template
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error creating template: {str(e)}"
        )
