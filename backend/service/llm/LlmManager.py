# Updated LlmManager.py - Dynamic model loading with Model instance as currentModel
import importlib
import os
from .LlmConfig import LlmConfig
from langchain_core.messages import HumanMessage

class LlmManager:
    def __init__(self) -> None:
        # Get supported models dynamically from config --> type: list[model_name : string]
        self.supported_models = LlmConfig.get_supported_models()
        
        # Dynamically load all model instances
        self.model_instances = {} # --> type: dict {"model_name" : Model(), ...}
        self._load_all_models()
        
        # Set default model (first in the list or specify)
        default_model = "Qwen" if "Qwen" in self.supported_models else self.supported_models[0]
        self.setCurrentModel(default_model) # type of currentModel: Model()

    def _load_all_models(self):
        """Dynamically loads all model classes and creates instances"""
        models_dir = os.path.join(os.path.dirname(__file__), 'all_llm_models')
        
        for model_name in self.supported_models:
            try:
                config = LlmConfig.get_model_config(model_name)
                class_name = config["class_name"]
                
                # Dynamically import the module
                module = importlib.import_module(f'.all_llm_models.{class_name}', package=__package__)
                
                # Get the class from the module
                model_class = getattr(module, class_name)
                
                # Create instance and store it
                self.model_instances[model_name] = model_class()
                
                print(f"✅ Successfully loaded {model_name} model")
                
            except Exception as e:
                print(f"❌ Failed to load {model_name} model: {e}")
                # Remove from supported models if loading fails
                self.supported_models = [m for m in self.supported_models if m != model_name]

    def setCurrentModel(self, model_name: str):
        """
        Set the current LLM model by name.
        Args:
            model_name (str): The name of the model to set as current.
        Raises:
            ValueError: If the model_name is not supported.
        """
        if model_name not in self.supported_models:
            raise ValueError(f"Model '{model_name}' is not supported. Supported models: {self.supported_models}")

        if model_name not in self.model_instances:
            raise ValueError(f"Model '{model_name}' is supported but not loaded.")
            
        # Now currentModel is a Model instance, not the llm_client
        self.currentModel = self.model_instances[model_name]
        print(f"🔄 Switched to {model_name} model")

    def getCurrentModel(self):
        """
        Returns the current Model instance (not the client).
        To get the actual LLM client, use getCurrentModelClient().
        """
        return self.currentModel
    
    def getCurrentModelClient(self):
        """
        Returns the current model's LLM client (ChatOpenAI instance).
        This is what you use to actually invoke the model.
        """
        return self.currentModel.llm_client
    
    def getCurrentModelName(self):
        """Returns the name of the current model"""
        for model_name, instance in self.model_instances.items():
            if instance == self.currentModel:
                return model_name
        return None
    
    def get_available_models(self):
        """Returns list of successfully loaded models: List["model_name" : string] """
        return list(self.model_instances.keys())
    
    def invoke(self, message: str):
        """
        Method to invoke the current client model of this LlmManager 
            - Input: message --> string
            - Output: response.content --> string
        """
        try: 
            # Use the new getCurrentModelClient() method
            current_client = self.getCurrentModelClient()
            current_client_response = current_client.invoke([HumanMessage(content=message)])
            return current_client_response.content
        except ValueError as e:
            print(f"Error setting model: {e}")
        except Exception as e:
            print(f"An unexpected error occurred with current model: {e}")
