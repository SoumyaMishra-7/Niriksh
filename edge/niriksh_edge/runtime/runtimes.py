from typing import Any
from niriksh_edge.runtime.base import InferenceRuntime
class PyTorchRuntime(InferenceRuntime):
    def load(self,model_path:str):
        try:import torch
        except ImportError as exc:raise RuntimeError('PyTorch is not installed') from exc
        self.model=torch.jit.load(model_path).eval()
    def infer(self,input_data:Any):return self.model(input_data)
class ONNXRuntime(InferenceRuntime):
    def load(self,model_path:str):
        try:import onnxruntime as ort
        except ImportError as exc:raise RuntimeError('onnxruntime is not installed') from exc
        self.session=ort.InferenceSession(model_path,providers=['CPUExecutionProvider'])
    def infer(self,input_data:Any):return self.session.run(None,{self.session.get_inputs()[0].name:input_data})
class QualcommQNNRuntime(InferenceRuntime):
    def load(self,model_path:str):raise NotImplementedError('Requires a licensed QAIRT/QNN SDK and supported Qualcomm hardware')
    def infer(self,input_data:Any):raise NotImplementedError('QNN execution is unavailable in this environment')
