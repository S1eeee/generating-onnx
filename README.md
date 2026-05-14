# generating-onnx-for-yolov8s (for yolov8s) (Not necessarily just for yolov8s)
This repository is meant to be a precursor to my  onnx-to-hef-yolov8s repository. Starting with training a pt with the training data you have labeled.

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
