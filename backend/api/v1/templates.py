"""
Template management API routes
"""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from core.database import get_db
from core.auth import current_active_user, get_user_manager
from pydantic import BaseModel
from features.pdf_generation.services.playwright_manager import PlaywrightManager
from nanoid import generate

# Create router
router = APIRouter()

# Protected route example - get current user info
@router.get("/me", response_model=schemas.UserRead)
async def get_current_user(
    user: models.User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Reload user with relationships to avoid async context issues
    from sqlalchemy.orm import selectinload
    result = await db.execute(
        select(models.User)
        .options(selectinload(models.User.oauth_accounts))
        .options(selectinload(models.User.api_keys))
        .where(models.User.id == user.id)
    )
    user_with_relationships = result.scalars().first()
    return user_with_relationships

@router.get("/templates", response_model=List[schemas.Template], status_code=status.HTTP_200_OK)
async def get_user_templates(
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_active_user)
    ):
    """Get all templates for the authenticated user"""
    result = await db.execute(
        select(models.Template).where(models.Template.user_id == user.id)
    )
    templates = result.scalars().all()
    return templates

@router.post("/templates", response_model=schemas.Template, status_code=status.HTTP_201_CREATED)
async def create_template(
    template_data: schemas.TemplateCreate,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_active_user)
):
    """Create a new template"""
    # Generate unique ID
    template_id = generate(size=10)
    
    # Create template
    template = models.Template(
        id=template_id,
        name=template_data.name,
        engine=template_data.engine,
        content=template_data.content,
        data=template_data.data,
        user_id=user.id
    )
    
    db.add(template)
    await db.commit()
    await db.refresh(template)
    
    return template

@router.get("/templates/{template_id}", response_model=schemas.Template)
async def get_template(
    template_id: str,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_active_user)
):
    """Get a specific template by ID"""
    result = await db.execute(
        select(models.Template)
        .where(models.Template.id == template_id)
        .where(models.Template.user_id == user.id)
    )
    template = result.scalars().first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    return template

@router.put("/templates/{template_id}", response_model=schemas.Template)
async def update_template(
    template_id: str,
    template_update: schemas.TemplateUpdate,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_active_user)
):
    """Update a template"""
    result = await db.execute(
        select(models.Template)
        .where(models.Template.id == template_id)
        .where(models.Template.user_id == user.id)
    )
    template = result.scalars().first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Update fields
    if template_update.content is not None:
        template.content = template_update.content
    if template_update.data is not None:
        template.data = template_update.data
    
    await db.commit()
    await db.refresh(template)
    
    return template

@router.delete("/templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(
    template_id: str,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_active_user)
):
    """Delete a template"""
    result = await db.execute(
        select(models.Template)
        .where(models.Template.id == template_id)
        .where(models.Template.user_id == user.id)
    )
    template = result.scalars().first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    await db.delete(template)
    await db.commit()
    
    return None

@router.post("/templates/{template_id}/generate", response_class=Response)
async def generate_pdf(
    template_id: str,
    pdf_request: schemas.PDFRequest,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_active_user)
):
    """Generate PDF from template"""
    # Get template
    result = await db.execute(
        select(models.Template)
        .where(models.Template.id == template_id)
        .where(models.Template.user_id == user.id)
    )
    template = result.scalars().first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Use template data or provided data
    data = pdf_request.data if pdf_request.data else template.data
    
    # Generate PDF
    playwright_manager = await PlaywrightManager.get_instance()
    pdf_bytes = await playwright_manager.generate_pdf(
        content=template.content,
        engine=template.engine,
        data=data
    )
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={template.name}.pdf"}
    )

@router.post("/generate-pdf", response_class=Response)
async def generate_pdf_from_content(
    pdf_request: schemas.PDFRequest,
    user: models.User = Depends(current_active_user)
):
    """Generate PDF from raw content"""
    if not pdf_request.content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content is required"
        )
    
    # Determine engine
    engine = "html"
    if pdf_request.is_jsx:
        engine = "jsx"
    elif pdf_request.is_vue:
        engine = "vue"
    
    # Generate PDF
    playwright_manager = await PlaywrightManager.get_instance()
    pdf_bytes = await playwright_manager.generate_pdf(
        content=pdf_request.content,
        engine=engine,
        data=pdf_request.data
    )
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=generated.pdf"}
    )

@router.post("/guest", response_model=schemas.GuestUserResponse, status_code=status.HTTP_201_CREATED)
async def create_guest_user(
    db: AsyncSession = Depends(get_db),
    user_manager = Depends(get_user_manager)
):
    """Create a guest user for temporary access"""
    import secrets
    import string
    
    # Generate random guest credentials
    guest_id = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    guest_email = f"guest_{guest_id}@pdfgen.com"
    guest_password = secrets.token_urlsafe(12)
    
    # Create guest user using the user manager to properly hash the password
    from schemas import UserCreate
    
    guest_user_create = UserCreate(
        email=guest_email,
        password=guest_password
    )
    
    guest_user = await user_manager.create(guest_user_create)
    
    # Update the guest user with additional fields
    guest_user.is_guest = True
    await db.commit()
    await db.refresh(guest_user)
    
    return schemas.GuestUserResponse(
        id=guest_user.id,
        email=guest_user.email,
        password=guest_password,  # Return plain password for guest
        is_active=guest_user.is_active,
        is_guest=guest_user.is_guest,
        created_at=guest_user.created_at,
        updated_at=guest_user.updated_at
    )
