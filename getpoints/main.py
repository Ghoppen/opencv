import cv2 as cv
import numpy as np

def findClickPosition(needle_img_path, haystack_img_path,threshold =0.8,debug_mode =None):
    haystack_img = cv.imread(haystack_img_path,cv.IMREAD_UNCHANGED)
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
        cv.waitKey()
    return points


points = findClickPosition('ok.jpg','full.jpg', debug_mode='rectangles')
print(points)



    #get best match position
   # min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    #if max_val >= threshold:
    #    print('found')
        #dimensions of ok image
       
    #    top_left = max_loc
    #    bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
        
    #    cv.drawMarker(haystack_img,(center_x,center_y),marker_color,marker_type)
    #    cv.rectangle(haystack_img,top_left,bottom_right,
   #                         color=(0,255,0),thickness=2,lineType=cv.LINE_4)
    #    cv.imshow('Result',haystack_img)
    #    cv.waitKey()                    
  #  else:
    #    print('not found')
#
    #locations = np.where(result>=threshold)
    #::-1 reverse list, * unpack list, zip merge list
    #creates a list of tuples with reverse values and combines items from each list
    #locations = list(zip(*locations[::-1]))

