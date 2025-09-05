// File: frontend/static/api/config/routes.js
window.API_ROUTES = {
  AUTH: {
    GET_USER_INFO: '/api/auth/user',
  },
  LLM: {
    GET_MODELS_LIST: '/api/llm/models',
    PUT_SWITCH_MODEL: '/api/llm/models',
    POST_SEND_MESSAGE: '/api/llm/chat',
  },
};

window.OAUTH_ROUTES = {
  GET_LOGIN: '/auth/login',
};