import numpy as np
import cv2 as cv
import sys
sys.path.append('..')
sys.path.append('../Poisson_Image_Editing/')
from Poisson_Image_Editing.preprocessing import PreProcessing
from Poisson_Image_Editing.kernel import Poisson

if __name__ == '__main__':
    src = cv.imread('./examples/illumination_change/1.jpeg')
    pre = PreProcessing()
    pre.selectSrc(src)

    retImg = Poisson.illuminationChange(src, pre.selectedMask, 0.1, 0.2)
    cv.imshow('result', retImg)
    cv.waitKey(0)
    cv.destroyAllWindows()

    cmpImg = cv.illuminationChange(src, pre.selectedMask, alpha=0.1, beta=0.2)
    cv.imshow('compare', cmpImg)
    cv.waitKey(0)
    cv.destroyAllWindows()
