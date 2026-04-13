from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import status
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep, IsUserLoggedIn, get_current_user, is_admin
from . import router, templates
from datetime import datetime
from app.models.userbudget import UserBudget
from sqlmodel import select

@router.get("/app", response_class=HTMLResponse)
async def user_home_view(
    request: Request,
    user: AuthDep,
    db:SessionDep
):
    budget = db.exec(select(UserBudget).where(UserBudget.user_id == user.id)).one_or_none()
    
    incomes = budget.income_list if budget else []
    expenses = budget.expense_list if budget else []
    
    recurring = []
    for e in expenses:
        if e.is_recurring:
            recurring.append(e)

    one_time = []
    for e in expenses:
        if not e.is_recurring:
            one_time.append(e)

    total_income = 0
    for i in incomes:
        total_income += i.earnings

    total_recurring = 0
    for e in recurring:
        total_recurring += e.cost

    total_one_time = 0
    for e in one_time:
        total_one_time += e.cost
    
    total_expenses = total_recurring + total_one_time
    remaining_budget = total_income - total_expenses

    current_month = datetime.now().strftime("%B")
    return templates.TemplateResponse(
        request=request, 
        name="user_home.html",
        context={
            "user": user,
            "month": current_month,
            "budget": budget,
            "incomes": incomes,
            "recurring": recurring,
            "one_time": one_time,
            "total_income": total_income, 
            "total_recurring": total_recurring,
            "total_one_time": total_one_time,
            "total_expenses": total_expenses,
            "remaining_budget": remaining_budget
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