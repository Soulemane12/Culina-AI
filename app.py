import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import uuid
from upload_app import save_files  # For handling file uploads
from vision import process_images  # For processing images and extracting data
from ingredient_processor import extract_ingredient_names  # For refining ingredients
from recipe import generate_recipe  # For generating the recipe
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_and_process():
    try:
        print("Received request to upload files.")
        
        # Get all files from the request
        files = request.files.getlist('files')
        print(f"Number of files received: {len(files)}")
        
        if not files or len(files) == 0:
            return jsonify({"error": "No files uploaded"}), 400

        # Save files
        uploaded_paths = save_files(files, app.config['UPLOAD_FOLDER'], allowed_file)
        print(f"Uploaded file paths: {uploaded_paths}")
        
        if not uploaded_paths:
            return jsonify({"error": "No valid files were uploaded"}), 400
        
        # Process each file
        all_ingredients = []
        for idx, file_path in enumerate(uploaded_paths):
            print(f"Processing file {idx + 1}: {file_path}")
            try:
                processed_data = process_images([file_path])
                print(f"Processed data for {file_path}: {processed_data}")
                
                refined_ingredients = extract_ingredient_names(processed_data)
                print(f"Refined ingredients for {file_path}: {refined_ingredients}")
                
                all_ingredients.extend(refined_ingredients)
                os.remove(file_path)
                print(f"File {file_path} processed and removed.")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        # Ensure at least one ingredient was extracted
        if not all_ingredients:
            return jsonify({"error": "No valid ingredients extracted"}), 400
        
        # Generate recipe
        unique_ingredients = list(set(all_ingredients))
        print(f"Final unique ingredients: {unique_ingredients}")
        
        recipe = generate_recipe(
            unique_ingredients,
            dietary_preference=request.form.get('dietary_preference'),
            health_goal=request.form.get('health_goal'),
            allergies=request.form.get('allergies'),
            cooking_skill=request.form.get('cooking_skill', 'beginner')
        )
        
        return jsonify({"success": True, "recipe": recipe})

    except Exception as e:
        print(f"Error during file upload and processing: {e}")
        return jsonify({"error": str(e)}), 500





if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(host='0.0.0.0', port=5000, debug=True)