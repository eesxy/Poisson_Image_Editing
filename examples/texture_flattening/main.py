import numpy as np
import cv2 as cv
import sys
sys.path.append('..')
sys.path.append('../Poisson_Image_Editing/')
from Poisson_Image_Editing.preprocessing import PreProcessing
from Poisson_Image_Editing.kernel import Poisson

if __name__ == '__main__':
    src = cv.imread('./examples/texture_flattening/1.jpg')
    pre = PreProcessing()
    pre.selectSrc(src)

    retImg = Poisson.textureFlattening(src, pre.selectedMask, 80, 120)
    cv.imshow('result', retImg)
    cv.waitKey(0)
    cv.destroyAllWindows()

    cmpImg = cv.textureFlattening(src, pre.selectedMask, low_threshold=80, high_threshold=120)
    cv.imshow('compare', cmpImg)
    cv.waitKey(0)
    cv.destroyAllWindows()
