from flask import session, request, current_app
from .base_api import BaseAPI
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
    def get_available_models(cls) -> Tuple[Dict, int]:
        """
        Get list of available LLM models.
        Returns:
            API response with list of models
        """
        try:
            models = llm_manager.get_available_models()
            current_model_name = llm_manager.getCurrentModelName()
            return cls.success_response(
                data={
                    'models': models,
                    'current_model': current_model_name
                },
                message="Available models retrieved successfully"
            )
        except Exception as e:
            return cls.handle_exception(e, "Failed to retrieve available models")

    @classmethod
    def get_current_model(cls) -> Tuple[Dict, int]:
        """
        Get the name of the currently active LLM model.
        Returns:
            API response with current model name
        """
        try:
            current_model_name = llm_manager.getCurrentModelName()
            if current_model_name:
                return cls.success_response(
                    data={'current_model': current_model_name},
                    message="Current model retrieved successfully"
                )
            else:
                return cls.error_response(
                    message="No current model set",
                    status_code=404,
                    error_code="NO_CURRENT_MODEL"
                )
        except Exception as e:
            return cls.handle_exception(e, "Failed to retrieve current model")

    @classmethod
    def set_current_model(cls, model_name: str) -> Tuple[Dict, int]:
        """
        Set the current LLM model.
        Args:
            model_name: The name of the model to set.
        Returns:
            API response confirming model switch
        """
        try:
            llm_manager.setCurrentModel(model_name)
            current_app.logger.info(f"Switched LLM model to: {model_name}")
            return cls.success_response(
                data={'current_model': model_name},
                message=f"Successfully switched to {model_name} model"
            )
        except ValueError as e:
            return cls.error_response(
                message=str(e),
                status_code=400,
                error_code="INVALID_MODEL"
            )
        except Exception as e:
            return cls.handle_exception(e, "Failed to switch LLM model")

    @classmethod
    def send_chat_message(cls) -> Tuple[Dict, int]:
        """
        Send a message to the current LLM and get a response.
        Returns:
            API response with LLM's reply
        """
        try:
            data = request.get_json()
            message = data.get('message')

            if not message:
                return cls.error_response(
                    message="Message content is required",
                    status_code=400,
                    error_code="MISSING_MESSAGE"
                )

            current_app.logger.info(f"User message to LLM: {message}")
            llm_response = llm_manager.invoke(message)
            current_app.logger.info(f"LLM response: {llm_response}")

            return cls.success_response(
                data={'reply': llm_response},
                message="LLM responded successfully"
            )
        except Exception as e:
            return cls.handle_exception(e, "Failed to get LLM response")
