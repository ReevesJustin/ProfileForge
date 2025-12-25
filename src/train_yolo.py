from ultralytics import YOLO

def train_yolo_pose(data_yaml='data.yaml', epochs=100, imgsz=640):
    """Train YOLOv8-pose on bullet keypoints dataset."""
    model = YOLO('yolov8n-pose.pt')  # load pre-trained
    model.train(data=data_yaml, epochs=epochs, imgsz=imgsz)
    model.save('models/yolo_bullet_pose.pt')

if __name__ == "__main__":
    train_yolo_pose()