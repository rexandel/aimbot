import dxcam
import cv2
import os
import time
import uuid
from datetime import datetime
from contextlib import contextmanager

@contextmanager
def dxcam_capture(target_fps=30, video_mode=False):
    camera = None
    try:
        camera = dxcam.create()
        
        if camera is None:
            raise RuntimeError("Не удалось инициализировать dxcam")
        
        camera.start(target_fps=target_fps, video_mode=video_mode)
        print(f"Dxcam инициализирован успешно (video_mode={video_mode})")
        yield camera
        
    except Exception as e:
        print(f"Ошибка при работе с dxcam: {e}")
        raise
    finally:
        if camera is not None:
            try:
                camera.stop()
                print("Dxcam остановлен")
            except Exception as e:
                print(f"Ошибка при остановке dxcam: {e}")

def adaptive_record_game(output_folder="unknown", fps=30, interval_seconds=1.0):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    frame_count = 0
    last_capture_time = time.time()
    last_successful_capture = time.time()
    consecutive_failures = 0
    
    print(f"Запись игры с интервалом {interval_seconds} секунд. Используйте Ctrl+C для остановки")
    
    try:
        with dxcam_capture(target_fps=fps, video_mode=False) as camera:
            while True:
                current_time = time.time()
                time_since_last_capture = current_time - last_capture_time
                
                if time_since_last_capture >= interval_seconds:
                    frame = camera.get_latest_frame()
                    
                    if frame is not None:    
                        try:
                            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                            filename = os.path.join(output_folder, f"{output_folder}_{timestamp}.png")
                            cv2.imwrite(filename, frame_rgb)
                            
                            frame_count += 1
                            last_capture_time = current_time
                            last_successful_capture = current_time
                            consecutive_failures = 0
                            
                            if frame_count % 10 == 0:
                                current_fps = 10 / (time.time() - last_successful_capture + 0.1)
                                print(f"Записано кадров: {frame_count}, текущий FPS: {current_fps:.1f}")
                                
                        except Exception as e:
                            print(f"Ошибка обработки кадра: {e}")
                            consecutive_failures += 1
                    else:
                        consecutive_failures += 1
                        if consecutive_failures % 10 == 0:
                            print(f"Подряд пропущено кадров: {consecutive_failures}")
                
                sleep_time = max(0.001, interval_seconds / 10)
                time.sleep(sleep_time)
                
                if consecutive_failures > 100:
                    print("Слишком много ошибок, попробуйте перезапустить запись")
                    break
                    
    except KeyboardInterrupt:
        print("\nОстановка записи...")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        print(f"Записано {frame_count} кадров")


if __name__ == "__main__":
    adaptive_record_game(output_folder="dust2", fps=60, interval_seconds=1.0)