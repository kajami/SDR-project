
import numpy as np
import torch
import pyautogui
import cv2

from matplotlib import pyplot as plt


# git clone https://github.com/ultralytics/yolov5
#


# Load custom model from local files
model = torch.hub.load(r'C:\Users\Pauli\Documents\School\monialaprojekti\yolov5\yolov5', 'custom', path='am_fm', source='local')


img = 'https://ultralytics.com/images/zidane.jpg'

# results = model(img)
# results.print()
#
#
# plt.imshow(np.squeeze(results.render()))
# plt.show()
#
# results.render()



# simple loop over screenshotted frames
while True:
    # Take a screenshot
    screen = pyautogui.screenshot()
    # convert to array
    screen_array = np.array(screen)
    # crop region
    crop = screen_array[100:400, 100:1200, :]
    color = cv2.cvtColor(crop, cv2.COLOR_RGB2BGR)

    # do detection
    results = model(color)

    print(results.xyxy[0])  # im predictions (tensor)
    print(results.pandas().xyxy[0])  # im predictions (pandas)

    # show live-detection
    cv2.imshow('SDR-signal', np.squeeze(results.render()))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()