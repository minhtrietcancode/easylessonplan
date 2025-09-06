# File: backend\api\LlmAPI.py"""
LLM API Module
Handles LLM-related API endpoints and operations.
"""

from flask import session, request, current_app, jsonify
from .BaseAPI import BaseAPI
import sys
import os

# Add the parent directory to the path to import llm
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.llm.LlmManager import LlmManager

from typing import Dict, Any, Tuple

# Initialize LlmManager globally or as part of app context
llm_manager = LlmManager()


class LlmAPI(BaseAPI):
    """API handler for LLM operations"""

    @classmethod
    def get_available_models(cls):
        """
        GET /api/llm/models - Get list of available LLM models and current model
        
        Returns:
            Flask response with list of models
        """
        try:
            models = llm_manager.get_available_models()
            current_model_name = llm_manager.getCurrentModelName()
            
            response_data, status_code = cls.success_response(
                data={
                    'models': models,
                    'current_model': current_model_name
                },
                message="Available models retrieved successfully"
            )
            
            return jsonify(response_data), status_code
            
        except Exception as e:
            response_data, status_code = cls.handle_exception(e, "Failed to retrieve available models")
            return jsonify(response_data), status_code

    @classmethod
    def get_current_model(cls):
        """
        GET /api/llm/current - Get the name of the currently active LLM model
        
        Returns:
            Flask response with current model name
        """
        try:
            current_model_name = llm_manager.getCurrentModelName()
            
            if current_model_name:
                response_data, status_code = cls.success_response(
                    data={'current_model': current_model_name},
                    message="Current model retrieved successfully"
                )
            else:
                response_data, status_code = cls.error_response(
                    message="No current model set",
                    status_code=404,
                    error_code="NO_CURRENT_MODEL"
                )
                
            return jsonify(response_data), status_code
            
        except Exception as e:
            response_data, status_code = cls.handle_exception(e, "Failed to retrieve current model")
            return jsonify(response_data), status_code

    @classmethod
    def set_current_model(cls):
        """
        PUT /api/llm/models - Set the current LLM model
        
        Returns:
            Flask response confirming model switch
        """
        try:
            data = request.get_json() or {}
            model_name = data.get('model_name')
            
            if not model_name:
                response_data, status_code = cls.error_response(
                    message="Model name is required",
                    status_code=400,
                    error_code="MISSING_MODEL_NAME"
                )
                return jsonify(response_data), status_code
            
            llm_manager.setCurrentModel(model_name)
            current_app.logger.info(f"Switched LLM model to: {model_name}")
            
            response_data, status_code = cls.success_response(
                data={'current_model': model_name},
                message=f"Successfully switched to {model_name} model"
            )
            
            return jsonify(response_data), status_code
            
        except ValueError as e:
            response_data, status_code = cls.error_response(
                message=str(e),
                status_code=400,
                error_code="INVALID_MODEL"
            )
            return jsonify(response_data), status_code
            
        except Exception as e:
            response_data, status_code = cls.handle_exception(e, "Failed to switch LLM model")
            return jsonify(response_data), status_code

    @classmethod
    def send_chat_message(cls):
        """
        POST /api/llm/chat - Send a message to the current LLM and get a response
        
        Returns:
            Flask response with LLM's reply
        """
        try:
            data = request.get_json() or {}
            message = data.get('message')

            if not message:
                response_data, status_code = cls.error_response(
                    message="Message content is required",
                    status_code=400,
                    error_code="MISSING_MESSAGE"
                )
                return jsonify(response_data), status_code

            current_app.logger.info(f"User message to LLM: {message}")
            llm_response = llm_manager.invoke(message)
            current_app.logger.info(f"LLM response: {llm_response}")

            response_data, status_code = cls.success_response(
                data={'reply': llm_response},
                message="LLM responded successfully"
            )
            
            return jsonify(response_data), status_code
            
        except Exception as e:
            response_data, status_code = cls.handle_exception(e, "Failed to get LLM response")
            return jsonify(response_data), status_code