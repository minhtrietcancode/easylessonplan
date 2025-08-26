# app.py - Your Flask Backend
from flask import Flask, request, jsonify, render_template_string
from file_handler.FileHandler import FileHandler
import os

# Create Flask app instance
app = Flask(__name__)
fh = FileHandler()  # Your existing file handler

# Configure upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# HTML Frontend (normally this would be a separate file)
FRONTEND_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>File Processor</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; }
        .upload-area { border: 2px dashed #ccc; padding: 20px; text-align: center; margin: 20px 0; }
        .result { background: #f0f0f0; padding: 10px; margin: 10px 0; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>Document Text Extractor</h1>
    
    <div class="upload-area">
        <form id="uploadForm" enctype="multipart/form-data">
            <input type="file" id="fileInput" accept=".pdf,.docx" required>
            <br><br>
            <button type="submit">Extract Text</button>
        </form>
    </div>
    
    <div id="result"></div>
    
    <script>
        // Frontend JavaScript
        document.getElementById('uploadForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const fileInput = document.getElementById('fileInput');
            const resultDiv = document.getElementById('result');
            
            if (!fileInput.files[0]) {
                alert('Please select a file');
                return;
            }
            
            // Prepare form data
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            
            resultDiv.innerHTML = 'Processing...';
            
            try {
                // Send request to Flask backend
                const response = await fetch('/api/extract-text', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Display extracted text
                    let html = '<h3>Extracted Text:</h3>';
                    for (const [page, text] of Object.entries(data.extracted_text)) {
                        html += `<div class="result"><strong>Page ${page}:</strong><br>${text}</div>`;
                    }
                    resultDiv.innerHTML = html;
                } else {
                    resultDiv.innerHTML = `<div style="color: red;">Error: ${data.error}</div>`;
                }
            } catch (error) {
                resultDiv.innerHTML = `<div style="color: red;">Network error: ${error.message}</div>`;
            }
        });
    </script>
</body>
</html>
"""

# ROUTE 1: Serve the Frontend Page
@app.route('/')
def home():
    """Serves the HTML frontend page"""
    return render_template_string(FRONTEND_HTML)

# ROUTE 2: API Endpoint for File Processing
@app.route('/api/extract-text', methods=['POST'])
def extract_text():
    """Handles file upload and text extraction"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'})
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        # Save uploaded file temporarily
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Use your FileHandler to extract text
        extracted_text = fh.extractText(file_path)
        
        # Clean up: delete temporary file
        os.remove(file_path)
        
        # Return success response
        return jsonify({
            'success': True,
            'filename': file.filename,
            'extracted_text': extracted_text
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ROUTE 3: Health Check
@app.route('/api/health')
def health():
    """Simple health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Backend is running!'})

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    print("📝 Frontend available at: http://localhost:5000")
    print("🔧 API available at: http://localhost:5000/api/extract-text")
    app.run(host='0.0.0.0', port=5000, debug=True)