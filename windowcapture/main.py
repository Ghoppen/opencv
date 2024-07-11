import cv2 as cv
import numpy as np
import os
from time import sleep, time
import win32gui , win32ui, win32con


#directory change to file directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
cropped_x = 0
cropped_y = 0
offset_x = 0
offset_y = 0

#wincap = CaptureWindow('Tanker-1')
def getScreenshot(windowName,):
    border = 8
    titlebar = 30
    hwnd = win32gui.FindWindow(None, windowName)
    windowRect = win32gui.GetWindowRect(hwnd)
    l,t,r,b = win32gui.GetWindowRect(hwnd)
    h = b-t
    w = r-l
    global cropped_x 
    cropped_x = border
    global cropped_y
    cropped_y = titlebar
    global offset_x
    global offset_y
    offset_x = windowRect[0] + cropped_x
    offset_y = windowRect[1] + cropped_y

    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()     
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0), (w, h) , dcObj, (0,0), win32con.SRCCOPY)
    signedIntArray = dataBitMap.GetBitmapBits(False)
    img = np.array(signedIntArray).astype(dtype="uint8")
    img.shape = (h,w,4)
    #delete stuff
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    img = img[...,:3]
    img = np.ascontiguousarray(img)

    return img

def get_screen_position(self, pos):
    return (pos[0] + offset_x, pos[1] + offset_y)

def findClickPosition(needle_img_path, haystack_img,threshold =0.5,debug_mode ='rectangles'):
    needle_img = cv.imread(needle_img_path,cv.IMREAD_UNCHANGED)

    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]

    #Best results in this case using TM_SQDIFF_NORMED
    method = cv.TM_CCOEFF_NORMED
    result = cv.matchTemplate(haystack_img,needle_img,method)
    
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))
    
    rectangles = []
    for loc in locations:
        rect = [int(loc[0]),int(loc[1]),needle_w,needle_h]
        rectangles.append(rect)

    rectangles,weights = cv.groupRectangles(rectangles,1,0.5)
    points = []
    if len(rectangles):
        print('found needle. ')
        line_color = (0,255,0)
        line_type = cv.LINE_4
        marker_color = (255,0,255)
        marker_type = cv.MARKER_CROSS
        #loop over locations and draw rectangles
        for(x,y,w,h) in rectangles:
            #center position
            center_x = x +int(w/2)
            center_y = y + int(h/2)
            #save center points
            points.append((center_x,center_y))
            if debug_mode == 'rectangles':
                top_left = (x,y)
                bottom_right = (x+w,y+h)
                cv.rectangle(haystack_img,top_left,bottom_right,line_color,line_type)
            elif debug_mode == 'points':
                cv.drawMarker(haystack_img,(center_x,center_y),marker_color,marker_type)
    if debug_mode:
        cv.imshow('Matches',haystack_img)
     # cv.waitKey()
    return points

def main():   
    loop_time = time()
    while(True):
        screenshot = getScreenshot('Tanker-1')
        sleep(2)
        start = findClickPosition('start.jpg',screenshot,threshold=0.6)
        rematch = findClickPosition('rematch.jpg',screenshot,threshold=0.6)
        ok_pos = findClickPosition('ok.jpg',screenshot,threshold=0.6)
        
        #screenshot = ImageGrab.grab()
        #screenshot = np.array(screenshot)
        #screenshot = cv.cvtColor(screenshot,cv.COLOR_RGB2BGR)
        #cv.imshow('Computer Vion', screenshot)
        #print('FPS {}'.format(1/ (time()-loop_time)))
        #loop_time = time()
        # pressing q exists
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break







main()
