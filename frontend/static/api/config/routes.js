// File: frontend/static/api/config/routes.js
window.API_ROUTES = {
  AUTH: {
    GET_USER_INFO: '/auth/user',
    GET_LOGIN: '/auth/login',
  },
  LLM: {
    GET_MODELS_LIST: '/llm/models',
    PUT_SWITCH_MODEL: '/llm/models',
    POST_SEND_MESSAGE: '/llm/chat',
  },
};