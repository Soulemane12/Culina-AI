import os
import uuid
from werkzeug.utils import secure_filename

def save_files(files, upload_folder, allowed_file):
    saved_paths = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            saved_paths.append(filepath)
            print(f"Saved file: {filepath}")
        else:
            print(f"File not allowed or empty: {file.filename}")
    return saved_paths
