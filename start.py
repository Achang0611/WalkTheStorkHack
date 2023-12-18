import threading

import cv2
import numpy as np
import pydirectinput
from mss import mss
from PIL import Image
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator


def press_left():
  pydirectinput.press("left")
  
def press_right():
  pydirectinput.press("right")

def get_bbox_sct_img(box):
  x, y, w, h = box
  box = (x, y, x + w, y + h)
  sct = mss().grab(box)
  img = Image.frombytes(
            "RGB", 
            (sct.width, sct.height), 
            sct.rgb, 
        )
  img = np.array(img)
  img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
  return img

model = YOLO("../runs/detect/train/weights/best.pt")
sct = mss()

screen = get_bbox_sct_img((0, 0, 1920, 1080))
game_bbox = cv2.selectROI("Game area", screen)
cv2.destroyWindow("Game area")
print("game bbox: ", game_bbox)
scale_x, scale_y = (0.551, 0.478)
center_x, center_y = (game_bbox[2] * scale_x, game_bbox[3] * scale_y)
head_center = (int(center_x), int(center_y))

last_cx = 0

while True:
  # ret, img = cap.read()
  # if not ret:
  #   break
  img = get_bbox_sct_img(game_bbox)
  
  annotator = Annotator(img)
  results = model(img)
  for result in results:
    for box in result.boxes:
      annotator.box_label(box.xyxy[0], f"{result.names[int(box.cls)]} {float(box.conf):.2}")
      
      x1, y1, x2, y2 = box.xyxy[0].tolist()
      cx, cy = (int((x1 + x2) / 2), int((y1 + y2) / 2))
      cv2.line(img, (cx, cy), head_center, (255, 0, 0), 2)
      
      error_x = cx - head_center[0]
      error_cx = cx - last_cx
      if error_x > 0:
        # 頭偏右
        if error_cx < 0:
          # 頭有往左回正的趨勢 不需要操作
          pass
        else:
          threading.Thread(target=press_left).start()
      if error_x < 0:
        if error_cx < 0:
          # 頭有往左倒的趨勢
          threading.Thread(target=press_right).start()
        else:
          pass
      
      last_cx = cx
      
  
  cv2.circle(img, head_center, 10, (0, 255, 0), 2)
  
  cv2.imshow("img", img)
  if cv2.waitKey(1) == ord('q'):
    break

cv2.destroyAllWindows()
