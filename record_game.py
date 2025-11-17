import dxcam
import cv2
import os
import time
import uuid
from datetime import datetime

def record_game(output_folder="unknown", fps=30, interval_seconds=1.0):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    camera = dxcam.create()
    
    if camera is None:
        print("Не удалось инициализировать dxcam")
        return
    
    camera.start(target_fps=fps, video_mode=True)
    
    frame_count = 0
    last_capture_time = time.time()
    
    print(f"Запись игры с интервалом {interval_seconds} секунд. Используйте Ctrl+C для остановки")
    
    try:
        while True:
            current_time = time.time()
            
            if current_time - last_capture_time >= interval_seconds:
                frame = camera.get_latest_frame()
                
                if frame is not None:
                    frame_id = str(uuid.uuid4())
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    filename = os.path.join(output_folder, f"{output_folder}_{timestamp}_{frame_id}.png")
                    cv2.imwrite(filename, frame_rgb)
                    frame_count += 1
                    
                    last_capture_time = current_time
                    
                    if frame_count % 10 == 0:
                        print(f"Записано кадров: {frame_count}")
            
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        print("\nОстановка записи...")
    finally:
        try:
            camera.stop()
        except:
            pass
        print(f"Записано {frame_count} кадров")


if __name__ == "__main__":
    record_game(output_folder="dast2", fps=30, interval_seconds=3.0)
