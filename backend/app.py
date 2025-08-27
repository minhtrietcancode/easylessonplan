from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from backend.os_handler.OsHandler import OsHandler
import shutil

app = Flask(__name__,
            static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..\', '..\', 'frontend', 'static')),
            template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..\', '..\', 'frontend', 'template')))
CORS(app)  # Enable CORS for all routes

os_handler = OsHandler()

@app.route('/')
def index():
    return send_from_directory(app.template_folder, 'easylesson.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

def _build_directory_tree(path, base_path):
    tree = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            tree.append({
                "name": item,
                "path": os.path.relpath(item_path, base_path),
                "type": "folder",
                "children": _build_directory_tree(item_path, base_path)
            })
        else:
            tree.append({
                "name": item,
                "path": os.path.relpath(item_path, base_path),
                "type": "file"
            })
    return tree

@app.route('/api/directory-tree', methods=['GET'])
def get_directory_tree():
    easy_lesson_path = os_handler.get_easy_lesson_path()
    
    # Ensure the base directory exists
    if not os.path.exists(easy_lesson_path):
        success, message, path = os_handler.makeEasyLessonDir()
        if not success:
            return jsonify({"success": False, "message": message}), 500
    
    tree = _build_directory_tree(easy_lesson_path, easy_lesson_path)
    return jsonify({"success": True, "tree": tree, "path": easy_lesson_path})

@app.route('/api/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"}), 400
    
    parent_folder = request.form.get('parent_folder', os_handler.get_easy_lesson_path())
    
    # Save the file temporarily
    temp_dir = os.path.join(os_handler.get_easy_lesson_path(), "temp_uploads")
    os.makedirs(temp_dir, exist_ok=True)
    temp_filepath = os.path.join(temp_dir, file.filename)
    file.save(temp_filepath)
    
    success, message, new_file_path = os_handler.copy_file_to(temp_filepath, parent_folder)
    
    # Clean up temporary file
    os.remove(temp_filepath)
    
    if success:
        return jsonify({"success": True, "message": message, "path": new_file_path})
    else:
        return jsonify({"success": False, "message": message}), 500

@app.route('/api/upload-folder', methods=['POST'])
def upload_folder():
    parent_folder = request.form.get('parent_folder', os_handler.get_easy_lesson_path())
    folder_name = request.form.get('folder_name')
    
    if not folder_name:
        return jsonify({"success": False, "message": "Folder name is required"}), 400

    # Create a temporary directory to reconstruct the folder structure
    temp_upload_dir_base = os.path.join(os_handler.get_easy_lesson_path(), "temp_folder_uploads")
    os.makedirs(temp_upload_dir_base, exist_ok=True)
    temp_upload_dir = os.path.join(temp_upload_dir_base, folder_name)
    os.makedirs(temp_upload_dir, exist_ok=True)

    files = request.files.getlist('files[]')
    
    if not files:
        return jsonify({"success": False, "message": "No files in folder"}), 400

    for file in files:
        if file.filename:
            # Reconstruct the path within the temporary folder
            relative_path = request.form.get(f'paths[{file.name}]') # This needs to be sent from frontend
            if not relative_path:
                 return jsonify({"success": False, "message": f"Relative path not found for file {file.filename}"}), 400

            dest_path = os.path.join(temp_upload_dir, relative_path)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            file.save(dest_path)

    success, message, new_folder_path = os_handler.copy_folder_to(temp_upload_dir, parent_folder)

    # Clean up temporary folder
    shutil.rmtree(temp_upload_dir_base)

    if success:
        return jsonify({"success": True, "message": message, "path": new_folder_path})
    else:
        return jsonify({"success": False, "message": message}), 500

@app.route('/api/create-folder', methods=['POST'])
def create_folder():
    data = request.get_json()
    folder_name = data.get('folder_name')
    parent_folder = data.get('parent_folder', os_handler.get_easy_lesson_path())
    
    if not folder_name:
        return jsonify({"success": False, "message": "Folder name is required"}), 400
        
    success, message, full_path = os_handler.makeDir(folder_name, parent_folder)
    
    if success:
        return jsonify({"success": True, "message": message, "path": full_path})
    else:
        return jsonify({"success": False, "message": message}), 500

@app.route('/api/system-info', methods=['GET'])
def get_system_info():
    info = os_handler.get_system_info()
    return jsonify({"success": True, "info": info})

if __name__ == '__main__':
    app.run(debug=True)
