import cv2
import os
from ultralytics import YOLO

model = YOLO('./model/yolov8n.pt')

def image_processing(image_path):

    orig_img = cv2.imread(image_path)
    
    if orig_img is None:
        print("File Not Found.")
        return

    orig_copy = orig_img.copy()
    outputs = model(orig_img)

    for output in outputs:
        boxes = output.boxes

        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            score = float(box.conf[0])
            class_id = int(box.cls[0])
            label = model.names[class_id]

            if score > 0.5:
                # Draw bounding box
                cv2.rectangle(orig_copy, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(orig_copy, f"{label}:{score:.2f}",
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (0, 0, 255), 2)

    save_folder = "output_images"
    os.makedirs(save_folder, exist_ok=True)

    image_count = len(os.listdir(save_folder))
    save_path = os.path.join(save_folder, f"output_{image_count}.jpg")

    cv2.imwrite(save_path, orig_copy)


if __name__ == "__main__":
    image_processing()