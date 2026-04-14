from fastapi import APIRouter, HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import status
from typing import Optional
from app.dependencies.session import SessionDep
from app.dependencies.auth import AdminDep, IsUserLoggedIn, get_current_user, is_admin
from app.repositories.user import UserRepository
from app.repositories.userbudget import UserBudgetRepository
from app.schemas import user
from app.services.user_budget_service import UserBudgetService
from app.services.user_service import UserService
from app.utilities.flash import flash
from . import router, templates


@router.get("/admin", response_class=HTMLResponse, name="admin_home_view")
async def admin_home_view(request: Request, user: AdminDep, db: SessionDep):

    user_repo = UserRepository(db)
    user_service = UserService(user_repo)

    budget_repo = UserBudgetRepository(db)
    budget_service = UserBudgetService(budget_repo)

    users = user_service.get_all_regular_users()

    users_with_totals = []

    for table_user in users:

        incomes = budget_service.get_all_incomes_for_budget(table_user.id)
        expenses = budget_service.get_all_expenses_for_budget(table_user.id)

        total_income = sum(income.earnings for income in incomes)
        total_expenses = sum(expense.cost for expense in expenses)

        users_with_totals.append({
            "id": table_user.id,
            "username": table_user.username,
            "creation_date": table_user.creation_date,
            "total_income": total_income,
            "total_expenses": total_expenses
        })

    return templates.TemplateResponse(
        name="admin.html",
        request=request,
        context={
            "user": user,
            "users": users_with_totals
        }
    )

@router.delete("/admin/delete-users")
async def delete_users(
    request: user.DeleteUsersRequest,
    db: SessionDep
):
    repo = UserRepository(db)
    service = UserService(repo)

    for user_id in request.selected_users:
        service.delete_user(user_id)

    return {"message": "Deleted"}
