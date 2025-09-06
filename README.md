# EasyLesson - Web Application for Teachers

## Overview of the Concepts

EasyLesson is a Flask-based web application designed to empower teachers with an intelligent lesson planning tool. Inspired by the interactive coding assistance of Cursor, this application aims to provide similar AI-powered support, but tailored specifically for educational content creation. Teachers can leverage Large Language Models (LLMs) to generate, refine, and organize lesson plans, making the process more efficient and creative. The application features robust user authentication via Google OAuth and a modular architecture that allows for easy integration of various LLM providers.

## Project Hierarchy Structure

Below is the directory structure of the EasyLesson project, with a brief description of each key component:

```
.
├── app.py                      # Main Flask application entry point and factory.
├── backend/                    # Contains all server-side (Flask) logic.
│   ├── api/                    # Defines concrete API endpoint handlers.
│   │   ├── AuthAPI.py          # Handles authentication-related API endpoints (e.g., login, logout).
│   │   ├── BaseAPI.py          # Provides common utilities and standardized response/error handling for all APIs.
│   │   └── LlmAPI.py           # Handles LLM-related API endpoints (e.g., get models, chat).
│   ├── auth/                   # Manages all authentication-related services and configurations.
│   │   ├── AuthConfig.py       # Configuration settings for Google OAuth and Flask session.
│   │   ├── AuthDecorators.py   # Decorators for protecting routes (e.g., login_required).
│   │   └── AuthService.py      # Core authentication logic (OAuth flow, token verification, session management).
│   ├── llm/                    # Manages Large Language Model integrations.
│   │   ├── all_llm_models/     # Directory containing individual LLM model implementations.
│   │   │   ├── DeepSeek.py     # Implementation for DeepSeek LLM.
│   │   │   ├── Gemma.py        # Implementation for Gemma LLM.
│   │   │   ├── Model.py        # Abstract Base Class (ABC) for all LLM models, defining a common interface.
│   │   │   ├── OpenAI.py       # Implementation for OpenAI LLM.
│   │   │   └── Qwen.py         # Implementation for Qwen LLM.
│   │   ├── LlmConfig.py        # Configuration settings for all LLM models (API keys, URLs, model names).
│   │   └── LlmManager.py       # Orchestrates loading, managing, and invoking LLM models.
│   └── APIRoutes.py            # Centralized file for registering all backend API routes (auth_bp, llm_bp).
├── frontend/                   # Contains all client-side assets and templates.
│   ├── static/                 # Static files served directly to the browser (CSS, JS, images).
│   │   ├── api/                # Client-side API layer for interacting with the backend.
│   │   │   ├── config/         # API configuration.
│   │   │   │   └── routes.js   # Defines frontend API route constants.
│   │   │   ├── core/           # Core API client functionalities.
│   │   │   │   ├── APIClient.js      # Utility for making HTTP requests to backend APIs.
│   │   │   │   ├── APIError.js       # Handles and processes API errors.
│   │   │   │   └── APIManager.js     # Higher-level manager for coordinating API requests/responses.
│   │   │   ├── init.js         # Initializes all frontend API service classes.
│   │   │   └── service/        # Specific client-side functions for interacting with backend services.
│   │   │       ├── auth_api.js # JavaScript functions for client-side auth API interactions.
│   │   │       └── llm_api.js  # JavaScript functions for client-side LLM API interactions.
│   │   ├── pages/              # Page-specific static assets.
│   │   │   ├── easylesson/     # Assets for the lesson planning page.
│   │   │   │   ├── easylesson.css  # CSS for the easylesson page.
│   │   │   │   └── easylesson.js   # JavaScript for the easylesson page interactivity.
│   │   │   └── home/           # Assets for the home page.
│   │   │       ├── home.css        # CSS for the home page.
│   │   │       └── home.js         # JavaScript for the home page interactivity.
│   │   └── images/             # Stores image assets.
│   └── templates/              # HTML templates rendered by Flask.
│       ├── easylesson.html     # HTML template for the main lesson planning interface.
│       └── home.html           # HTML template for the application's home/login page.
├── docker-compose.yml          # Docker Compose configuration for multi-container setup.
├── Dockerfile                  # Dockerfile for building the application image.
├── requirements.txt            # Python dependencies.
└── README.md                   # This README file.
```

> **Visual Overview:**  
> To see the big picture of the workflow, view this diagram:  
>  
> ![Easy Lesson Plan Workflow](Easy%20Lesson%20Plan.png)


## Workflow: How the Web App Works

This section provides a high-level overview of the application's flow, highlighting the interaction between different components.

### 1. Initial Load: Flask Renders the Home Page

When a user first accesses the application (e.g., `http://localhost:5000/`):
*   The `app.py` script's `main()` function is executed, which calls `create_app()`.
*   `create_app()` initializes the Flask application and loads configuration from `backend/auth/AuthConfig.py` (e.g., `SECRET_KEY`, Google OAuth details).
*   It then registers the `auth_bp` and `llm_bp` blueprints (defined in `backend/APIRoutes.py`) and home-specific routes.
*   The `app.add_url_rule('/', 'index', HomeRoutes.index)` in `app.py` maps the root URL to the `HomeRoutes.index` method.
*   `HomeRoutes.index` (in `app.py`) checks the Flask `session` for user information.
*   Finally, `HomeRoutes.index` renders `frontend/templates/home.html`. This page typically displays introductory content and a "Continue with Google" button.

### 2. User Authentication and Redirect to EasyLesson

When the user clicks "Continue with Google" (or a similar login trigger on `home.html`):
*   The frontend (likely `frontend/static/pages/home/home.js` or `frontend/static/api/service/auth_api.js`) triggers a redirect to the backend `/auth/login` route.
*   The `AuthAPI.login` method (in `backend/api/AuthAPI.py`) is invoked.
*   `AuthAPI.login` utilizes `AuthService.create_oauth_flow()` (in `backend/auth/AuthService.py`) to construct the Google OAuth URL.
*   The user's browser is redirected to Google's authentication page. The `AuthService` stores a `state` parameter in the Flask `session` for CSRF protection.
*   After successful authentication with Google, Google redirects the user back to the `/auth/callback` route of your application.
*   The `AuthAPI.callback` method (in `backend/api/AuthAPI.py`) handles this callback:
    *   It verifies the `state` parameter against the one stored in the `session` (for security).
    *   It uses `AuthService.create_oauth_flow()` and `flow.fetch_token()` to exchange the authorization code for an access token.
    *   `AuthService.verify_token_and_get_user()` (in `backend/auth/AuthService.py`) verifies the token and extracts user details (email, name, etc.).
    *   `AuthService.store_user_in_session()` (in `backend/auth/AuthService.py`) stores this user data in the Flask `session`.
*   Upon successful authentication, `AuthAPI.callback` redirects the user's browser to the `/easylesson` route.
*   The `app.add_url_rule('/easylesson', 'easylesson', HomeRoutes.easylesson)` in `app.py` maps this URL to `HomeRoutes.easylesson`.
*   Crucially, `HomeRoutes.easylesson` is protected by `@AuthDecorators.login_required` (from `backend/auth/AuthDecorators.py`), which ensures that only authenticated users can access this page.
*   `HomeRoutes.easylesson` then renders the `frontend/templates/easylesson.html` page, which is the main lesson planning interface.

### 3. LLM Initialization and Interaction on EasyLesson Page

Once `easylesson.html` is rendered and loaded in the browser:
*   Frontend JavaScript files (primarily `frontend/static/pages/easylesson/easylesson.js` and `frontend/static/api/service/llm_api.js`) will initialize.
*   The `frontend/static/api/init.js` script plays a role in centralizing the initialization of API service classes.
*   On the backend, the `LlmManager` (in `backend/llm/LlmManager.py`) is initialized when the Flask app starts (or first accessed, depending on its scope).
*   `LlmManager` dynamically loads all supported LLM models based on configurations defined in `backend/llm/LlmConfig.py`. Each model (e.g., Qwen, OpenAI) is an instance of a class found in `backend/llm/all_llm_models/` (inheriting from `backend/llm/all_llm_models/Model.py`).
*   When a user interacts with the lesson planning interface (e.g., types a prompt and clicks "Generate"):
    *   `frontend/static/pages/easylesson/easylesson.js` will call a function from `frontend/static/api/service/llm_api.js`.
    *   `llm_api.js` uses an instance of `APIClient` (from `frontend/static/api/core/APIClient.js`) and the LLM API routes (from `frontend/static/api/config/routes.js`) to send a request (e.g., POST to `/llm/chat`) to the backend.
    *   On the backend, `LlmAPI.send_chat_message` (in `backend/api/LlmAPI.py`) receives the request.
    *   `LlmAPI.send_chat_message` then delegates the actual interaction to `llm_manager.invoke(message)` (in `backend/llm/LlmManager.py`).
    *   `LlmManager.invoke()` uses the currently selected LLM model's client (e.g., `self.currentModel.llm_client`) to send the message to the LLM (via OpenRouter/LangChain).
    *   The LLM's response is returned through `LlmManager` to `LlmAPI`, which then sends it back as a JSON response to the frontend.
    *   `easylesson.js` receives the response and updates the UI accordingly.

## API Connection Between Frontend and Backend

The application employs a centralized API layer, promoting a clean separation of concerns and maintainable code. Backend and Frontend communicate primarily using JSON data over RESTful HTTP routes.

### Backend API Layer

1.  **Service-Specific Logic**: Your backend is organized into service-specific directories (e.g., `backend/auth/`, `backend/llm/`). These directories contain the core business logic for each domain (e.g., `AuthService.py` for authentication, `LlmManager.py` for LLM management).
2.  **API Handler Classes**: For each service, there's a corresponding API handler class in the `backend/api/` directory (e.g., `backend/api/AuthAPI.py`, `backend/api/LlmAPI.py`). These classes contain methods that implement the specific API endpoints. They act as a thin layer, often delegating complex tasks to the service-specific logic. They also inherit from `backend/api/BaseAPI.py` for standardized responses, error handling, and data sanitization.
3.  **Centralized Route Registration (`backend/APIRoutes.py`)**: This file serves as the single source of truth for all backend API routes.
    *   It defines Flask Blueprints (e.g., `auth_bp`, `llm_bp`).
    *   It imports the API handler methods (e.g., `AuthAPI.login`, `LlmAPI.get_available_models`).
    *   It registers these methods to specific URL rules within their respective blueprints using `add_url_rule`.
    *   This centralization makes it easy to review and manage all available API endpoints in one place.

### Frontend API Layer

The `frontend/static/api/` directory houses the entire client-side API interaction logic:

1.  **Configuration (`frontend/static/api/config/routes.js`)**: This file defines all the API routes that the frontend can interact with. It's a JavaScript object (attached to `window.API_ROUTES`) where each key represents a backend service (e.g., `AUTH`, `LLM`) and contains specific endpoint paths. This ensures that frontend and backend refer to the same paths, preventing discrepancies and making route changes manageable. All communication happens by these defined routes, with data exchanged in JSON format.
2.  **Core API Client (`frontend/static/api/core/`)**:
    *   `APIClient.js`: This is the low-level utility for making HTTP requests (GET, POST, PUT, etc.) to your backend. It handles the actual fetching, request headers, and basic response parsing.
    *   `APIError.js`: Provides a structured way to handle and interpret error responses received from the backend, allowing for consistent error display to the user.
    *   `APIManager.js`: A higher-level module that might wrap `APIClient.js` to add features like request queuing, caching, or more complex error handling across multiple API calls.
3.  **Service-Specific API Functions (`frontend/static/api/service/`)**:
    *   `auth_api.js`: Contains JavaScript functions for interacting with the backend's authentication API (e.g., `loginUser()`, `getUserInfo()`). These functions use an instance of `core/APIClient` and the route constants from `config/routes.js` to construct and send requests. They then process the JSON response into JavaScript actions or update the UI state.
    *   `llm_api.js`: Similarly, contains functions for interacting with the backend's LLM API (e.g., `getModels()`, `sendMessage()`).
    These service files abstract away the direct API calls, providing clean, reusable functions for the rest of the frontend.
4.  **Page-Level Integration (`frontend/static/pages/home/home.js`, `frontend/static/pages/easylesson/easylesson.js`)**: These page-specific JavaScript files will import and utilize the functions exposed by `service/auth_api.js` and `service/llm_api.js` to implement dynamic behavior and update the UI based on user interactions and API responses.
5.  **Centralized Initialization (`frontend/static/api/init.js`)**: This file centralizes the initialization steps for all API service classes (e.g., creating instances of `auth_api`, `llm_api`). This makes it easy to organize and manage the entire frontend API layer, ensuring that all services are properly set up before use.

## How to Add a New API

Extending the API with new functionality is straightforward due to the modular design. Let's say you want to add a `FileHandler` API for managing user files.

### 1. Backend Integration

1.  **Define New Service Logic (Optional but Recommended)**:
    *   Create a new directory for your service logic, e.g., `backend/file_handler/`.
    *   Inside this directory, create Python files for any business logic related to file handling (e.g., `FileService.py` for file upload/download, storage management).
2.  **Create API Handler Class**:
    *   Create a new Python file in `backend/api/`, e.g., `backend/api/FileHandlerAPI.py`.
    *   Define a class (e.g., `FileHandlerAPI`) that inherits from `BaseAPI`.
    *   Implement class methods for each API endpoint (e.g., `@classmethod def upload_file(cls):`, `@classmethod def download_file(cls):`). These methods will handle the Flask `request` and delegate to your `FileService` (if created) for core logic.
    ```python
    # backend/api/FileHandlerAPI.py
    from flask import request, jsonify
    from .BaseAPI import BaseAPI
    # from backend.file_handler.FileService import FileService # If you create a service

    class FileHandlerAPI(BaseAPI):
        @classmethod
        def upload_file(cls):
            # Logic to handle file upload
            return jsonify({"message": "File uploaded"}), 200

        @classmethod
        def list_files(cls):
            # Logic to list user files
            return jsonify({"files": ["file1.txt", "file2.pdf"]}), 200
    ```
3.  **Register Routes in `backend/APIRoutes.py`**:
    *   Import your new API handler class and define a new Flask Blueprint.
    *   Register the new routes to this blueprint.
    ```python
    # backend/APIRoutes.py
    # ... existing code ...
    from flask import Blueprint
    from backend.api.FileHandlerAPI import FileHandlerAPI # Import your new API

    # ... existing blueprints ...
    file_bp = Blueprint('file', __name__, url_prefix='/api/files') # Define new blueprint

    # Register File Handler routes
    file_bp.add_url_rule('/upload', view_func=FileHandlerAPI.upload_file, methods=['POST'])
    file_bp.add_url_rule('/list', view_func=FileHandlerAPI.list_files, methods=['GET'])
    # ... existing code ...
    ```
    *   Finally, ensure this new blueprint (`file_bp`) is registered in `app.py` within the `create_app` function:
    ```python
    # app.py
    # ... existing code ...
    from backend.APIRoutes import auth_bp, llm_bp, file_bp # Import new blueprint

    def create_app():
        app = Flask(__name__,
                    template_folder=HomeConfig.TEMPLATE_FOLDER,
                    static_folder=HomeConfig.STATIC_FOLDER)
        # ... existing config ...
        app.register_blueprint(auth_bp)
        app.register_blueprint(llm_bp)
        app.register_blueprint(file_bp) # Register the new blueprint
        # ... existing code ...
    ```

### 2. Frontend Integration

1.  **Add Routes to `frontend/static/api/config/routes.js`**:
    *   Define constants for your new API routes within the `window.API_ROUTES` object.
    ```javascript
    // frontend/static/api/config/routes.js
    window.API_ROUTES = {
      AUTH: { /* ... */ },
      LLM: { /* ... */ },
      FILE: { // Add new API routes here
        UPLOAD: '/api/files/upload',
        LIST: '/api/files/list',
      },
    };
    ```
2.  **Create Service-Specific API Functions (`frontend/static/api/service/file_api.js`)**:
    *   Create a new JavaScript file, e.g., `frontend/static/api/service/file_api.js`.
    *   Define functions that use your `APIClient` instance and the new route constants to interact with the backend.
    ```javascript
    // frontend/static/api/service/file_api.js
    import APIClient from '../core/APIClient.js';
    import { API_ROUTES } from '../config/routes.js'; // Assuming API_ROUTES is exported

    class FileApi {
      constructor(apiClient) {
        this.apiClient = apiClient;
      }

      async uploadFile(fileData) {
        const response = await this.apiClient.post(API_ROUTES.FILE.UPLOAD, fileData);
        return response.data;
      }

      async listFiles() {
        const response = await this.apiClient.get(API_ROUTES.FILE.LIST);
        return response.data.files;
      }
    }

    export default FileApi;
    ```
3.  **Update Centralized Initialization (`frontend/static/api/init.js`)**:
    *   Import your new API service class and instantiate it, making it available globally or through a manager.
    ```javascript
    // frontend/static/api/init.js
    import APIClient from './core/APIClient.js';
    import AuthApi from './service/auth_api.js';
    import LlmApi from './service/llm_api.js';
    import FileApi from './service/file_api.js'; // Import new API service

    const apiClient = new APIClient();

    // Initialize all API service classes
    window.authApi = new AuthApi(apiClient);
    window.llmApi = new LlmApi(apiClient);
    window.fileApi = new FileApi(apiClient); // Initialize new API service

    console.log("Frontend API services initialized.");
    ```
4.  **Integrate into Page-Level JavaScript**:
    *   Now you can use the new API functions in your page-specific JavaScript files (e.g., `frontend/static/pages/easylesson/easylesson.js`, `frontend/static/pages/home/home.js`) as needed.
    ```javascript
    // frontend/static/pages/easylesson/easylesson.js
    // Assuming fileApi is available via window.fileApi or imported
    // import { fileApi } from '../../static/api/init.js'; // Or direct import if module system supports

    document.getElementById('uploadButton').addEventListener('click', async () => {
      const file = document.getElementById('fileInput').files[0];
      if (file) {
        const formData = new FormData();
        formData.append('file', file);
        const result = await window.fileApi.uploadFile(formData);
        console.log('Upload result:', result);
      }
    });
    ```
