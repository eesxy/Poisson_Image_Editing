import numpy as np
import cv2 as cv
from scipy.sparse import lil_matrix, linalg


class Poisson:
    # 用户接口
    # src, dst大小不必相同, 通道数必须相同, mask对应src遮罩, point为dst对应拷贝位置的中心点
    @classmethod
    def seamlessClone(cls, src, dst, mask, point, flags=None):
        laplacian = cv.Laplacian(np.float64(src), -1, ksize=1)
        inner = np.nonzero(mask)
        # 取出蒙版指定的位置
        xbegin, xend, ybegin, yend = np.min(inner[0])-1, np.max(inner[0]) + 2,\
            np.min(inner[1])-1, np.max(inner[1])+2
        cutMask = mask[xbegin:xend, ybegin:yend]
        cutSrc = src[xbegin:xend, ybegin:yend]
        cutLap = laplacian[xbegin:xend, ybegin:yend]
        # 可移动的最小, 最大位置
        minPoint = ((np.max(inner[0])-np.min(inner[0]))//2+1,
                    (np.max(inner[1])-np.min(inner[1]))//2+1)
        maxPoint = (dst.shape[0]-cutSrc.shape[0]+minPoint[0],
                    dst.shape[1]-cutSrc.shape[1]+minPoint[1])
        # 选区过大
        if cutSrc.shape[0] > dst.shape[0] or cutSrc.shape[0] > dst.shape[0]:
            raise UserWarning
        # 越界
        if point[0] < minPoint[0] or point[1] < minPoint[1] or point[0] > maxPoint[0] or point[1] > maxPoint[1]:
            raise UserWarning
        # 复制到对应位置
        reMask = np.zeros((dst.shape[0], dst.shape[1]))
        reSrc = np.zeros_like(dst)
        reLap = np.zeros_like(dst, dtype=np.float64)
        xbegin, xend, ybegin, yend = \
            point[0]-minPoint[0], cutMask.shape[0]+point[0]-minPoint[0], \
            point[1]-minPoint[1], cutMask.shape[1]+point[1]-minPoint[1]
        reMask[xbegin:xend, ybegin:yend] = cutMask
        reSrc[xbegin:xend, ybegin:yend] = cutSrc
        reLap[xbegin:xend, ybegin:yend] = cutLap
        # 逐通道求解
        ret = [cls._solve(s, d, reMask, l) for s, d, l in zip(
            cv.split(reSrc), cv.split(dst), cv.split(reLap))]
        retImg = cv.merge(ret)
        return retImg

    # scipy.sparse稀疏矩阵LU分解求解线性方程组
    # 此内部函数要求src, dst, mask已预处理, uint8存储, src, dst尺寸相同, 单通道, mask即拷贝位置
    @classmethod
    def _solve(cls, src, dst, mask, laplacian):
        inner = np.nonzero(mask)
        size = inner[0].shape[0]
        mmap = {(x, y): i for i, (x, y) in enumerate(zip(inner[0], inner[1]))}
        dx, dy = [1, 0, -1, 0], [0, 1, 0, -1]
        A, b = lil_matrix((size, size), dtype=np.float64), np.ndarray(
            (size, ), dtype=np.float64)
        # 构造系数矩阵
        for i, (x, y) in enumerate(zip(inner[0], inner[1])):
            A[i, i] = -4
            b[i] = laplacian[x, y]
            p = [(x+dx[j], y+dy[j]) for j in range(4)]
            for j in range(4):
                if p[j] in mmap:
                    A[i, mmap[p[j]]] = 1
                else:
                    b[i] -= dst[p[j]]
        A = A.tocsc()
        LU = linalg.splu(A)
        X = LU.solve(b)
        ret = np.copy(dst)
        for i, (x, y) in enumerate(zip(inner[0], inner[1])):
            ret[x, y] = min((255, max((0, X[i]))))
        return ret
