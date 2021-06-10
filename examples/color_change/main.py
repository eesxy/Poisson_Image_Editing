import numpy as np
import cv2 as cv
import sys
sys.path.append('..')
sys.path.append('../Poisson_Image_Editing/')
from Poisson_Image_Editing.preprocessing import PreProcessing
from Poisson_Image_Editing.kernel import Poisson

if __name__ == '__main__':
    src = cv.imread('./examples/color_change/1.jpeg')
    pre = PreProcessing()
    pre.selectSrc(src)

    retImg = Poisson.colorChange(cv.cvtColor(src, cv.COLOR_BGR2RGB), pre.selectedMask, 1.5, 0.5, 0.5)
    retImg = cv.cvtColor(retImg, cv.COLOR_RGB2BGR)
    cv.imshow('result', retImg)
    cv.waitKey(0)
    cv.destroyAllWindows()

    cmpImg = cv.colorChange(src, pre.selectedMask, red_mul=1.5, green_mul=0.5, blue_mul=0.5)
    cv.imshow('compare', cmpImg)
    cv.waitKey(0)
    cv.destroyAllWindows()
