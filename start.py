import threading
from time import sleep

import cv2
import numpy as np
import pydirectinput
from mss import mss
from PIL import Image


def pick_sct():
  img = get_bbox_sct_img({'left': 0, 'top': 0, 'width': 1920, 'height': 1080})
  bbox = cv2.selectROI("pick screen range", img, fromCenter=False, showCrosshair=True) 
  cv2.destroyWindow("pick screen range")
  cv2.waitKey(250)
  bbox = {"left": bbox[0], "top": bbox[1], "width": bbox[2], "height": bbox[3]}
  return bbox

def get_bbox_sct_img(box):
  # box = {'left': 556, 'top': 176, 'width': 820, 'height': 616}
  sct = mss().grab(box)
  img = Image.frombytes(
            "RGB", 
            (sct.width, sct.height), 
            sct.rgb, 
        )
  img = np.array(img)
  img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
  return img

def hold(key, secs):
  pydirectinput.keyDown(key)
  sleep(secs)
  pydirectinput.keyUp(key)

def go_left():
  global stop_flag
  while not stop_flag:
    global left_flag
    global x_error
    global last_error
    if left_flag:
      diff = last_error - x_error
      print(diff)
      if diff <= 0:
        print("順偏正")
        continue
      else:
        print("逆偏正")
        hold("left", 0)
      # pydirectinput.press("left")
      # print("left ", x_error)
      continue
    sleep(0.001)

def go_right():
  global stop_flag
  while not stop_flag:
    global right_flag
    global x_error
    global last_error
    if right_flag:
      diff = last_error - x_error
      print(diff)
      if diff >= 0:
        print("順偏正")
        continue
      else:
        print("逆偏正")
        hold("right", 0)
      # pydirectinput.press("right")
      # print("right ", x_error)
      continue
    sleep(0.001)

left_flag = False
right_flag = False
x_error = 0
last_error = 0
stop_flag = False

def main():
  img_set = cv2.VideoCapture("./assets/dock_1.gif")
  
  tracker = cv2.legacy.TrackerCSRT.create()
  capture_bbox = pick_sct()
  # capture_bbox = {'left': 189, 'top': 177, 'width': 657, 'height': 494}
  print(capture_bbox)
  # ret, img = image_set.read()
  img = get_bbox_sct_img(capture_bbox)
  
  init_bbox = cv2.selectROI("select target", img, fromCenter=True, showCrosshair=True)
  cv2.destroyWindow("select target")
  cv2.waitKey(250)
  tracker.init(img, init_bbox)
  
  left_thread = threading.Thread(target=go_left).start()
  right_thread = threading.Thread(target=go_right).start()
  
  while True:
    # ret, img = image_set.read()
    # if not ret:
    #   break
    img = get_bbox_sct_img(capture_bbox)
    
    x, y, w, h = [int(e) for e in init_bbox]
    init_center = (x + int(w / 2), y + int(h / 2))
    cv2.circle(img, init_center, 10, (0, 0, 255), 2)
    
    ok, bbox = tracker.update(img)
    x, y, w, h = [int(v) for v in bbox]
    dock_center = (x + int(w / 2), y + int(h / 2))
    cv2.circle(img, dock_center, 10, (255, 0, 0), 2)
      
    init = np.array(init_center)
    dock = np.array(dock_center)
    error = init - dock 
    
    global left_flag
    global right_flag
    global x_error
    global last_error
    left_flag = error[0] < -5
    right_flag = error[0] > 5
    last_error = x_error
    x_error = error[0]
    
    # if error[0] < 0:
    #   # print("鴨頭在右邊 往左走")
    #   threading.Thread(target = go_left).start()
    # else:
    #   # print("鴨頭在左邊 往右走")
    #   # threading.Thread(target = lambda: pydirectinput.press("left")).start()
    #   threading.Thread(target = go_right).start()
    
    cv2.imshow("image", img)
    key = cv2.waitKey(1)
    if key == ord("q"):
      break
    elif key == ord("w"):
      tracker = cv2.legacy.TrackerCSRT.create()
      tracker.init(img, init_bbox)
  
  global stop_flag
  stop_flag = True

if __name__ == "__main__":
  main()