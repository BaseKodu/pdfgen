from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db
from auth import current_active_user, get_user_manager
from pydantic import BaseModel
from utils.playwright_manager import PlaywrightManager
from nanoid import generate

# Create router
router = APIRouter()



# Protected route example - get current user info
@router.get("/me", response_model=schemas.UserRead)
def get_current_user(user: models.User = Depends(current_active_user)):
    return user



@router.get("/templates", response_model=List[schemas.Template], status_code=status.HTTP_200_OK)
async def get_user_templates(
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_active_user)
    ):
    
    try:
        result = await db.execute(
            select(models.Template)
            .where(models.Template.user_id == user.id)
            )
        templates = result.scalars().all()
        return templates
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/templates", response_model=schemas.TemplateCreate, status_code=status.HTTP_201_CREATED)
async def create_new_template(
    template_data: schemas.TemplateCreate,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_active_user),
    ):
    
    try:
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
    
@router.get("/templates/{id}", response_model=schemas.Template)
async def get_template(
    id: str,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_active_user)
):
    result = await db.execute(
        select(models.Template)
        .where(models.Template.id == id)
        .where(models.Template.user_id == user.id)
    )
    template = result.scalars().first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )

    return template


@router.patch("/templates/{id}", response_model=schemas.Template)
async def update_template(
    id: str,
    template_update: schemas.TemplateUpdate,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_active_user)
):
    
    result = await db.execute(
        select(models.Template)
        .where(models.Template.id == id)
        .where(models.Template.user_id == user.id)
    )
    template = result.scalars().first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found or you don't have permission"
        )



    # 2. Apply only allowed updates
    if template_update.content is not None:
        template.content = template_update.content
    if template_update.data is not None:
        template.data = template_update.data

    # 3. Save changes
    try:
        await db.commit()
        await db.refresh(template)
        return template
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating template: {str(e)}"
        )
    


@router.post("/generate-pdf", response_model=schemas.PDFRequest)
async def generate_pdf(
    pdf_request: schemas.PDFRequest,
    db: AsyncSession = Depends(get_db)  # Add database dependency
):
    try:
        if pdf_request.template_id:
            # Query the template directly instead of using the route handler
            result = await db.execute(
                select(models.Template)
                .where(models.Template.id == pdf_request.template_id)
            )
            template = result.scalars().first()
            
            if not template:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Template not found"
                )
                
            pdf_request.content = template.content
            pdf_request.is_jsx = template.engine == schemas.TemplatingEngineEnum.JSX
            pdf_request.data = template.data

        playwright_manager = await PlaywrightManager.get_instance()
        pdf_bytes = await playwright_manager.generate_pdf(
            content=pdf_request.content,
            context=pdf_request.data,
            is_jsx=pdf_request.is_jsx
        )
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=generated.pdf"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/guest", response_model=schemas.GuestUserResponse)
async def create_guest_user(
    db: AsyncSession = Depends(get_db),
    user_manager = Depends(get_user_manager)
):
    try:
        # Generate a unique guest email
        guest_email = f"guest_{generate(size=10)}@guest.com"
        # Create a random password
        guest_password = generate(size=20)
        
        # Create guest user using UserCreate schema
        guest_user = await user_manager.create(
            schemas.UserCreate(
                email=guest_email,
                password=guest_password,
                is_active=True
            )
        )
        
        # Set is_guest flag after creation
        guest_user.is_guest = True
        await db.commit()
        await db.refresh(guest_user)
        
        # Create response with password
        response = schemas.GuestUserResponse(
            id=guest_user.id,
            email=guest_user.email,
            password=guest_password,  # Include the original password
            is_active=guest_user.is_active,
            is_guest=guest_user.is_guest,
            created_at=guest_user.created_at,
            updated_at=guest_user.updated_at
        )
        
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating guest user: {str(e)}"
        ) 