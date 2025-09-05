window.API_ROUTES = {
  AUTH: {
    GET_STATUS: '/api/auth/status',
    GET_USER_INFO: '/api/auth/user',
    GET_VALIDATE_SESSION: '/api/auth/validate',
    GET_USER_PREFERENCES: '/api/auth/preferences',
    PUT_UPDATE_USER_PREFERENCES: '/api/auth/preferences',
  },
  USER: {
    GET_PROFILE: '/api/user/profile',
    PUT_UPDATE_PROFILE: '/api/user/profile',
    GET_DASHBOARD_DATA: '/api/user/dashboard',
    GET_ACTIVITY_LOG: '/api/user/activity',
    GET_STATISTICS: '/api/user/stats',
  },
  LLM: {
    GET_MODELS_LIST: '/api/llm/models',
    PUT_SWITCH_MODEL: '/api/llm/models',
    POST_SEND_MESSAGE: '/api/llm/chat',
  },
};

window.OAUTH_ROUTES = {
  GET_LOGIN: '/auth/login',
  GET_LOGOUT: '/auth/logout',
};
