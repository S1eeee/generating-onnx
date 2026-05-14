#!/bin/bash
set -e

echo "Starting Training..."
python3 /workspace/train.py

echo "Moving best.onnx to output folder..."
cp /workspace/runs/detect/train/weights/best.onnx /workspace/output/best.onnx

echo "Done, you can find your onnx model in the /output directory."