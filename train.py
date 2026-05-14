import os
import yaml
import shutil
import random
from pathlib import Path
from ultralytics import YOLO

def get_dataset_stats(base_path):
    stats = {}
    for split in ['train', 'valid', 'test']:
        img_path = os.path.join(base_path, split, 'images')
        if os.path.exists(img_path):
            stats[split] = [f for f in os.listdir(img_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        else:
            stats[split] = []
    return stats

def move_files(base_path, files, source_split, target_split):
    os.makedirs(os.path.join(base_path, target_split, 'images'), exist_ok=True)
    os.makedirs(os.path.join(base_path, target_split, 'labels'), exist_ok=True)
    for f in files:
        # Move image
        shutil.move(os.path.join(base_path, source_split, 'images', f),
                    os.path.join(base_path, target_split, 'images', f))
        # Move label
        label_name = os.path.splitext(f)[0] + '.txt'
        src_label = os.path.join(base_path, source_split, 'labels', label_name)
        if os.path.exists(src_label):
            shutil.move(src_label, os.path.join(base_path, target_split, 'labels', label_name))

def detect_classes(base_path):
    """
    Finds class names. Priority: 
    1. Existing data.yaml in dataset folder
    2. classes.txt
    3. Manual scan of label files
    """
    # 1. Try existing data.yaml (Roboflow style)
    roboflow_yaml = os.path.join(base_path, 'data.yaml')
    if os.path.exists(roboflow_yaml):
        try:
            with open(roboflow_yaml, 'r') as f:
                data = yaml.safe_load(f)
                if 'names' in data:
                    # Convert list to dict if necessary
                    if isinstance(data['names'], list):
                        return {i: name for i, name in enumerate(data['names'])}
                    return data['names']
        except Exception as e:
            print(f"Warning: Could not parse existing data.yaml: {e}")

    # 2. Try classes.txt
    txt_path = os.path.join(base_path, 'train', 'labels', 'classes.txt')
    if os.path.exists(txt_path):
        with open(txt_path, 'r') as f:
            names = [line.strip() for line in f.readlines() if line.strip()]
            return {i: name for i, name in enumerate(names)}

    # 3. Fallback: Scan label IDs
    print("⚠️ No metadata found. Scanning labels to count classes...")
    label_dir = os.path.join(base_path, 'train', 'labels')
    max_idx = 0
    if os.path.exists(label_dir):
        for label_file in os.listdir(label_dir):
            if label_file.endswith('.txt'):
                with open(os.path.join(label_dir, label_file), 'r') as f:
                    for line in f:
                        try:
                            cls_idx = int(line.split()[0])
                            max_idx = max(max_idx, cls_idx)
                        except: continue
    return {i: f"class_{i}" for i in range(max_idx + 1)}

def smart_split_logic(base_path):
    stats = get_dataset_stats(base_path)
    total = sum(len(v) for v in stats.values())
    if total == 0: return

    print(f"\n--- Dataset Analysis ---")
    print(f"Total Images: {total}")
    for split, files in stats.items():
        print(f"  - {split}: {len(files)} images")

    # Only offer to split if valid folder is missing or empty
    if not stats['valid']:
        print("\n⚠️ No 'valid' folder detected.")
        choice = input("Create a 'valid' split from 'train'? (y/n): ").lower()
        if choice == 'y':
            pct = float(input("Enter % to move (e.g. 20): ") or 20) / 100
            num_to_move = int(len(stats['train']) * pct)
            to_move = random.sample(stats['train'], num_to_move)
            move_files(base_path, to_move, 'train', 'valid')
            print(f"✅ Moved {num_to_move} samples.")

def prepare_final_yaml(base_path):
    class_map = detect_classes(base_path)
    print(f"✅ Training with {len(class_map)} classes: {list(class_map.values())}")
    
    # Check what folders exist AFTER the split logic
    has_val = len(os.listdir(os.path.join(base_path, 'valid', 'images'))) > 0 if os.path.exists(os.path.join(base_path, 'valid', 'images')) else False
    has_test = len(os.listdir(os.path.join(base_path, 'test', 'images'))) > 0 if os.path.exists(os.path.join(base_path, 'test', 'images')) else False
    
    config = {
        'path': base_path,
        'train': 'train/images',
        'val': 'valid/images' if has_val else 'train/images',
        'names': class_map
    }
    if has_test: config['test'] = 'test/images'

    yaml_path = '/workspace/data.yaml'
    with open(yaml_path, 'w') as f:
        yaml.dump(config, f)
    return yaml_path

# --- START ---
DATA_DIR = "/workspace/dataset"

# 1. Manage folder splits
smart_split_logic(DATA_DIR)

# 2. Build the YAML based on detected classes
final_yaml = prepare_final_yaml(DATA_DIR)

# 3. Train
model = YOLO('yolov8s.pt')
model.train(
    data=final_yaml,
    epochs=100,
    imgsz=640,
    batch=4,
    workers=2,
    device=0,
    project='/workspace/output',
    name='custom_yolo_model',
    exist_ok=True
)

# 4. Export
print("Exporting ONNX...")
model.export(format='onnx', imgsz=640, opset=12, dynamic=False)