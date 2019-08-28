from test import Ui_CamShow
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog
from PyQt5.QtCore import QTimer,QCoreApplication
from PyQt5.QtGui import QPixmap
import cv2
import qimage2ndarray
import time
from PyQt5.QtCore import Qt,QRect
import numpy as np
import pyqtgraph
from PyQt5 import QtGui,QtCore

class CamShow(QMainWindow,Ui_CamShow):
    def __init__(self,parent=None):
        super(CamShow,self).__init__(parent)
        self.setupUi(self)
        self.PrepWidgets()
        self.PrepParameters()
        self.CallBackFunctions()
        self.Timer = QTimer()
        self.Timer.timeout.connect(self.TimerOutFun)
        self.stopbt = 0
        self.AvgPlot.plotItem.showGrid(True, True, 0.7)
        

    #控件初始化
    def PrepWidgets(self):
        self.PrepCamera()
        self.StopBt.setEnabled(False)
        self.RecordBt.setEnabled(False)

    def PrepCamera(self):
        self.camera=cv2.VideoCapture(0)
  

    def PrepParameters(self):
        self.RecordFlag=0
        self.RecordPath='D:/Python/PyQt/'
        self.FilePathLE.setText(self.RecordPath)
        self.Image_num=0
        

    def CallBackFunctions(self):
        self.FilePathBt.clicked.connect(self.SetFilePath)
        self.ShowBt.clicked.connect(self.StartCamera)
        self.StopBt.clicked.connect(self.StopCamera)
        self.RecordBt.clicked.connect(self.RecordCamera)
        self.ExitBt.clicked.connect(self.ExitApp)
        self.btnUpdate.clicked.connect(self.update)
        

    def StartCamera(self):
        self.ShowBt.setEnabled(False)
        self.StopBt.setEnabled(True)
        self.RecordBt.setEnabled(True)
        self.RecordBt.setText('Record')
        self.Timer.start(1)
        self.timelb=time.clock()

    def StopCamera(self):
        if self.StopBt.text() == 'Stop':
            self.StopBt.setText('Continue')
            #self.stopbt = 0
            self.RecordBt.setText('Save Pic')
            self.Timer.stop()
        else:
            self.StopBt.setText('Stop')
            #self.stopbt = 1
            self.RecordBt.setText('Record')
            self.Timer.start(1)


    def TimerOutFun(self):
        success,self.img=self.camera.read()
        self.gray = cv2.cvtColor(self.img,cv2.COLOR_RGB2GRAY) #轉灰階
        if success:   
            #self.Image = self.ColorAdjust(img)
            
            self.DispImg()
            self.CopyImg()            
            #self.Image_num+=1
            if self.RecordFlag:
                self.video_writer.write(self.img)

    def CopyImg(self):
        ret=QRect(50,200,411,10)       
        CVimg = cv2.cvtColor(self.gray,cv2.COLOR_BGR2RGB)       
        qimg = qimage2ndarray.array2qimage(CVimg)
        b=qimg.copy(ret)

        self.DispCopyImg.setPixmap(QPixmap(b))
        self.DispCopyImg.show()

                       
    
    def DispImg(self):
        CVimg = cv2.cvtColor(self.gray,cv2.COLOR_BGR2RGB)
        qimg = qimage2ndarray.array2qimage(CVimg)
        self.DispLb.setPixmap(QPixmap(qimg))
        self.DispLb.show()

    
    def SetFilePath(self):
        dirname = QFileDialog.getExistingDirectory(self, "瀏覽", '.')
        if dirname:

            self.FilePathLE.setText(dirname)
            self.RecordPath=dirname+'/'

    def RecordCamera(self):
        tag=self.RecordBt.text()
        if tag=='Save Pic':
            image_name=self.RecordPath+'self.image'+time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'.jpg'
            print(image_name)
            cv2.imwrite(image_name,self.img)
            
        elif tag =='Record':
            self.RecordBt.setText('Stop')
            video_name = self.RecordPath + 'video' + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '.avi'
            size = (self.img.shape[1],self.img.shape[0])
            fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
            self.video_writer = cv2.VideoWriter(video_name, fourcc,self.camera.get(5), size)
            self.RecordFlag=1
            self.StopBt.setEnabled(False)
            self.ExitBt.setEnabled(False)

        elif tag == 'Stop':
            self.RecordBt.setText('Record')
            self.video_writer.release()
            self.RecordFlag = 0
            self.StopBt.setEnabled(True)
            self.ExitBt.setEnabled(True)

    def showUpdate(self):
        t=time.clock()
        points=100 #number of data points
        X=np.arange(points)
        Y=np.sin(np.arange(points)/points*3*np.pi+time.time())
        C=pyqtgraph.hsvColor(time.time()/5%1,alpha=.5)
        pen=pyqtgraph.mkPen(color=C,width=5)
        self.AvgPlot.plot(X,Y,pen=pen,clear=True)
           
    
    def update(self):
        t1=time.clock()
        points=100 #number of data points
        X=np.arange(points)
        Y=np.sin(np.arange(points)/points*3*np.pi+time.time())
        C=pyqtgraph.hsvColor(time.time()/5%1,alpha=.5)
        pen=pyqtgraph.mkPen(color=C,width=5)
        self.AvgPlot.plot(X,Y,pen=pen,clear=True)
        print("update took %.02f ms"%((time.clock()-t1)*1000))        
        QtCore.QTimer.singleShot(1, self.update) # QUICKLY repeat

    def ExitApp(self):
        self.Timer.Stop()
        self.camera.release()
        QCoreApplication.quit()
        
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui=CamShow()
    ui.show()   
    ui.showUpdate() #start with showUadapte()   
    sys.exit(app.exec_())
