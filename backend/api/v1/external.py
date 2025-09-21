"""
External API Routes - PDF Generation using API Keys
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
import models
import schemas
from core.database import get_db
from api.dependencies import get_user_from_api_key
from features.pdf_generation.services.playwright_manager import PlaywrightManager
import io

router = APIRouter()

@router.post("/generate-pdf")
async def generate_pdf_external(
    pdf_request: schemas.PDFRequest,
    user: models.User = Depends(get_user_from_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate PDF using API key authentication
    This endpoint can be used by external applications with a valid API key
    """
    try:
        # Get the template if template_id is provided
        template = None
        if pdf_request.template_id:
            result = await db.execute(
                select(models.Template)
                .where(models.Template.id == pdf_request.template_id)
                .where(models.Template.user_id == user.id)
            )
            template = result.scalars().first()
            
            if not template:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Template not found"
                )
        
        # Use template content if available, otherwise use provided content
        content = template.content if template else pdf_request.content
        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No content provided for PDF generation"
            )
        
        # Determine the engine type
        engine = template.engine if template else "html"
        if pdf_request.is_jsx:
            engine = "jsx"
        elif pdf_request.is_vue:
            engine = "vue"
        
        # Use template data if available, otherwise use provided data
        data = template.data if template else pdf_request.data
        
        # Generate PDF using Playwright
        playwright_manager = await PlaywrightManager.get_instance()
        pdf_bytes = await playwright_manager.generate_pdf(
            content=content,
            engine=engine,
            data=data
        )
        
        # Create a streaming response
        pdf_stream = io.BytesIO(pdf_bytes)
        
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=generated.pdf",
                "Content-Length": str(len(pdf_bytes))
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PDF generation failed: {str(e)}"
        )

@router.get("/templates")
async def list_templates_external(
    user: models.User = Depends(get_user_from_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    List all templates for the authenticated user via API key
    """
    result = await db.execute(
        select(models.Template)
        .where(models.Template.user_id == user.id)
        .order_by(models.Template.created_at.desc())
    )
    templates = result.scalars().all()
    
    return [schemas.Template.model_validate(template) for template in templates]

@router.get("/templates/{template_id}")
async def get_template_external(
    template_id: str,
    user: models.User = Depends(get_user_from_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific template by ID via API key
    """
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
    
    return schemas.Template.model_validate(template)
