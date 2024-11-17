import json
import os
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def extract_ingredient_names(input_files, output_file="combined_ingredients.txt"):
    try:
        combined_data = {}
        for file_path in input_files:
            print(f"Loading data from {file_path}")
            with open(file_path, 'r') as file:
                data = json.load(file)
                combined_data.update(data)  # Merge JSON contents

        print(f"Combined data: {combined_data}")

        # Collect ingredient descriptions
        ingredient_descriptions = []
        for item in combined_data.values():
            if isinstance(item, dict):  # If it's a dictionary
                ingredient_descriptions.extend(item.get('ingredients', []))
            elif isinstance(item, list):  # If it's a list of ingredients
                ingredient_descriptions.extend(item)
            else:
                print(f"Unexpected data format in {item}, skipping.")

        raw_text = "\n".join(
            [desc if isinstance(desc, str) else desc.get('name', 'unknown ingredient') for desc in ingredient_descriptions]
        )

        print(f"Raw text for processing: {raw_text}")

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = (
            f"Extract only the ingredient names from the following text :\n\n{raw_text}\n\n"
            "Return the names as a comma-separated list."
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.5,
        )
        result = response.choices[0].message.content.strip()
        print(f"Extracted ingredient names: {result}")

        ingredient_names = [name.strip() for name in result.split(",")]

        with open(output_file, 'w') as f:
            f.write("\n".join(ingredient_names))
        print(f"Refined ingredient names saved to {output_file}.")

        return ingredient_names

    except (OpenAIError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error extracting ingredient names: {e}")
        return []
