import os
from dotenv import load_dotenv

load_dotenv()


def update_workout_plan(
    original_plan,
    feedback,
    goal,
    intensity
):

    prompt = f"""
Update the following workout plan based on the user's feedback.

Fitness Goal: {goal}
Workout Intensity: {intensity}

Original Workout Plan:
{original_plan}

User Feedback:
{feedback}

Create a revised 7-day workout plan.
Keep the useful parts of the original plan.
Apply the user's feedback where appropriate.
Keep it simple and easy to understand.
"""

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        return (
            original_plan
            + "\n\nUPDATED BASED ON FEEDBACK:\n"
            + feedback
        )

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

        return original_plan

    except Exception as e:

        print("Gemini update error:", e)

        return (
            original_plan
            + "\n\nUPDATED BASED ON FEEDBACK:\n"
            + feedback
        )