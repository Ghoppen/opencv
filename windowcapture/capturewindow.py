import cv2 as cv
import numpy as np
import os
import pyautogui
from time import time
from PIL import ImageGrab
import win32gui , win32ui, win32con

class CaptureWindow:
    w = 0 # set this
    h = 0 # set this
    hwnd = None

    def __init__(self,windowName):
        self.hwnd = win32gui.FindWindow(None, windowName)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(windowName))
        self.w = 1920
        self.h = 1080
    @staticmethod
    def list_window_names():
        def winEnumHandler( hwnd, ctx ):
            if win32gui.IsWindowVisible( hwnd ):
                print (hex(hwnd), win32gui.GetWindowText( hwnd ))

        win32gui.EnumWindows( winEnumHandler, None )

    def windowCapture(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0), (self.w, self.h) , dcObj, (0,0), win32con.SRCCOPY)
        #dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)
        signedIntArray = dataBitMap.GetBitmapBits(False)
        img = np.array(signedIntArray).astype(dtype="uint8")
        img.shape = (self.h,self.w,4)
        #img.shape(h,w,4)
        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        img = img[...,:3]
        img = np.ascontiguousarray(img)
        return img

  