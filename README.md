# generating-onnx-for-yolov8s (for yolov8s)
This repository is meant to be a precursor to my  onnx-to-hef-yolov8s repository. It trains an onnx model straight your training data, made for yolov8s


### Avoid Using This Repo If You Can ###

This is really janky and rigid, a nightmare to work on. I am planning on improvements, but at least for now, avoid using this. 
It is really only good for quick, successive iterations, or as a quick, inital proof of concept. 

In the future I want this to be more of an interactive cli tool, likely just for yolov8. Either way, it is not there yet. 

If you must, however, The general instructions follow.

# Video

### This is a video that I made, might be useful. It'll be updated in the future

```
https://www.youtube.com/watch?v=tDq6RIIhIlc
```

# Usage

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
