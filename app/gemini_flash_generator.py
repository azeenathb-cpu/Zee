import os
from dotenv import load_dotenv

load_dotenv()


def generate_nutrition_tip_with_flash(
    goal: str
):

    api_key = os.getenv("GOOGLE_API_KEY")

    prompt = f"""
Give one short and practical nutrition or recovery tip
for a person whose fitness goal is {goal}.

Keep it simple and safe.
"""

    if not api_key:
        return (
            "Stay hydrated throughout the day and include "
            "balanced meals with vegetables, fruits, whole grains "
            "and a suitable protein source."
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

        return "Stay hydrated and eat balanced meals."

    except Exception as e:

        print("Gemini nutrition error:", e)

        return (
            "Stay hydrated and eat balanced meals with "
            "vegetables, fruits and a suitable protein source."
        )