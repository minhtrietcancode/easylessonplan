window.API_ROUTES = {
  AUTH: {
    STATUS: '/api/auth/status',
    USER: '/api/auth/user',
    VALIDATE: '/api/auth/validate',
    PREFERENCES: '/api/auth/preferences',
    LOGIN: '/api/auth/login',
    LOGOUT: '/api/auth/logout',
  },
  USER: {
    PROFILE: '/api/user/profile',
    DASHBOARD: '/api/user/dashboard',
    ACTIVITY: '/api/user/activity',
    STATISTICS: '/api/user/stats',
  },
  LLM_API: {
    GET_MODELS_LIST: '/api/llm/models',
    CHAT: '/api/llm/chat',
    SWITCH_MODEL: '/api/llm/models',
    SEND_MESSAGE: '/api/llm/chat',
  },
};
