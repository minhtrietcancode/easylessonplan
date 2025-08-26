from .all_llm_models.Qwen import Qwen
from .all_llm_models.OpenAI import Openai
from . import SupportedModels

class LlmManager():
    def __init__(self) -> None:
        # load the list of supported models 
        self.supported_models = SupportedModels.supported_models
        
        # create an instance for each models classes
        self.Qwen = Qwen()
        self.Openai = Openai()

        # initially, make the Qwen model as the default currentModel 
        self.currentModel = self.Qwen.llm_client


    """
        Set the current LLM model by name.
        Args:
            model_name (str): The name of the model to set as current.
        Raises:
            ValueError: If the model_name is not supported.
    """
    def setCurrentModel(self, model_name: str):
        # validate the Model first, if not in the supported_models list then exit + raise error
        if model_name not in self.supported_models:
            raise ValueError(f"Model '{model_name}' is not supported. Supported models: {self.supported_models}")

        # if valid then set self.currentModel = corresponding model instance
        # Map model_name to the corresponding instance
        try:
            model_instance = getattr(self, model_name)
            self.currentModel = model_instance.llm_client
        except AttributeError:
            raise ValueError(f"Model '{model_name}' is recognized but no instance is available or property name is incorrect.")
        
    '''
        Getters to get the currentModel
    '''
    def getCurrentModel(self):
        return self.currentModel
    
    
    