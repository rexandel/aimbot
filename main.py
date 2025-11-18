import torch
from ultralytics import YOLO
import time

def monitor_gpu():
    if torch.cuda.is_available():
        print(f"GPU Memory allocated: {torch.cuda.memory_allocated(0) / 1024**2:.1f} MB")
        print(f"GPU Memory reserved: {torch.cuda.memory_reserved(0) / 1024**2:.1f} MB")

def main():
    print(f"CUDA available: {torch.cuda.is_available()}")
    print(f"CUDA device count: {torch.cuda.device_count()}")
    if torch.cuda.is_available():
        print(f"Current CUDA device: {torch.cuda.current_device()}")
        print(f"CUDA device name: {torch.cuda.get_device_name()}")
    
    torch.cuda.set_device(0)

    model = YOLO('yolo12n.pt')
    
    print("Before training - GPU usage:")
    monitor_gpu()
    
    results = model.train(
        data=r'Z:\Aimbot\dataset\data.yaml',
        epochs=50,
        imgsz=640,
        batch=16,
        device=1,  
        workers=2,
        cache='disk',
        patience=10,
        save=True,
        verbose=True,
        amp=True
    )

if __name__ == '__main__':
    main()