import sys
from requests import post
from PyQt5.QtGui import QIcon, QPixmap, QDoubleValidator, QCursor, QRegExpValidator
from PyQt5.QtWidgets import QMessageBox, QApplication, QLabel, QWidget, QMainWindow, QPushButton, QLineEdit
from PyQt5.QtCore import QThread, QObject, pyqtSignal, Qt, QRegExp, QTimer
import time
import httpx
import asyncio
from Cashier_Window import Cashier_Window
import json

with open("appsettings.json", 'r') as openfile:
    appsettings = json.load(openfile)


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # CashGenic Cube POS parameters
        self.CashGenic_IP_address = appsettings['CashGenic_IP']
        self.AcceptCashMayStop = appsettings['AcceptCashMayStop']
        self.Hide_Cashier_window_time = appsettings['Hide_Cashier_Info_TimeoutSec']
        self.Allow_Dispense_Operation = appsettings['AllowDispenseOperation']
        self.API_username = appsettings['API_username']
        self.API_password = appsettings['API_password']
        self.credentials = self.get_token()

        # Thread variables
        self.worker_1 = None
        self.pay_thread_1 = None
        self.w = None

        # SetupUI variables
        self.main_window = None
        self.label_image_1 = None
        self.label_image_2 = None
        self.label_image_3 = None
        self.label_image_4 = None
        self.label_image_5 = None
        self.label_image_6 = None
        self.label_image_7 = None
        self.label_image_8 = None
        self.CubeIQ_image = None
        self.CubeIQ_icon_image = None
        self.Euro_image = None
        self.POS_button_0 = None
        self.POS_button_1 = None
        self.POS_button_2 = None
        self.POS_button_3 = None
        self.POS_button_4 = None
        self.POS_button_5 = None
        self.POS_button_6 = None
        self.POS_button_7 = None
        self.POS_button_8 = None
        self.POS_button_9 = None
        self.POS_button_minus = None
        self.POS_button_comma = None
        self.POS_button_clear = None
        self.POS_button_arrow = None
        self.Entry_button_clear = None
        self.Entry_button_PayPod = None
        self.label_0 = None
        self.label_1 = None
        self.label_2 = None
        self.label_3 = None
        self.label_4 = None
        self.label_5 = None
        self.label_6 = None
        self.label_7 = None
        self.input_text_0 = None
        self.input_text_1 = None
        self.input_text_2 = None
        self.input_text_3 = None
        self.input_text_4 = None
        self.input_text_5 = None
        self.input_text_total_amount = None
        self.input_text_customer = None

        # The design
        self.setupUI()

        # Line Edit Focused has the last widget focused before the button is pressed
        self.lineEditFocused = None
        self.app = QApplication(sys.argv)
        self.app.focusChanged.connect(self.on_focusChanged)

        # Check if appsettings settings are right
        QTimer.singleShot(1, self.check_settings)

    # Get initial token of Cashgenic
    def get_token(self):
        CashGenic_token_answer = ''
        myobj = {
            'username': self.API_username,
            'password': self.API_password,
            'grant_type': ''
        }

        try:
            CashGenic_token_answer = post(url='https://' + self.CashGenic_IP_address + ':44333/token',
                                          headers={'Content-Type': 'application/x-www-form-urlencoded'}, verify=False,
                                          params=myobj)
        except (Exception,):
            pass
        return CashGenic_token_answer

    # Check if appsettings.json values are right
    def check_settings(self):
        if self.credentials == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error! Wrong settings.")
            msg.setWindowTitle("Error")
            msg.exec()
            self.Entry_button_PayPod.setEnabled(False)

    # The design of Cube POS
    def setupUI(self):

        style = '''
        QMainWindow {background: #00171f;}
        QLabel#Text_Label {font-size: 22px;   font-weight: 600;   background-image: linear-gradient(to left, #553c9a, #b393d3);   color: orange;   background-clip: text;   -webkit-background-clip: text;}
        QPushButton#POS_button {   background-color: #0a6bff;   border-radius: 4px;   border: 0;   box-shadow: rgba(1,60,136,.5) 0 -1px 3px 0 inset,rgba(0,44,97,.1) 0 3px 6px 0;   box-sizing: border-box;   color: #fff;   cursor: pointer;   display: inherit;   font-family: "Space Grotesk",-apple-system,system-ui,"Segoe UI",Roboto,Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";   font-size: 18px;   font-weight: 700;   line-height: 24px;   margin: 0;   min-height: 50px;   min-width: 35px;   padding: 16px 20px;   position: relative;   text-align: center;   user-select: none;   -webkit-user-select: none;   touch-action: manipulation;   vertical-align: baseline;   transition: all .2s cubic-bezier(.22, .61, .36, 1); } QPushButton:hover {   background-color: #065dd8;   transform: translateY(-2px); }
        QPushButton#Entry_button{   background-color: #0a6bff;   border-radius: 4px;   border: 0;   box-shadow: rgba(1,60,136,.5) 0 -1px 3px 0 inset,rgba(0,44,97,.1) 0 3px 6px 0;   box-sizing: border-box;   color: #fff;   cursor: pointer;   display: inherit;   font-family: "Space Grotesk",-apple-system,system-ui,"Segoe UI",Roboto,Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";   font-size: 18px;   font-weight: 700;   line-height: 24px;   margin: 0;   min-height: 50px;   min-width: 80px;   padding: 16px 20px;   position: relative;   text-align: center;   user-select: none;   -webkit-user-select: none;   touch-action: manipulation;   vertical-align: baseline;   transition: all .2s cubic-bezier(.22, .61, .36, 1); } QPushButton:hover {   background-color: #065dd8;   transform: translateY(-2px); }
        QLineEdit{{direction:rtl; font-size:32px; color: #EBEBEB; border: 0px solid black; background-color: {0}; color: #EBEBEB; border: 2px solid #ffa02f;}} QLineEdit:hover{{ border: 3px solid #FFFF00;}}
        '''

        input_style = """QLineEdit{{direction:rtl; font-size:32px; color: #EBEBEB; border: 0px solid black; background-color: {0}; color: #EBEBEB; border: 2px solid #ffa02f;}} QLineEdit:hover{{ border: 3px solid #FFFF00;}}""".format(
            '#262626')

        # Set Main Window Title
        self.setWindowTitle('CubePOS Ver.A1')

        # Create Central Widget
        self.main_window = QWidget()
        self.setCentralWidget(self.main_window)

        # Create Image Labels to add the Images
        self.label_image_1 = QLabel(self)
        self.label_image_2 = QLabel(self)
        self.label_image_3 = QLabel(self)
        self.label_image_4 = QLabel(self)
        self.label_image_5 = QLabel(self)
        self.label_image_6 = QLabel(self)
        self.label_image_7 = QLabel(self)
        self.label_image_8 = QLabel(self)

        # Import Images
        self.CubeIQ_image = QPixmap('Images/CubeIQ_logo.png')
        self.CubeIQ_icon_image = QIcon('Images/Project1.ico')
        self.Euro_image = QPixmap('Images/euro_sign_612x612-removebg-preview.png')

        # CubeIQ image
        self.CubeIQ_image.scaled(64, 64)
        self.label_image_1.resize(170, 50)
        self.label_image_1.setPixmap(self.CubeIQ_image)
        self.label_image_1.move(80, 830)

        # Euro images
        self.label_image_2.setPixmap(self.Euro_image)
        self.label_image_3.setPixmap(self.Euro_image)
        self.label_image_4.setPixmap(self.Euro_image)
        self.label_image_5.setPixmap(self.Euro_image)
        self.label_image_6.setPixmap(self.Euro_image)
        self.label_image_7.setPixmap(self.Euro_image)
        self.label_image_8.setPixmap(self.Euro_image)
        self.label_image_2.move(345, 202)
        self.label_image_3.move(345, 352)
        self.label_image_4.move(345, 502)
        self.label_image_5.move(745, 202)
        self.label_image_6.move(745, 352)
        self.label_image_7.move(745, 502)
        self.label_image_8.move(552, 80)

        # Set Window Icon
        self.setWindowIcon(self.CubeIQ_icon_image)

        # Buttons
        self.POS_button_0 = QPushButton('0', self)
        self.POS_button_1 = QPushButton('1', self)
        self.POS_button_2 = QPushButton('2', self)
        self.POS_button_3 = QPushButton('3', self)
        self.POS_button_4 = QPushButton('4', self)
        self.POS_button_5 = QPushButton('5', self)
        self.POS_button_6 = QPushButton('6', self)
        self.POS_button_7 = QPushButton('7', self)
        self.POS_button_8 = QPushButton('8', self)
        self.POS_button_9 = QPushButton('9', self)

        self.POS_button_comma = QPushButton('.', self)
        self.POS_button_clear = QPushButton('C', self)

        self.Entry_button_clear = QPushButton('Clear', self)
        self.Entry_button_PayPod = QPushButton('Pay', self)

        # When hover over button change the cursor
        self.POS_button_0.setCursor(QCursor(Qt.PointingHandCursor))
        self.POS_button_1.setCursor(QCursor(Qt.PointingHandCursor))
        self.POS_button_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.POS_button_3.setCursor(QCursor(Qt.PointingHandCursor))
        self.POS_button_4.setCursor(QCursor(Qt.PointingHandCursor))
        self.POS_button_5.setCursor(QCursor(Qt.PointingHandCursor))
        self.POS_button_6.setCursor(QCursor(Qt.PointingHandCursor))
        self.POS_button_7.setCursor(QCursor(Qt.PointingHandCursor))
        self.POS_button_8.setCursor(QCursor(Qt.PointingHandCursor))
        self.POS_button_9.setCursor(QCursor(Qt.PointingHandCursor))

        self.POS_button_comma.setCursor(QCursor(Qt.PointingHandCursor))
        self.POS_button_clear.setCursor(QCursor(Qt.PointingHandCursor))

        self.Entry_button_clear.setCursor(QCursor(Qt.PointingHandCursor))
        self.Entry_button_PayPod.setCursor(QCursor(Qt.PointingHandCursor))

        # Move buttons to the desired location
        self.POS_button_0.move(980, 450)
        self.POS_button_1.move(850, 150)
        self.POS_button_2.move(980, 150)
        self.POS_button_3.move(1110, 150)
        self.POS_button_4.move(850, 250)
        self.POS_button_5.move(980, 250)
        self.POS_button_6.move(1110, 250)
        self.POS_button_7.move(850, 350)
        self.POS_button_8.move(980, 350)
        self.POS_button_9.move(1110, 350)

        self.POS_button_comma.move(1110, 450)
        self.POS_button_clear.move(850, 550)

        self.Entry_button_clear.move(200, 730)
        self.Entry_button_PayPod.move(430, 730)

        # Set Object Name for buttons for style
        self.POS_button_0.setObjectName('POS_button')
        self.POS_button_1.setObjectName('POS_button')
        self.POS_button_2.setObjectName('POS_button')
        self.POS_button_3.setObjectName('POS_button')
        self.POS_button_4.setObjectName('POS_button')
        self.POS_button_5.setObjectName('POS_button')
        self.POS_button_6.setObjectName('POS_button')
        self.POS_button_7.setObjectName('POS_button')
        self.POS_button_8.setObjectName('POS_button')
        self.POS_button_9.setObjectName('POS_button')

        self.POS_button_comma.setObjectName('POS_button')
        self.POS_button_clear.setObjectName('POS_button')

        self.Entry_button_clear.setObjectName('Entry_button')
        self.Entry_button_PayPod.setObjectName('Entry_button')

        # Text Labels
        self.label_0 = QLabel('Total amount to pay', self)
        self.label_1 = QLabel('Amount 1', self)
        self.label_2 = QLabel('Amount 2', self)
        self.label_3 = QLabel('Amount 3', self)
        self.label_4 = QLabel('Amount 4', self)
        self.label_5 = QLabel('Amount 5', self)
        self.label_6 = QLabel('Amount 6', self)
        self.label_7 = QLabel('Customer', self)

        # Set Object name for style
        self.label_0.setObjectName('Text_Label')
        self.label_1.setObjectName('Text_Label')
        self.label_2.setObjectName('Text_Label')
        self.label_3.setObjectName('Text_Label')
        self.label_4.setObjectName('Text_Label')
        self.label_5.setObjectName('Text_Label')
        self.label_6.setObjectName('Text_Label')
        self.label_7.setObjectName('Text_Label')

        # Move Text Labels to specified position and resize them in order to fit text
        self.label_0.move(290, 30)
        self.label_1.move(130, 150)
        self.label_2.move(130, 300)
        self.label_3.move(130, 450)
        self.label_4.move(530, 150)
        self.label_5.move(530, 300)
        self.label_6.move(530, 450)
        self.label_7.move(330, 600)

        self.label_0.resize(300, 25)
        self.label_1.resize(200, 20)
        self.label_2.resize(200, 20)
        self.label_3.resize(200, 20)
        self.label_4.resize(200, 20)
        self.label_5.resize(200, 20)
        self.label_6.resize(200, 20)
        self.label_7.resize(200, 20)

        # Create Text Inputs
        self.input_text_0 = QLineEdit(self)
        self.input_text_1 = QLineEdit(self)
        self.input_text_2 = QLineEdit(self)
        self.input_text_3 = QLineEdit(self)
        self.input_text_4 = QLineEdit(self)
        self.input_text_5 = QLineEdit(self)
        self.input_text_total_amount = QLineEdit(self)
        self.input_text_customer = QLineEdit(self)

        # Set Text right to left write
        self.input_text_0.setAlignment(Qt.AlignRight)
        self.input_text_1.setAlignment(Qt.AlignRight)
        self.input_text_2.setAlignment(Qt.AlignRight)
        self.input_text_3.setAlignment(Qt.AlignRight)
        self.input_text_4.setAlignment(Qt.AlignRight)
        self.input_text_5.setAlignment(Qt.AlignRight)
        self.input_text_total_amount.setAlignment(Qt.AlignRight)
        self.input_text_customer.setAlignment(Qt.AlignRight)

        # Move Text Inputs to specified positions
        self.input_text_0.move(40, 200)
        self.input_text_1.move(440, 200)
        self.input_text_2.move(40, 350)
        self.input_text_3.move(440, 350)
        self.input_text_4.move(40, 500)
        self.input_text_5.move(440, 500)
        self.input_text_total_amount.move(260, 70)
        self.input_text_customer.move(180, 630)

        self.input_text_0.resize(300, 40)
        self.input_text_1.resize(300, 40)
        self.input_text_2.resize(300, 40)
        self.input_text_3.resize(300, 40)
        self.input_text_4.resize(300, 40)
        self.input_text_5.resize(300, 40)
        self.input_text_total_amount.resize(290, 50)
        self.input_text_customer.resize(400, 70)

        # Set Validator to inputs
        only_float = QDoubleValidator(0.0, 250.0, 2)
        if self.Allow_Dispense_Operation == 1:
            reg_ex = QRegExp(r'^(-)?[0-9]+(\.[0-9]{0,2})?$|^(-)?|^(\.[0-9]{0,2})$')
        else:
            reg_ex = QRegExp(r'^[0-9]*(\.[0-9]{0,2})?$')

        float_validator_0 = QRegExpValidator(reg_ex, self.input_text_0)
        float_validator_1 = QRegExpValidator(reg_ex, self.input_text_1)
        float_validator_2 = QRegExpValidator(reg_ex, self.input_text_2)
        float_validator_3 = QRegExpValidator(reg_ex, self.input_text_3)
        float_validator_4 = QRegExpValidator(reg_ex, self.input_text_4)
        float_validator_5 = QRegExpValidator(reg_ex, self.input_text_5)
        float_validator_total = QRegExpValidator(reg_ex, self.input_text_total_amount)

        self.input_text_0.setValidator(only_float)
        self.input_text_0.setValidator(float_validator_0)
        self.input_text_1.setValidator(only_float)
        self.input_text_1.setValidator(float_validator_1)
        self.input_text_2.setValidator(only_float)
        self.input_text_2.setValidator(float_validator_2)
        self.input_text_3.setValidator(only_float)
        self.input_text_3.setValidator(float_validator_3)
        self.input_text_4.setValidator(only_float)
        self.input_text_4.setValidator(float_validator_4)
        self.input_text_5.setValidator(only_float)
        self.input_text_5.setValidator(float_validator_5)
        self.input_text_total_amount.setValidator(only_float)
        self.input_text_total_amount.setValidator(float_validator_total)

        # Make total amount input at Read Only mode
        self.input_text_total_amount.setReadOnly(True)

        # Set Style
        self.input_text_0.setStyleSheet(input_style)
        self.input_text_1.setStyleSheet(input_style)
        self.input_text_2.setStyleSheet(input_style)
        self.input_text_3.setStyleSheet(input_style)
        self.input_text_4.setStyleSheet(input_style)
        self.input_text_5.setStyleSheet(input_style)
        self.input_text_total_amount.setStyleSheet(input_style)
        self.input_text_customer.setStyleSheet(input_style)
        self.setStyleSheet(style)

        # When a change happens at sub_amount input then trigger function
        self.input_text_0.textChanged.connect(self.calculate_total_amount)
        self.input_text_1.textChanged.connect(self.calculate_total_amount)
        self.input_text_2.textChanged.connect(self.calculate_total_amount)
        self.input_text_3.textChanged.connect(self.calculate_total_amount)
        self.input_text_4.textChanged.connect(self.calculate_total_amount)
        self.input_text_5.textChanged.connect(self.calculate_total_amount)

        # Press Clear and clear all inputs
        self.Entry_button_clear.clicked.connect(self.clear_text)
        self.POS_button_clear.clicked.connect(self.clear_text)

        # WHen Button clicked add character to the last focused user input
        self.POS_button_0.clicked.connect(lambda: self.setFocusText('0'))
        self.POS_button_1.clicked.connect(lambda: self.setFocusText('1'))
        self.POS_button_2.clicked.connect(lambda: self.setFocusText('2'))
        self.POS_button_3.clicked.connect(lambda: self.setFocusText('3'))
        self.POS_button_4.clicked.connect(lambda: self.setFocusText('4'))
        self.POS_button_5.clicked.connect(lambda: self.setFocusText('5'))
        self.POS_button_6.clicked.connect(lambda: self.setFocusText('6'))
        self.POS_button_7.clicked.connect(lambda: self.setFocusText('7'))
        self.POS_button_8.clicked.connect(lambda: self.setFocusText('8'))
        self.POS_button_9.clicked.connect(lambda: self.setFocusText('9'))
        self.POS_button_comma.clicked.connect(lambda: self.setFocusText('.'))

        self.Entry_button_PayPod.clicked.connect(self.show_cashier_window)

        self.add_POS_button_minus()

        self.show()

    def add_POS_button_minus(self):
        if self.Allow_Dispense_Operation == 1:
            # POS minus button
            self.POS_button_minus = QPushButton('-', self)
            self.POS_button_minus.setCursor(QCursor(Qt.PointingHandCursor))
            self.POS_button_minus.move(850, 450)
            self.POS_button_minus.setObjectName('POS_button')
            self.POS_button_minus.clicked.connect(lambda: self.setFocusText('-'))

            # POS arrow button
            self.POS_button_arrow = QPushButton('->', self)
            self.POS_button_arrow.setCursor(QCursor(Qt.PointingHandCursor))
            self.POS_button_arrow.move(1110, 550)
            self.POS_button_arrow.setObjectName('POS_button')
        else:
            self.POS_button_clear.move(850, 450)

    # Clear text when clear button is pressed
    def clear_text(self):
        for qlineedit in [self.input_text_0, self.input_text_1, self.input_text_2, self.input_text_3, self.input_text_4,
                          self.input_text_5, self.input_text_total_amount]:
            QLineEdit.clear(qlineedit)

    # Calculate total amount of qlineedit input when value changes
    def calculate_total_amount(self):
        total = 0
        values = [self.input_text_0, self.input_text_1, self.input_text_2, self.input_text_3, self.input_text_4,
                  self.input_text_5]

        values = [entry.text() for entry in values]
        values = ['0' if value == '' else value for value in values]
        values = ['0.' if value == '.' else value for value in values]
        values = ['-0' if value == '-' else value for value in values]

        for value in values:
            total += float(value)
        self.input_text_total_amount.setText(str(round(total, 2)))

    def setFocusText(self, button_value):
        if self.lineEditFocused.__class__.__name__ == 'QLineEdit':
            if self.lineEditFocused.text() == '':
                if button_value == '.':
                    self.lineEditFocused.setText('0.')
                else:
                    self.lineEditFocused.setText(button_value)
            elif '.' in self.lineEditFocused.text() and len(self.lineEditFocused.text().split(".", 1)[1]) == 2:
                if button_value == '-':
                    self.lineEditFocused.setText('-' + self.lineEditFocused.text())
                else:
                    pass
            else:
                if button_value == '.' and '.' not in self.lineEditFocused.text() and '-' not in self.lineEditFocused.text():
                    self.lineEditFocused.setText(self.lineEditFocused.text() + '.')
                elif button_value == '.' and '.' in self.lineEditFocused.text():
                    pass  # do not add more than one point
                elif button_value == '.' and self.lineEditFocused.text() == '-':
                    pass
                elif button_value == '-' and '-' not in self.lineEditFocused.text():
                    self.lineEditFocused.setText('-' + self.lineEditFocused.text())
                elif button_value == '-' and '-' in self.lineEditFocused.text():
                    pass  # do not add more than two minus
                else:
                    self.lineEditFocused.setText(self.lineEditFocused.text() + button_value)

    def on_focusChanged(self, widget):
        if widget.__class__.__name__ == 'QLineEdit':
            self.lineEditFocused = widget
            QApplication.focusWidget()

    def show_cashier_window(self):
        status_before_Payment = self.get_status()
        print('sta', status_before_Payment)

        # If the system is in Idle mode then a new payment/dispense can start
        if status_before_Payment[0] in ['Idle', 'Change', 'PaymentComplete']:
            # If in total amount we have a - the dispense operation is activated
            if '-' in self.input_text_total_amount.text():
                self.w = Cashier_Window(self.credentials.json(), self.CashGenic_IP_address, mode=3)
                self.w[0].show()
                self.POS_accept_request()
            # If there is a 0 or nothing then nothing happens
            elif self.input_text_total_amount.text() in ['', '0']:
                return
            # Else a payment request is sent to the CashGenic
            else:
                self.w = Cashier_Window(self.credentials.json(), self.CashGenic_IP_address, mode=self.AcceptCashMayStop)
                self.w[0].show()
                self.POS_accept_request()
        # If CashGenic has an error then the error condition is reported via a message
        elif status_before_Payment[0] in ['BillOutOfService', 'CoinOutOfService', 'BillCoinOutOfService']:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(f"Error condition: {status_before_Payment[1]}")
            msgBox.setWindowTitle("CashGenic Message")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            return
        # Else the CashGenic has an active transaction
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("There is an active transaction at CashGenic. Please wait!")
            msgBox.setWindowTitle("CashGenic Message")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            return

    def POS_accept_request(self):
        self.pay_thread_1 = QThread()

        self.worker_1 = Worker(thread=self.pay_thread_1, labels=self.w[2], btns=self.w[1],
                               total_amount_value=self.input_text_total_amount.text(),
                               token=self.credentials.json())

        self.worker_1.moveToThread(self.pay_thread_1)
        # self.worker_1.finished.connect()

        self.pay_thread_1.started.connect(
            self.worker_1.run)

        # self.worker_1.finished.connect(self.show_result)
        # self.worker_1.finished.connect(self.pay_thread_1.quit)

        self.worker_1.finished.connect(self.pay_thread_1.quit)

        self.pay_thread_1.finished.connect(self.worker_1.deleteLater)
        self.pay_thread_1.finished.connect(self.pay_thread_1.deleteLater)

        # self.pay_thread_1.finished.connect(lambda: self.quit_fun(self.pay_thread_1))
        self.pay_thread_1.finished.connect(self.exit_UI)

        self.pay_thread_1.destroyed.connect(self.worker_1.deleteLater)
        self.pay_thread_1.destroyed.connect(self.clean_threads)

        self.pay_thread_1.start()

    def clean_threads(self):
        print("QThread destroyed")
        del self.worker_1
        del self.pay_thread_1

    def get_status(self, port=44333):
        flag_status = True
        status_event = ''

        while flag_status:
            headers = {'Content-Type': 'application/json',
                       'Authorization': 'Bearer ' + self.credentials.json()['access_token']}
            try:
                status_event = httpx.get('https://' + self.CashGenic_IP_address + ':' + str(port) + '/status',
                                         headers=headers, verify=False)
                if status_event.json()['events'][0]['event'] in ['StopComplete', 'CancelComplete', 'RefundComplete']:  # Maybe this is not needed
                    continue
                else:
                    flag_status = False
            except:
                continue

        if status_event.json()['events'][0]['event'] in ['BillOutOfService', 'CoinOutOfService', 'BillCoinOutOfService']:
            return [status_event.json()['events'][0]['event'], status_event.json()['events'][0]['errorCondition']]
        else:
            return [status_event.json()['events'][0]['event']]

    def exit_UI(self):

        def create_exit_button():
            style = '#Cancel_Button {align-items: center;   background-clip: padding-box;   background-color: #FF2400;   border-radius: .25rem;  color: #fff;  font-family: system-ui,-apple-system,system-ui,"Helvetica Neue",Helvetica,Arial,sans-serif;   font-size: 20px;   font-weight: 600;   min-height: 35px;   width: 80px;}' \
                    '#Stop_Button{align-items: center;   background-clip: padding-box;   background-color: #0BDA51;   border-radius: .25rem;  color: #fff;  font-family: system-ui,-apple-system,system-ui,"Helvetica Neue",Helvetica,Arial,sans-serif;   font-size: 20px;   font-weight: 600;   min-height: 35px;   width: 80px;}' \
                    '#Exit_Button {align-items: center;   background-clip: padding-box;   background-color: #03A89E;   border-radius: .25rem;  color: #fff;  font-family: system-ui,-apple-system,system-ui,"Helvetica Neue",Helvetica,Arial,sans-serif;   font-size: 20px;   font-weight: 600;   min-height: 35px;   width: 80px;}'
            exit_button = QPushButton(self.w[0])
            exit_button.setObjectName('Exit_Button')
            exit_button.setStyleSheet(style)
            exit_button.setText('Exit')
            exit_button.setCursor(QCursor(Qt.PointingHandCursor))
            exit_button.move(140, 600)
            exit_button.clicked.connect(lambda: self.w[0].destroy())

            thank_you_label = QLabel('Thank you!', self.w[0])
            thank_you_label.setObjectName('thank_you_label')
            thank_you_label.setStyleSheet('color: white; font-weight:bold; font-size: 21px; font: Source Sans Pro;')
            thank_you_label.move(130, 570)
            thank_you_label.resize(150, 23)
            thank_you_label.show()
            exit_button.show()

            QTimer.singleShot(self.Hide_Cashier_window_time, self.w[0].destroy)

        if self.w is None:
            return
        elif self.w[1][0] is None and self.w[1][1] is None:  # Dispense mode = 3
            self.w[2][3].deleteLater()
            create_exit_button()
        elif self.w[1][1] is None:  # Pay mode = 1
            self.w[1][0].deleteLater()
            self.w[2][3].deleteLater()
            create_exit_button()
        else:  # Pay mode = 2
            self.w[1][0].deleteLater()
            self.w[1][1].deleteLater()
            self.w[2][3].deleteLater()
            create_exit_button()


class Worker(QObject):
    finished = pyqtSignal()

    def __init__(self, thread, labels, btns, total_amount_value='', token='', port=44333, parent=None):
        super().__init__(parent)
        self.total_amount_value = total_amount_value
        self.token = token
        self.port = port
        self.m_thread = thread
        self.labels = labels
        self.btns = btns
        self.CashGenic_IP_address = appsettings['CashGenic_IP']

    def run(self):
        ########################## START OF FUNCTION SECTION ##########################

        # Takes as input a float number and transform it into MDU.
        # MDU = Minimum Dispense Unit
        def amount_to_MDU(amount_to_transform):
            if amount_to_transform == '':
                return 0.0
            else:
                amount_to_transform = float(amount_to_transform)
                return amount_to_transform * 100

        # Send a Get request for the status of CashGenic machine
        async def get_HTTP_status(IP_address_CS, port, status_headers, flag=True, get_status_mode=1):
            """
                :param status_headers: headers for status method
                :param IP_address_CS: IP address of CashGenic
                :param port: default port of CashGenic is 44333
                :param flag: flag is default True in order to run while loop
                :param get_status_mode: mode == 1 is for Pay/Dispense, and mode == 2 is for PayOutError
                :return:
            """
            answer = ''
            ################ BEGIN OF WHILE LOOP ####################
            while flag:
                async with httpx.AsyncClient(verify=False) as client:
                    tasks = client.get('https://' + IP_address_CS + ':' + str(port) + '/status', headers=status_headers)
                    reqs = await asyncio.gather(tasks, return_exceptions=True)
                    try:
                        self.labels[0].setText(f'Total amount: {abs(round(float(self.total_amount_value), 2))} €')
                        self.labels[1].setText(
                            f"Cash In: {round(reqs[0].json()['events'][0]['transaction']['cash_in'] / 100, 2)} €")
                        self.labels[2].setText(
                            f"Cash Out: {round(reqs[0].json()['events'][0]['transaction']['cash_out'] / 100, 2)} €")
                        answer = reqs[0].json()['events'][0]['event']
                    except (Exception,):  # If error pops here then try using only except
                        answer = 'Waiting_exception'

                if answer in ['Waiting', 'Waiting_exception', 'Payment', 'NewPayment', 'PayInStarted', 'Refund', 'Idle',
                              'PayInComplete', 'CancelPayment', 'StoppingPayment', 'Change']:
                    continue
                elif answer == 'PayOutError' and get_status_mode == 2:
                    continue
                else:
                    flag = False
            #################### END OF WHILE LOOP ####################

            return answer

        ########################## END FUNCTION SECTION ##########################

        value = amount_to_MDU(self.total_amount_value)
        IP_address = self.CashGenic_IP_address
        flag_close = True

        if value == 0.0:
            self.finished.emit()
        elif value > 0:
            # IP address with port
            complete_IP = 'https://' + IP_address + ':' + str(self.port) + '/session'

            # Parameters of PayAmount API method
            parameters = {
                "request": "PayAmount",
                "value": value
            }

            # Headers of PayAmount API method
            headers = {'Content-Type': 'application/json',
                       'Authorization': 'Bearer ' + self.token['access_token']}  # answer token

            # Session PayAmount API method
            HTTP_PayAmount_answer = httpx.post(url=complete_IP, json=parameters, headers=headers, verify=False)

            if HTTP_PayAmount_answer.status_code == 200 and HTTP_PayAmount_answer.json()['responseCode'] == 0:
                self.labels[3].setText("Waiting for deposit...")
                event = asyncio.run(get_HTTP_status(IP_address_CS=IP_address, port=self.port, status_headers=headers))

                if event in ['PaymentComplete', 'RefundComplete', 'CancelComplete',
                             'StopComplete']:  # Check for event Idle
                    while flag_close:
                        # PaymentComplete event is for completion of Payment
                        # RefundComplete event is for completion of Payment after Refund
                        # CancelComplete event is for completion of Cancel of Payment
                        # Stop Complete event is for completion of Stop of Payment
                        CLOSE_ANSWER = httpx.post(url=complete_IP,
                                                  # There is a chance that Here CloseSession won't work?
                                                  json={"request": "CloseSession"},
                                                  headers=headers,
                                                  verify=False)
                        try:
                            if CLOSE_ANSWER.json()['responseCode'] == 0:
                                flag_close = False
                        except (Exception,):
                            continue

                    self.finished.emit()



                # PayOutError occurs when there is change available so we should cancel the request
                elif event == 'PayOutError':  # , 'NotEnoughFloat', 'BillDeviceDisconnected', 'CoinDeviceDisconnected','PayoutJammed', 'PayoutOutOfService', 'SoftwareError', 'NotePathOpen', 'BillJammed', 'CashboxRemoved','CalibrationFailedPaid', 'CoinMechError', 'MaintainenceRequired', 'RCCassetteRemoved','Full'
                    # Cancel the Payment
                    self.labels[3].move(95, 530)
                    self.labels[3].setText('No cash available\n      to return')
                    self.labels[3].resize(300, 60)
                    HTTP_Cancel_answer = httpx.post(url=complete_IP,
                                                    json={'request': 'CancelPayment'},
                                                    headers=headers, verify=False)

                    if HTTP_Cancel_answer.status_code == 200 and HTTP_Cancel_answer.json()['responseCode'] == 0:
                        event = asyncio.run(get_HTTP_status(IP_address, self.port, headers, get_status_mode=2))

                        if event == 'RefundComplete':
                            flag_close = True
                            while flag_close:
                                CLOSE_ANSWER = httpx.post(url=complete_IP,
                                                          # There is a chance that Here CloseSession won't work?
                                                          json={"request": "CloseSession"},
                                                          headers=headers,
                                                          verify=False)
                                try:
                                    if CLOSE_ANSWER.json()['responseCode'] == 0:
                                        flag_close = False
                                except:
                                    continue

                            self.finished.emit()

                else:
                    print('Error 404. Something went wrong at Payment')  # Edw tha mpei pop message
                    self.finished.emit()

            elif HTTP_PayAmount_answer.status_code == 200 and HTTP_PayAmount_answer.json()['responseCode'] == 10:
                print('response Code 10 PayAmount error')
                self.finished.emit()

        elif value < 0:
            # IP address with port
            complete_IP = 'https://' + IP_address + ':' + str(self.port) + '/session'

            # Parameters of RefundAmount API method
            parameters = {
                "request": "RefundAmount",
                "value": abs(value)
            }

            # Headers of RefundAmount API method
            headers = {'Content-Type': 'application/json',
                       'Authorization': 'Bearer ' + self.token['access_token']}  # answer token

            # Session RefundAmount API method
            HTTP_RefundAmount_answer = httpx.post(url=complete_IP, json=parameters, headers=headers, verify=False)

            if HTTP_RefundAmount_answer.status_code == 200 and HTTP_RefundAmount_answer.json()['responseCode'] == 0:  # If token can ensure Refund

                self.labels[3].setText("Waiting for dispense...")
                self.labels[3].move(75, 550)
                event = asyncio.run(get_HTTP_status(IP_address_CS=IP_address, port=self.port, status_headers=headers))

                while flag_close:
                    CLOSE_ANSWER = httpx.post(url=complete_IP,
                                              # There is a chance that Here CloseSession won't work?
                                              json={"request": "CloseSession"},
                                              headers=headers,
                                              verify=False)
                    try:
                        if CLOSE_ANSWER.json()['responseCode'] == 0:
                            flag_close = False
                    except (Exception,):
                        print("Exception")
                        continue

                self.finished.emit()

            # The System is out-of-service
            elif HTTP_RefundAmount_answer.status_code == 200 and HTTP_RefundAmount_answer.json()['responseCode'] == 11:
                self.labels[3].move(75, 530)
                self.labels[3].setText('The System is\n     out-of-service')
                self.labels[3].resize(300, 60)
                self.finished.emit()
                time.sleep(2.6)

            # No Cash Available to dispense
            elif HTTP_RefundAmount_answer.status_code == 200 and HTTP_RefundAmount_answer.json()['responseCode'] == 12:
                self.labels[3].move(75, 530)
                self.labels[3].setText('No cash available to\n          return')
                self.labels[3].resize(300, 60)
                time.sleep(2.6)
                self.finished.emit()

            # Admin mode on
            elif HTTP_RefundAmount_answer.status_code == 200 and HTTP_RefundAmount_answer.json()['responseCode'] == 15:
                self.labels[3].move(75, 530)
                self.labels[3].setText('The system is \n     in admin mode')
                self.labels[3].resize(300, 60)
                self.finished.emit()
                time.sleep(2.6)
        else:
            self.finished.emit()
            print('Value Error at Dispense')

    def __del__(self):
        print("--- Worker destroyed")
