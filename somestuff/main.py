import cv2 as cv
import numpy as np
from time import time,sleep
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter
import pyautogui
from threading import Thread
from detection import Detection


# initialize the WindowCapture class
wincap = WindowCapture('Tanker-1')
vision_ok = Vision('ok.jpg')
vision_rematch = Vision('rematch.jpg')
vision_start = Vision('start.jpg')
vision_mitra = Vision('mitra.jpg')
vision_start_game = Vision('start_game.jpg')
is_bot_in_action = False

#vision_mitra.init_control_gui()
#hsv_filter = HsvFilter(0,12,12,12,12,12,12,12,12,12,21)
def bot_Actions(rectangles):
    if len(rectangles) > 0:
        targets = vision_start.get_click_points(rectangles)
        #target = wincap.get_screen_position(targets[0])
        target = wincap.get_relative_mouse_coordinates()
        wincap.click_on_certain_position(target)
    global is_bot_in_action
    is_bot_in_action = False

loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    #processed_output = vision_start.apply_hsv_filter(screenshot,hsv_filter)
    #cv.imshow('Matches',output)
    #rectangles = vision_start_processed_needle.find(processed_output, threshold=0.5)
    # do object detection
    rectangles = vision_start.find(screenshot, threshold=0.60)
   
    #draw image
    output_image = vision_start.draw_rectangles(screenshot,rectangles)

    #display processed image
    cv.imshow('Matches',output_image) 
    #bot actions
    if not is_bot_in_action:
        is_bot_in_action = True
        t = Thread(target=bot_Actions,args=(rectangles,))
        t.start()

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')