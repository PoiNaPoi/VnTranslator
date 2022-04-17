import sys
import os
from os.path import basename
from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import tkinter as tk
from PIL import ImageGrab
import PIL
import easyocr
import cutlet
from deep_translator import GoogleTranslator

class Menu(QWidget):

    default_title = "VnTranslator"
    reader = easyocr.Reader(['ja'])
    iconSize = 100
    Lable = []
    check_box_Scanning_State = True
    check_box_Romanji_State = False
    ErrorHandle_continue_snip_button = True
    ErrorHandle_continue_snip_button2 = True

    def __init__(self):
        super().__init__()

        self.title = Menu.default_title
        self.setWindowTitle(self.title)
        self.SRC = 'ja'
        self.DEST = 'en'
        self.katsu = cutlet.Cutlet()
        self.setGeometry(300, 300, 800, 300)
        self.setWindowIcon(QtGui.QIcon('icon/logo.png'))

        textLog_f = open("Log\\textLog.txt", "w", encoding='utf8')
        choiceLog_f = open("Log\\choiceLog.txt", "w", encoding='utf8')
        textLog_f.close()
        choiceLog_f.close()
        
        crop_button = QPushButton("Select Text Area", self)
        crop_button.setGeometry(0, 0, self.iconSize, self.iconSize)
        crop_button.clicked.connect(self.new_image_window)
        crop_button.clicked.connect(lambda action: changeStatusBar("The text area has been selected !!"))
        crop_button.setIcon(QIcon('icon/select.png'))
        crop_button.setIconSize(QtCore.QSize(self.iconSize, self.iconSize))
        crop_button.setToolTip('Click to Choose Area to Translate !!')

        translate_button = QPushButton("Translate Text", self)
        translate_button.setGeometry(0, 0, self.iconSize, self.iconSize)
        translate_button.clicked.connect(self.continue_snip_button)
        translate_button.clicked.connect(lambda action: Translate_Text())
        translate_button.setIcon(QIcon('icon/nabipop2.png'))
        translate_button.setIconSize(QtCore.QSize(self.iconSize, self.iconSize))
        translate_button.setToolTip('Click to Translate the Selected Area !!')

        crop_choice = QPushButton("Select Choice Area", self)
        crop_choice.setGeometry(0, 0, self.iconSize, self.iconSize)
        crop_choice.clicked.connect(self.new_image_window2)
        crop_choice.clicked.connect(lambda action: changeStatusBar("The choice area has been selected !!"))
        crop_choice.setIcon(QIcon('icon/select.png'))
        crop_choice.setIconSize(QtCore.QSize(self.iconSize, self.iconSize))
        crop_choice.setToolTip('Click to Choose Area to Translate Choice !!')

        choice_translate_button = QPushButton("Translate Choice", self)
        choice_translate_button.setGeometry(0, 0, self.iconSize, self.iconSize)
        choice_translate_button.clicked.connect(self.continue_snip_button2)
        choice_translate_button.clicked.connect(lambda action: Translate_Selective_Choice())
        choice_translate_button.setIcon(QIcon('icon/nabipop2.png'))
        choice_translate_button.setIconSize(QtCore.QSize(self.iconSize, self.iconSize))
        choice_translate_button.setToolTip('Click to Translate the Selected Choice Area !!')

        check_box_Scanning = QCheckBox("Display Scanning Text",self)
        check_box_Scanning.setChecked(True)
        check_box_Scanning.stateChanged.connect(self.check_box_Scanning_Show)
        check_box_Scanning.stateChanged.connect(lambda action: display_text())

        check_box_Romanji = QCheckBox("Display Romaji Text",self)
        check_box_Romanji.setChecked(False)
        check_box_Romanji.stateChanged.connect(self.check_box_Romanji_Show)
        check_box_Romanji.stateChanged.connect(lambda action: display_text())

        label = QLabel("")
        label.setFont(QFont('Arial', 12))

        formLayout = QFormLayout()
        formLayout.addRow(label)

        groupBox = QGroupBox()
        groupBox.setLayout(formLayout)

        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)

        checkBox_layout = QVBoxLayout(self)
        checkBox_layout.addWidget(check_box_Scanning)
        checkBox_layout.addWidget(check_box_Romanji)

        menuBar = QHBoxLayout(self)
        menuBar.addWidget(crop_button)
        menuBar.addWidget(translate_button)
        menuBar.addWidget(crop_choice)
        menuBar.addWidget(choice_translate_button)
        menuBar.addLayout(checkBox_layout)

        label2 = QLabel("Press Select Text Area button to select area for translating the text")
        statusbaR = QHBoxLayout(self)
        statusbaR.addWidget(label2)
        
        layout.addLayout(menuBar)
        layout.addLayout(statusbaR)

        def changeStatusBar(text):
            label2.setText(text)

        def Translate_Selective_Choice():
            if self.ErrorHandle_continue_snip_button2 == False:
                changeStatusBar("Please Select Choice Area Before Translate !!")
                return

            translated = GoogleTranslator(source = self.SRC, target = self.DEST)
            readPicture = self.reader.readtext("capture.png")
            now = datetime.now()
            wordScanning = ""
            # wordRomaji = ""
            wordTranslate = ""
            round = 0

            for box in readPicture:
                if(round!=0):
                    wordTranslate = wordTranslate + " "
                wordTranslate = wordTranslate + box[1]
                round = round + 1

            try:
                translated.translate(wordTranslate)
            
            except:
                changeStatusBar('Text not found !!')

            else:
                round = 0
                for box in readPicture:
                    choiceLog_f = open("Log\\choiceLog.txt", "a", encoding='utf8')
                    if(round==0):
                        wordTranslate = str(round+1) + ') ' + translated.translate(box[1])
                        wordScanning = str(round+1) + ') ' + box[1]
                        choiceLog_f.writelines(box[1])
                    else:
                        wordTranslate = wordTranslate + '\n' + str(round+1) + ') ' + translated.translate(box[1])
                        wordScanning = wordScanning + '\n' + str(round+1) + ') ' + box[1]
                        choiceLog_f.writelines('|'+box[1])
                    round = round + 1

                choiceLog_f.writelines('\n')
                choiceLog_f.close()

                self.Lable.append([
                    '---[ ' + str(len(self.Lable)+1) + ' ]-[ ' + str(now.strftime("%H:%M:%S")) + ' ]------------------------------------------------------------------------------------------------------------------',
                    wordScanning,
                    '',
                    wordTranslate
                ])
                changeStatusBar("The text has been translated !!")
                display_text()

            self.removePNG()

        def Translate_Text():
            if self.ErrorHandle_continue_snip_button == False:
                changeStatusBar("Please Select Text Area Before Translate !!")
                return
            translated = GoogleTranslator(source = self.SRC, target = self.DEST)
            readPicture = self.reader.readtext("capture.png")
            now = datetime.now()
            wordScanning = ""
            wordRomaji = ""
            wordTranslate = ""
            round = 0

            for box in readPicture:
                if(round!=0):
                    wordScanning = wordScanning + " "
                wordScanning = wordScanning + box[1]
                round = round + 1

            try:
                wordTranslate = translated.translate(wordScanning)

            except:
                changeStatusBar('Text not found !!')
            
            else:     
                textLog_f = open("Log\\textLog.txt", "a", encoding='utf8')
                textLog_f.writelines(wordScanning + '\n')
                textLog_f.close()

                wordRomaji = self.katsu.romaji(wordScanning)
                self.Lable.append([
                    '---[ ' + str(len(self.Lable)+1) + ' ]-[ ' + str(now.strftime("%H:%M:%S")) + ' ]------------------------------------------------------------------------------------------------------------------',
                    'Scanning  : ' + wordScanning,
                    'Romaji  : ' + wordRomaji,
                    'Translate : ' + wordTranslate
                ])

                changeStatusBar("The choice have been translated !!")
                display_text()

            self.removePNG()

        def display_text():
            Text = ""
            for lable in self.Lable[::-1]:
                row = 0
                for word in lable:
                    if row == 0 and word != "":
                        Text = Text + word + "\n"
                    elif row == 1 and word != "" and self.check_box_Scanning_State:
                        Text = Text + word + "\n"
                    elif row == 2 and word != "" and self.check_box_Romanji_State:
                        Text = Text + word + "\n"
                    elif row == 3 and word != "":
                        Text = Text + word + "\n"
                    row = row + 1
                Text = Text + "\n"
            label.setText(Text)

    def removePNG(self):
        if os.path.exists('capture.png'):
            os.remove('capture.png')

    def new_image_window(self):
        self.myWidget = MyWidget()
        self.myWidget.show()

    def new_image_window2(self):
        self.myWidget2 = MyWidget()
        self.myWidget2.show()

    def continue_snip_button(self):
        try:
            self.myWidget.continueCaptureEvent()

        except:
            self.ErrorHandle_continue_snip_button = False

        else:
            self.ErrorHandle_continue_snip_button = True

    def continue_snip_button2(self):
        try:
            self.myWidget2.continueCaptureEvent()

        except:
            self.ErrorHandle_continue_snip_button2 = False

        else:
            self.ErrorHandle_continue_snip_button2 = True

    def closeEvent(self, event):
        event.accept()

    def check_box_Scanning_Show(self, state):
        if state == QtCore.Qt.Checked:
            self.check_box_Scanning_State = True
        else:
            self.check_box_Scanning_State = False

    def check_box_Romanji_Show(self, state):
        if state == QtCore.Qt.Checked:
            self.check_box_Romanji_State = True
        else:
            self.check_box_Romanji_State = False

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)

        self.X1 = 0
        self.Y1 = 0
        self.X2 = 0
        self.Y2 = 0

        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        self.X1 = x1
        self.Y1 = y1
        self.X2 = x2
        self.Y2 = y2

        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.ArrowCursor)
        )

    def continueCaptureEvent(self):
        self.close()
        img = ImageGrab.grab(bbox=(self.X1, self.Y1, self.X2, self.Y2))
        img.save('capture.png')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = Menu()
    mainMenu.show()
    sys.exit(app.exec_())