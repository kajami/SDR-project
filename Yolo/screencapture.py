import numpy as np
import torch
import pyautogui
import cv2
import pytesseract

from matplotlib import pyplot as plt

# git clone https://github.com/ultralytics/yolov5
#


# Load custom model from local files
model = torch.hub.load(r'C:\Users\Pauli\Documents\School\monialaprojekti\yolov5\yolov5', 'custom', path='sigandnum',
                       source='local')

# img = 'https://ultralytics.com/images/zidane.jpg'
#
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

    # print(results.xyxy[0])  # im predictions (tensor)
    # print(results.pandas().xyxy[0])  # im predictions (pandas)

    pred = results.pandas().xyxy[0]
    i = 0
    signal_middle = []
    num_middle = []
    text_abs = 0
    text = ''
    dist_coords = 0
    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
    for index, row in pred.iterrows():
        middle = (row['xmax'] + row['xmin']) / 2 + 100
        if row['name'] == "radio-signal":
            signal_middle.append([index, middle])

        if row['name'] == "numbers" and i < 2:
            i += 1
            xy = [100 + int(row['ymin']), 110 + int(row['ymax']), 100 + int(row['xmin']), 110 + int(row['xmax'])]
            crop_num = screen_array[xy[0]:xy[1], xy[2]:xy[3], :]
            text = pytesseract.image_to_string(crop_num)
            if len(text) == 5:
                text_abs = abs(text_abs - int(text))
                dist_coords = abs(dist_coords - middle)
                freq_step = dist_coords / text_abs
                num_middle.append([index, middle, int(text)])

            if len(text) == 5 and i == 2:
                print(text_abs, "text abs")
                print(dist_coords, "distance between number coordinates ")
                print(freq_step, "how many pixels is one frequency")

            if len(text) != 5:
                print("invalid detection!", len(text))

            print("frequency", text)
            input("press enter to continue")
            # cv2.imshow("cropped number", crop_num)

    freq_for_sig = ((signal_middle[0][1] - num_middle[0][1]) / freq_step) + num_middle[0][2]
    print(freq_for_sig,  "frequency for signal")
    freq_for_sig = ((signal_middle[1][1] - num_middle[0][1]) / freq_step) + num_middle[0][2]
    print(freq_for_sig, "frequency for signal")
    freq_for_sig = ((signal_middle[2][1] - num_middle[0][1]) / freq_step) + num_middle[0][2]
    print(freq_for_sig, "frequency for signal")
    input("continue?")

    # if str(row['class']) == "0":
    #     print("SIGNAL FOUND")
    # if float(row['confidence']) > 0.7:
    #     print("HIT")

    # show live-detection
    cv2.imshow('SDR-signal', np.squeeze(results.render()))

    # pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
    # text = pytesseract.image_to_string(r"C:\Users\Pauli\Documents\ShareX\Screenshots/2022-10/586.png")
    # test = 'this is text' + text
    # print(test)
    #
    # input("Press Enter to continue...")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
