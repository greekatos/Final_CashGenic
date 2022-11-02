from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRectF, QTimer
from PyQt5.QtGui import QPainterPath, QRegion, QCursor
import httpx
import time


def center_window(window):
    frameGm = window.frameGeometry()
    screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
    center_Point = QApplication.desktop().screenGeometry(screen).center()
    frameGm.moveCenter(center_Point)
    window.move(frameGm.topLeft())


def Cashier_Window(token, IP_address, mode=1):
    pay_window = QWidget()
    pay_window.setFixedSize(350, 650)
    pay_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)  # Destroy Window Title

    # Make Widget round on the edges. Idea from https://stackoverflow.com/a/55172738/14749665 Understand how it cuts the window
    path = QPainterPath()
    radius = 40.0
    path.addRoundedRect(QRectF(pay_window.rect()), radius, radius)
    mask = QRegion(path.toFillPolygon().toPolygon())
    pay_window.setMask(mask)
    center_window(pay_window)

    style = '#Cancel_Button {align-items: center;   background-clip: padding-box;   background-color: #FF2400;   border-radius: .25rem;  color: #fff;  font-family: system-ui,-apple-system,system-ui,"Helvetica Neue",Helvetica,Arial,sans-serif;   font-size: 20px;   font-weight: 600;   min-height: 35px;   width: 80px;}' \
            '#Stop_Button{align-items: center;   background-clip: padding-box;   background-color: #0BDA51;   border-radius: .25rem;  color: #fff;  font-family: system-ui,-apple-system,system-ui,"Helvetica Neue",Helvetica,Arial,sans-serif;   font-size: 20px;   font-weight: 600;   min-height: 35px;   width: 80px;}' \
            '#Exit_Button {align-items: center;   background-clip: padding-box;   background-color: #8cd3ff;   border-radius: .25rem;  color: #fff;  font-family: system-ui,-apple-system,system-ui,"Helvetica Neue",Helvetica,Arial,sans-serif;   font-size: 20px;   font-weight: 600;   min-height: 35px;   width: 80px;}'

    # Set Widget style
    pay_window.setObjectName('Cashier_Window')
    pay_window.setStyleSheet("""#Cashier_Window {     background: #80ADBC;   }""")

    # Set Widget Labels and style
    label_total_amount = QLabel('Total amount:', pay_window)
    label_total_amount.setStyleSheet('color: white; font-weight:bold; font-size: 20px')
    label_total_amount.move(20, 100)
    label_total_amount.resize(250, 20)

    label_cash_in = QLabel('Cash In:', pay_window)
    label_cash_in.setStyleSheet('color: white; font-weight:bold; font-size: 20px')
    label_cash_in.move(20, 200)
    label_cash_in.resize(200, 20)

    label_cash_out = QLabel('Cash Out:', pay_window)
    label_cash_out.setStyleSheet('color: white; font-weight:bold; font-size: 20px')
    label_cash_out.move(20, 300)
    label_cash_out.resize(200, 20)

    label_transaction_information = QLabel(pay_window)
    label_transaction_information.setStyleSheet(
        'color: white; font-weight:bold; font-size: 22px; font: Source Sans Pro;')
    label_transaction_information.move(85, 550)
    label_transaction_information.resize(250, 25)

    stop_button = None
    cancel_button = None

    if mode == 1:  # If mode is 1 then create only cancel button
        # Create Widget buttons
        cancel_button = QPushButton(pay_window)

        cancel_button.setObjectName('Cancel_Button')
        cancel_button.setStyleSheet(style)
        cancel_button.setText('Cancel')
        cancel_button.setCursor(QCursor(Qt.PointingHandCursor))

        cancel_button.move(140, 600)
        cancel_button.clicked.connect(
            lambda: cancel_payment(IP_address=IP_address, type_button='Cancel', buttons=[cancel_button, stop_button],
                                   token=token))
        stop_button = None
    elif mode == 2:  # If mode is 2 then create can stop and cancel button
        # Cancel button
        stop_button = QPushButton(pay_window)
        cancel_button = QPushButton(pay_window)

        cancel_button.setObjectName('Cancel_Button')
        cancel_button.setStyleSheet(style)
        cancel_button.setText('Cancel')
        cancel_button.setCursor(QCursor(Qt.PointingHandCursor))

        # Stop button
        stop_button.setObjectName('Stop_Button')
        stop_button.setStyleSheet(style)
        stop_button.setText('Stop')
        stop_button.setCursor(QCursor(Qt.PointingHandCursor))

        cancel_button.move(230, 600)
        stop_button.move(50, 600)

        stop_button.clicked.connect(
            lambda: cancel_payment(IP_address=IP_address, type_button='Stop', buttons=[cancel_button, stop_button],
                                   token=token))
        cancel_button.clicked.connect(
            lambda: cancel_payment(IP_address=IP_address, type_button='Cancel', buttons=[cancel_button, stop_button],
                                   token=token))


    elif mode == 3:
        cancel_button = None
        stop_button = None

    return [pay_window, [cancel_button, stop_button],
            [label_total_amount, label_cash_in, label_cash_out, label_transaction_information]]


def cancel_payment(IP_address, token, type_button, buttons, port=44333):
    complete_IP = 'https://' + IP_address + ':' + str(port) + '/session'

    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + str(token['access_token'])}  # answer token

    if type_button == 'Stop':

        httpx.post(url=complete_IP,
                   json={'request': 'StopPayment'},
                   headers=headers, verify=False)
        # buttons[0].setEnabled(False)
        # buttons[1].setEnabled(False)
    else:
        httpx.post(url=complete_IP,
                   json={'request': 'CancelPayment'},
                   headers=headers, verify=False)
        # buttons[0].setEnabled(False)
        # buttons[1].setEnabled(False)
