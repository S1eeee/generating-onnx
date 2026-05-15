# generating-onnx-for-yolov8s (for yolov8s)
This repository is meant to be a precursor to my  onnx-to-hef-yolov8s repository. It trains an onnx model straight your training data, made for yolov8s

```
docker build -t yolov8-trainer .
```
```
sudo docker run -it --gpus all \
  --shm-size=2g \
  -v $(pwd)/dataset:/workspace/dataset \
  -v $(pwd)/output:/workspace/output \
  yolov8-trainer
```

# Next Steps:

[onnx to hef](https://github.com/S1eeee/onnx-to-hef-yolov8s/)
