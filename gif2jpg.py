# convert gif to jpg

import numpy as np
import cv2 as cv
 
def gif2jpg(gif_path, jpg_path):
    gif = cv.VideoCapture(gif_path)
    ret, frame = gif.read()
    cv.imwrite(jpg_path, frame)
    return
 
if __name__ == '__main__':
    gif_path = './figures/source'
    jpg_path = './figures/results'