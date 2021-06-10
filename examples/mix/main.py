import numpy as np
import cv2 as cv
import sys
import time
sys.path.append('..')
sys.path.append('../Poisson_Image_Editing/')
from Poisson_Image_Editing.preprocessing import PreProcessing
from Poisson_Image_Editing.kernel import Poisson

if __name__ == '__main__':
    src = cv.imread('./examples/mix/1.jpg')
    dst = cv.imread('./examples/mix/2.jpg')
    pre = PreProcessing()
    pre.select(src, dst)

    retImg = Poisson.seamlessClone(src, dst, pre.selectedMask, pre.selectedPoint, Poisson.MIXED_CLONE)
    cv.imshow('result', retImg)
    cv.waitKey(0)
    cv.destroyAllWindows()

    cmpImg = cv.seamlessClone(src, dst, pre.selectedMask, (pre.selectedPoint[1], pre.selectedPoint[0]), Poisson.MIXED_CLONE)
    cv.imshow('compare', cmpImg)
    cv.waitKey(0)
    cv.destroyAllWindows()
