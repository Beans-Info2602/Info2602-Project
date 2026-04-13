from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, status, Form
from app.dependencies import SessionDep
from . import router, templates
from app.services.auth_service import AuthService
from app.repositories.user import UserRepository
from app.utilities.flash import flash
from app.config import get_settings

@router.get("/landing", response_class=HTMLResponse)
async def landing_view(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="landing.html",
    )