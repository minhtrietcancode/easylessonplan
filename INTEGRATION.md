# EasyLesson Integration Documentation

## Overview of Changes

We've integrated the EasyLesson functionality into the main Flask application while maintaining our clean API architecture. Here's what changed:

### 1. Authentication Flow
- Modified OAuth callback to redirect to `/easylesson` instead of `/dashboard`
- Added login protection to the EasyLesson interface
- Maintained session handling and user verification

### 2. API Structure
- Created new `lesson_api.py` using the existing BaseAPI pattern
- Routes organized under `/api/lesson/*` prefix:
  - `/api/lesson/chat` - Handle chat messages
  - `/api/lesson/models` - Get/switch LLM models
  - `/api/lesson/conversation/*` - Manage chat history

### 3. Main Application
- Integrated EasyLesson page routes into `home.py`
- Added LLM service initialization
- Preserved existing authentication and user API endpoints

### 4. Frontend Integration
- EasyLesson interface accessible at `/easylesson`
- Maintains existing API client structure
- Uses the same authentication flow

## API Endpoints

### Authentication (Unchanged)
- `/auth/login` - Initiate OAuth login
- `/auth/callback` - Handle OAuth response
- `/auth/logout` - User logout
- `/auth/user` - Get user info
- `/auth/status` - Check auth status

### Lesson Planning (New)
- `/api/lesson/chat` - Send/receive chat messages
- `/api/lesson/models` - List available LLM models
- `/api/lesson/models/switch` - Switch active model
- `/api/lesson/conversation/clear` - Clear chat history
- `/api/lesson/conversation/history` - Get chat history

### User Management (Unchanged)
- `/api/user/profile` - User profile operations
- `/api/user/dashboard` - Get dashboard data
- `/api/user/activity` - User activity log
- `/api/user/stats` - Usage statistics

## Response Format

All API endpoints maintain the standardized response format:

```json
{
  "success": boolean,
  "message": string,
  "data": object,
  "error_code": string (optional)
}
```

## Authentication Flow

1. User visits site → Sees login page
2. Clicks login → Google OAuth
3. OAuth callback → Redirected to EasyLesson interface
4. All subsequent API calls include session cookie

## LLM Service

The LLM functionality is now properly integrated into the main application:
- Initialization happens during app startup
- Error handling follows the BaseAPI pattern
- Model management is accessible through the API
