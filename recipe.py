import os
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_recipe(ingredient_names, dietary_preference=None, health_goal=None, allergies=None, cooking_skill=None):
    try:
        print(f"Generating recipe with ingredients: {ingredient_names}")

        ingredients_str = ", ".join(ingredient_names)
        
        # Build prompt with combined ingredients
        prompt_parts = [
            f"Create a recipe that uses only the following ingredients you can add seasonings and condiments nothing else  : {ingredients_str}.",
            f"This recipe should align with the dietary preference: {dietary_preference}." if dietary_preference else "",
            f"It should also consider the health goal: {health_goal}." if health_goal else "",
            f"Ensure the recipe avoids these allergies: {allergies}." if allergies else "",
            f"The recipe should be suitable for a {cooking_skill} level cook." if cooking_skill else ""
        ]
        
        prompt = " ".join(part for part in prompt_parts if part)
        print(f"Generated prompt for OpenAI: {prompt}")

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7,
        )
        recipe = response.choices[0].message.content.strip()
        print(f"Generated recipe content: {recipe}")
        return recipe

    except OpenAIError as e:
        print(f"Error generating recipe: {e}")
        return "Sorry, there was an error generating your recipe. Please try again later."
