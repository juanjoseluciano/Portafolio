import sys
from PyQt5 import QtWidgets 
from PyQt5 import QtGui 
from PyQt5 import QtCore
from PIL.ImageQt import ImageQt
from form import Ui_MainWindow#import forms made in designer
import grayscale
import automatic_thresholding
import cv2

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)#call setupUi
        self.image_path = ""
        
        self.pushButton.clicked.connect(self.loadImage)
        self.pushButton_2.clicked.connect(self.imageProcessing)
        self.pushButton_3.clicked.connect(self.save_image)

        # End main UI code
        self.show()
        
    def loadImage(self):
        self.image_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, "Select an image",
            QtCore.QDir.homePath(), "Images (*.png *.jpg)")
        
        self.label.clear()
        self.label_2.clear()
        self.label_8.clear()
        self.graphicsView.clear()
        
        pixmap = QtGui.QPixmap(self.image_path)
        smaller_pixmap = pixmap.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(QtGui.QPixmap(smaller_pixmap))

    def imageProcessing(self):

        if self.image_path == "":
            dlg = QtWidgets.QMessageBox(self)
            dlg.setText("First select an image")
            button = dlg.exec_()
            self.loadImage()
        
        self.label_2.clear()
        self.label_8.clear()
        self.graphicsView.clear()
        
        if self.comboBox.currentText() == "":
            dlg_1 = QtWidgets.QMessageBox(self)
            dlg_1.setText("Select a Thresholding method, default Otsu method")
            button = dlg_1.exec_()
            thresholding_method = getattr(automatic_thresholding, 'otsu_threshold')

        elif self.comboBox.currentText() == "Isodata Thresholding":
            thresholding_method = getattr(automatic_thresholding, 'isodata_threshold')
        elif self.comboBox.currentText() == "Fast Isodata Thresholdining":
            thresholding_method = getattr(automatic_thresholding, 'fast_isodata_threshold')
        elif self.comboBox.currentText() == "Otsu Thresholding":
            thresholding_method = getattr(automatic_thresholding, 'otsu_threshold')

        self.grayscale_image = grayscale.grayscale_conversion(self.image_path)
        histogram = grayscale.grayscale_histogram(self.grayscale_image)
        self.binary_image = thresholding_method(self.grayscale_image, histogram)
        
        image = ImageQt(self.grayscale_image)
        pixmap = QtGui.QPixmap.fromImage(image)
        smaller_pixmap = pixmap.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(QtGui.QPixmap(smaller_pixmap))        

        image_2 = ImageQt(self.binary_image)
        pixmap = QtGui.QPixmap.fromImage(image_2)
        smaller_pixmap_2 = pixmap.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio)
        self.label_8.setPixmap(QtGui.QPixmap(smaller_pixmap_2))

        #self.graphicsView.setBackground("w")
        self.graphicsView.plot(histogram)
        
    def save_image(self):
        if self.image_path == "":
            dlg = QtWidgets.QMessageBox(self)
            dlg.setText("First select an image")
            button = dlg.exec_()
            self.loadImage()
            self.imageProcessing()
        
        save_file, _ = QtWidgets.QFileDialog.getSaveFileName(
            None, "Save your image",
            QtCore.QDir.homePath(), "PNG Images (*.png)")
        
        if save_file:
##            self.grayscale_image.save(save_file, "PNG")
            self.binary_image.save(save_file, "PNG")
            dlg = QtWidgets.QMessageBox(self)
            dlg.setText("Image saved successfully")
            button = dlg.exec_()
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
