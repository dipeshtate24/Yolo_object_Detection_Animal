import cv2
import os
from ultralytics import YOLO

model = YOLO('./model/yolov8n.pt')

def image_processing(image_path):

    orig_img = cv2.imread(image_path)
    orig_copy = orig_img.copy()
    
    try:
        if orig_img is None:
            raise FileNotFoundError("Could not read image.")
        else:
            outputs = model(orig_img)
    
    except FileNotFoundError as e:
        print("File Not Found.")

    for output in outputs:
        boxes = output.boxes
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            score = float(box.conf[0])
            class_id = int(box.cls[0])
            label = model.names[class_id]

            if score > 0.5:
                cropped_image = orig_img[y1:y2, x1:x2]

                folder_path = label
                os.makedirs(folder_path, exist_ok=True)

                image_count = len(os.listdir(folder_path))
                save_path = os.path.join(folder_path, f"{label}_{image_count}.jpg" )
                cv2.imwrite(save_path, cropped_image)


                cv2.rectangle(orig_copy, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(orig_copy, f"{label}:{score:.2f}", (x1, y1-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                

if __name__ == "__main__":
    image_processing()
    
