from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import (
    save_user,
    save_plan,
    update_plan,
    get_original_plan,
    get_user,
    get_all_users,
    get_all_plans
)

from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan


router = APIRouter()

templates = Jinja2Templates(directory="templates")


# HOME
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# GENERATE WORKOUT
@router.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    workout_plan = generate_workout_gemini(
        goal=goal,
        intensity=intensity
    )

    nutrition_tip = generate_nutrition_tip_with_flash(
        goal=goal
    )

    user = save_user(
        user_id=user_id,
        username=username,
        age=age,
        weight=weight,
        fitness_goal=goal,
        workout_intensity=intensity
    )

    save_plan(
        user_id=user_id,
        workout_plan=workout_plan,
        nutrition_tip=nutrition_tip
    )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "user": user,
            "username": username,
            "user_id": user_id,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip,
            "updated_plan": None,
            "message": None
        }
    )


# FEEDBACK
@router.post("/submit-feedback", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...)
):

    user = get_user(user_id)

    if user is None:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "error": "User ID not found."
            }
        )

    original_plan = get_original_plan(user_id)

    if original_plan is None:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "error": "Workout plan not found."
            }
        )

    new_plan = update_workout_plan(
        original_plan,
        feedback,
        user.fitness_goal,
        user.workout_intensity
    )

    update_plan(
        user_id=user_id,
        updated_plan=new_plan
    )

    nutrition_tip = generate_nutrition_tip_with_flash(
        goal=user.fitness_goal
    )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "user": user,
            "username": user.username,
            "user_id": user.user_id,
            "age": user.age,
            "weight": user.weight,
            "goal": user.fitness_goal,
            "intensity": user.workout_intensity,
            "workout_plan": original_plan,
            "updated_plan": new_plan,
            "nutrition_tip": nutrition_tip,
            "message": "Your workout plan has been updated successfully!"
        }
    )


# VIEW ALL USERS
@router.get("/view-all-users", response_class=HTMLResponse)
async def view_all_users(request: Request):

    users = get_all_users()
    plans = get_all_plans()

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "request": request,
            "users": users,
            "plans": plans
        }
    )