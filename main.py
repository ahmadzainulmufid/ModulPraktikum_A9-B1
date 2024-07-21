import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from matplotlib import pyplot as plt

class ShowImage(QMainWindow):
    def __init__(self):
        super(ShowImage, self).__init__()
        loadUi('showgui.ui', self)
        self.Image = None

        #button load
        self.button_loadImage.clicked.connect(self.fungsi)
        self.button_saveImage.clicked.connect(self.grayScale)

        #operasi histogram
        self.actionHistogram_Gray.triggered.connect(self.grayHistogram)
        self.actionHistogram_RGB.triggered.connect(self.rgbHistogram)
        self.actionHistogram_Equal.triggered.connect(self.equalHistogram)

        #operasi geometri
        self.actionTranslasi.triggered.connect(self.translasi)

    def fungsi(self):
        self.Image = cv2.imread('test.jpg')
        self.displayImage(1)

    def grayScale(self):
        if self.Image is not None:
            gray = cv2.cvtColor(self.Image, cv2.COLOR_BGR2GRAY)
            self.Image = gray
            self.displayImage(2)

    def grayHistogram(self):
        plt.hist(self.Image.ravel(), 255, [0, 255])
        plt.show()

    def rgbHistogram(self):
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            histo = cv2.calcHist([self.Image], [i], None, [256], [0, 256])
            plt.plot(histo, color=col)
            plt.xlim([0, 256])
        plt.show()

    def equalHistogram(self):
        hist, bins = np.histogram(self.Image.flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_normalized = cdf * hist.max() / cdf.max()
        cdf_m = np.ma.masked_equal(cdf, 0)
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
        cdf = np.ma.filled(cdf_m, 0).astype("uint8")
        self.displayImage(2)

        plt.plot(cdf_normalized, color="b")
        plt.hist(self.Image.flatten(), 256, [0, 256], color="r")
        plt.xlim([0, 256])
        plt.legend(("cdf", "histogram"), loc="upper left")
        plt.show()

    def translasi(self):
        h, w = self.Image.shape[:2]
        quarter_h,quarter_w = h/4,w/4
        T = np.float32([[1,0,quarter_w], [0,1,quarter_h]])
        img = cv2.warpAffine(self.Image,T,(w,h))
        self.Image = img
        self.displayImage(2)

    def displayImage(self, window=1):   
        if self.Image is not None:
            qformat = QImage.Format_Indexed8

            if len(self.Image.shape) == 3:
                if self.Image.shape[2] == 4:
                    qformat = QImage.Format_RGBA8888
                else:
                    qformat = QImage.Format_RGB888

            img = QImage(self.Image, self.Image.shape[1], self.Image.shape[0], self.Image.strides[0], qformat)
            img = img.rgbSwapped()

            if window == 1:
                self.label.setPixmap(QPixmap.fromImage(img))
            elif window == 2:
                self.label_2.setPixmap(QPixmap.fromImage(img))


app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('Kelompok 3')
window.show()
sys.exit(app.exec_())