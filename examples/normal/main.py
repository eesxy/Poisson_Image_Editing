import numpy as np
import cv2 as cv
import sys
sys.path.append('..')
sys.path.append('../Poisson_Image_Editing/')
from Poisson_Image_Editing.preprocessing import PreProcessing
from Poisson_Image_Editing.kernel import Poisson

if __name__ == '__main__':
    src = cv.imread('./examples/normal/1.jpeg',cv.IMREAD_GRAYSCALE)
    dst = cv.imread('./examples/normal/2.jpeg',cv.IMREAD_GRAYSCALE)
    pre = PreProcessing()
    pre.select(src, dst)

    retImg = Poisson.seamlessClone(src, dst, pre.selectedMask, pre.selectedPoint, Poisson.NORMAL_CLONE)
    cv.imshow('result', retImg)
    cv.waitKey(0)
    cv.destroyAllWindows()
