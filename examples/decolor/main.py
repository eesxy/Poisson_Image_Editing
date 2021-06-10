import numpy as np
import cv2 as cv
import sys
sys.path.append('..')
sys.path.append('../Poisson_Image_Editing/')
from Poisson_Image_Editing.preprocessing import PreProcessing
from Poisson_Image_Editing.kernel import Poisson

if __name__ == '__main__':
    src = cv.imread('./examples/decolor/1.jpeg')
    pre = PreProcessing()
    pre.selectSrc(src)

    retImg = Poisson.deColor(src, pre.selectedMask)
    cv.imshow('result', retImg)
    cv.waitKey(0)
    cv.destroyAllWindows()
