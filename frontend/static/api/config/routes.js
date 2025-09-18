// File: frontend/static/api/config/routes.js
window.API_ROUTES = {
  AUTH: {
    GET_USER_INFO: '/auth/get_user_info',
    GET_LOGIN: '/auth/login',
  },
  LLM: {
    GET_MODELS_LIST: '/llm/get_available_models',
    PUT_SWITCH_MODEL: '/llm/set_current_model',
    POST_SEND_MESSAGE: '/llm/chat',
  },
};