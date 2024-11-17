import base64
import os
import json
import re
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def encode_image(image_path):
    print(f"Encoding image: {image_path}")
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode('utf-8')
    print(f"Encoded image for {image_path}")
    return encoded

def extract_json(raw_response):
    try:
        # Use regex to extract JSON block from the response
        match = re.search(r"\{.*\}", raw_response, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            raise ValueError("No valid JSON found in the response.")
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        raise

def process_images(image_paths, output_folder="processed_data"):
    os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists
    print(f"Processing images: {image_paths}")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    output_files = []

    for image_path in image_paths:
        try:
            print(f"Processing image at {image_path}")
            base64_img = f"data:image/{image_path.rsplit('.', 1)[1].lower()};base64,{encode_image(image_path)}"
            
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": (
                                "Analyze the following image carefully. Identify all visible ingredients and "
                                "provide a detailed JSON document listing each ingredient with its name and type (e.g., "
                                "vegetable, fruit, protein, spice, etc.). If possible, include additional metadata like "
                                "approximate quantity or form (e.g., chopped, whole, liquid). Ensure no ingredient is missed."
                            )},
                            {"type": "image_url", "image_url": {"url": base64_img}}
                        ]
                    }
                ],
                max_tokens=750,
            )

            raw_response = response.choices[0].message.content.strip()
            print(f"Raw JSON response for {image_path}: {raw_response}")
            
            # Extract valid JSON data
            json_data = extract_json(raw_response)
            filename = os.path.splitext(os.path.basename(image_path))[0]
            output_file = os.path.join(output_folder, f"{filename}_data.json")
            
            with open(output_file, 'w') as file:
                json.dump(json_data, file, indent=4)
            print(f"Processed data saved to {output_file}")

            output_files.append(output_file)

        except (OpenAIError, ValueError) as e:
            print(f"Error processing {image_path}: {e}")
            continue

    print(f"All processed files: {output_files}")
    return output_files
def process_images(image_paths, output_folder="processed_data"):
    os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists
    print(f"Processing images: {image_paths}")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    output_files = []

    for image_path in image_paths:
        try:
            print(f"Processing image at {image_path}")
            base64_img = f"data:image/{image_path.rsplit('.', 1)[1].lower()};base64,{encode_image(image_path)}"
            
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": (
                                "Analyze the following image carefully. Identify all visible ingredients and "
                                "provide a detailed JSON document listing each ingredient with its name and type (e.g., "
                                "vegetable, fruit, protein, spice, etc.). If possible, include additional metadata like "
                                "approximate quantity or form (e.g., chopped, whole, liquid). Ensure no ingredient is missed."
                            )},
                            {"type": "image_url", "image_url": {"url": base64_img}}
                        ]
                    }
                ],
                max_tokens=750,
            )

            raw_response = response.choices[0].message.content.strip()
            print(f"Raw JSON response for {image_path}: {raw_response}")
            
            # Extract valid JSON data
            json_data = extract_json(raw_response)
            filename = os.path.splitext(os.path.basename(image_path))[0]
            output_file = os.path.join(output_folder, f"{filename}_data.json")
            
            with open(output_file, 'w') as file:
                json.dump(json_data, file, indent=4)
            print(f"Processed data saved to {output_file}")

            output_files.append(output_file)

        except (OpenAIError, ValueError) as e:
            print(f"Error processing {image_path}: {e}")
            continue

    print(f"All processed files: {output_files}")
    return output_files
