from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import status
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep, IsUserLoggedIn, get_current_user, is_admin
from app.models.user import User
from . import router, templates
from datetime import datetime
from app.models.userbudget import UserBudget
from app.services.user_budget_service import UserBudgetService
from app.repositories.userbudget import UserBudgetRepository
from app.schemas.budget_schema import BudgetCreate

@router.get("/app", response_class=HTMLResponse)
async def user_home_view(
    request: Request,
    user: AuthDep,
    db:SessionDep
):
    repo = UserBudgetRepository(db)
    service = UserBudgetService(repo)
    budget = service.get_budget_for_user(user.id)
    
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

@router.post("/budgets/create")
async def save_budget(budget: BudgetCreate, db:SessionDep, current_user: User = Depends(get_current_user)):

    budget_data = budget.model_dump()
    budget_data["user_id"] = current_user.id

    repo = UserBudgetRepository(db)
    service = UserBudgetService(repo)
    new_budget = service.create_user_budget(budget_data)

    return {
        "message": "Budget saved successfully",
        "budget": new_budget
    }