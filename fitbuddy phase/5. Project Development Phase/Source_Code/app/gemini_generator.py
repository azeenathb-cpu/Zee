import os
from dotenv import load_dotenv

load_dotenv()


def generate_workout_gemini(
    goal: str,
    intensity: str
):

    api_key = os.getenv("GOOGLE_API_KEY")

    prompt = f"""
Create a personalized 7-day workout plan.

Fitness Goal: {goal}
Workout Intensity: {intensity}

Give the plan in this format:

Day 1:
Warm-up:
Main Workout:
Sets/Reps:
Rest:
Cool-down:

Day 2:
Warm-up:
Main Workout:
Sets/Reps:
Rest:
Cool-down:

Continue until Day 7.

Include suitable recovery/rest days.
Keep the plan simple and easy to understand.
"""

    # If API key is not available, return a demo plan
    if not api_key:
        return create_demo_plan(goal, intensity)

    try:

        from google import genai

        client = genai.Client(
            api_key=api_key
        )

        model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        )

        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )

        if response.text:
            return response.text

        return create_demo_plan(goal, intensity)

    except Exception as e:

        print("Gemini error:", e)

        return create_demo_plan(goal, intensity)


def create_demo_plan(goal, intensity):

    return f"""
FITBUDDY 7-DAY WORKOUT PLAN

Goal: {goal}
Intensity: {intensity}

Day 1 - Full Body
Warm-up: 5-10 minutes walking
Main Workout:
- Squats - 3 sets x 10 reps
- Wall Push-ups - 3 sets x 10 reps
- Glute Bridge - 3 sets x 12 reps
Rest: 45-60 seconds
Cool-down: 5 minutes stretching

Day 2 - Cardio
Warm-up: 5 minutes
Main Workout:
- Brisk Walking - 20 minutes
- Step-ups - 3 sets x 10 reps
Rest: 45 seconds
Cool-down: 5 minutes

Day 3 - Upper Body
Warm-up: 5 minutes
Main Workout:
- Wall Push-ups - 3 x 10
- Arm Circles - 3 x 15
- Light Dumbbell Rows - 3 x 10
Rest: 45-60 seconds
Cool-down: 5 minutes

Day 4 - Recovery
- Light walking
- Gentle stretching
- Rest and hydration

Day 5 - Lower Body
Warm-up: 5-10 minutes
Main Workout:
- Squats - 3 x 10
- Lunges - 3 x 8 each leg
- Glute Bridge - 3 x 12
Rest: 60 seconds
Cool-down: 5 minutes

Day 6 - Cardio + Core
Warm-up: 5 minutes
Main Workout:
- Brisk Walking - 20 minutes
- Plank - 3 x 20 seconds
- Bird Dog - 3 x 10
Rest: 45-60 seconds
Cool-down: 5 minutes

Day 7 - Recovery
- Easy walking
- Full-body stretching
- Relax and recover
"""