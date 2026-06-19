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

##Update Parameters

To update train parameters look at the python script and scroll all the way down. Updating parameters will be easier in the future.

Then just run the following commands; self explanatory what they do

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

--shm-size was necessary when I was initially working on this, due to the specs of the gpu I had to use at the time. You can probably remove that flag.

# Next Steps:

[onnx to hef](https://github.com/S1eeee/onnx-to-hef-yolov8s/)
