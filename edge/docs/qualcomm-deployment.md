# Qualcomm deployment pathway

Target architecture: Qualcomm Dragonwing/QCS6490 through QAIRT/QNN. This repository does not claim or emulate QNN execution.

```text
Validated PyTorch model → ONNX export → numerical comparison → representative calibration
→ INT8 post-training quantization → accuracy evaluation → QAIRT/QNN conversion → Hexagon NPU
```

Freeze preprocessing, input layout/size, normalization, output tensor shapes, and NMS behavior before conversion. Compare FP32 PyTorch and ONNX output tolerances on a licensed evaluation set. Only then collect representative calibration samples and evaluate quantized accuracy. Measure latency, thermal behavior, and throughput on the actual target; do not extrapolate desktop results.

`QualcommQNNRuntime` intentionally raises `NotImplementedError` until a supported device and licensed SDK are configured.
