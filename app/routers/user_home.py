from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import status
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep, IsUserLoggedIn, get_current_user, is_admin
from . import router, templates
from datetime import datetime

@router.get("/app", response_class=HTMLResponse)
async def user_home_view(
    request: Request,
    user: AuthDep,
    db:SessionDep
):
    current_month = datetime.now().strftime("%B")

    return templates.TemplateResponse(
        request=request, 
        name="home.html",
        context={
            "user": user,
            "month": current_month
        }
    )

@router.get("/budget", response_class=HTMLResponse)
def budget_page(request: Request, user: AuthDep, db:SessionDep):
    current_month = datetime.now().strftime("%B")

    return templates.TemplateResponse(
        request=request,
        name="budget.html",
        context={
            "user": user,
            "month": current_month
        }
    )