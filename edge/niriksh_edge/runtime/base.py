from abc import ABC,abstractmethod
from typing import Any
class InferenceRuntime(ABC):
    @abstractmethod
    def load(self,model_path:str)->None:...
    @abstractmethod
    def infer(self,input_data:Any)->Any:...
