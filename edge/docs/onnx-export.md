# ONNX export contract

Suggested MVP input is NCHW float32 at 640×640 with letterbox preprocessing and model-specific normalization. Preserve raw detection head output or explicitly document whether NMS is embedded. Export is intentionally manual because output contracts differ across model families. Compare class scores and boxes against the original runtime on the same frames before deployment.
