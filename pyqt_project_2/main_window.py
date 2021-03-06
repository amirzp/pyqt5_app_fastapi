from PyQt5 import (QtWidgets, QtGui)

import login_app
import home_app
import sys
import request_api

BASE_URL = 'http://127.0.0.1:8000'


class MainWindow:
    def __init__(self):
        self.api = request_api.ApiRequest(self)
        self.homeWindow = None
        self.loginWindow = None
        self.admin_name = None
        self.login()

    # ########## home app options >>
    def home_app(self):
        self.loginWindow.destroy()
        self.loginWindow = None
        self.homeWindow = home_app.Window(self.admin_name, self.api)
        self.homeWindow.logoutButton.clicked.connect(self.login)
        self.homeWindow.exitButton.clicked.connect(self.home_exit)

    def home_exit(self):
        if self.homeWindow:

            if QtWidgets.QMessageBox.information(
                    self.homeWindow,
                    "Warning",
                    "Are you sure want to exit?",
                    QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes
            ) == QtWidgets.QMessageBox.Yes:

                sys.exit(0)
    # ########## end home app options <<

    # ########## login app options >>
    def login(self):
        if self.homeWindow:

            if QtWidgets.QMessageBox.information(
                    self.homeWindow,
                    "Warning",
                    "Are you sure want to Log out?",
                    QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes
            ) == QtWidgets.QMessageBox.Yes:

                self.homeWindow.destroy()
                self.homeWindow = None

        if not self.homeWindow:
            self.loginWindow = login_app.Dialog()
            self.loginWindow.logButton.clicked.connect(self.login_click)
            self.loginWindow.backButton.clicked.connect(self.register)
            self.loginWindow.show()

    def login_token(self):
        if self.homeWindow:
            self.homeWindow.destroy()
            self.homeWindow = None
        self.loginWindow = login_app.Dialog()
        self.loginWindow.logButton.clicked.connect(self.login_click)
        self.loginWindow.backButton.clicked.connect(self.register)
        self.loginWindow.show()

    def register(self):
        self.loginWindow = login_app.Dialog('reg')
        self.loginWindow.logButton.clicked.connect(self.register_click)
        self.loginWindow.backButton.clicked.connect(self.login)
        self.loginWindow.show()

    def register_click(self):
        user = self.loginWindow.userLine.text().lower()
        password = self.loginWindow.passLine.text()
        c_password = self.loginWindow.confirmPassLine.text()
        if user and password and c_password:
            if password == c_password:
                data = {
                    "username": f"{user}",
                    "password": f"{password}",
                    "is_staff": True,
                    "is_active": True
                }
                url = f'{BASE_URL}/user/'
                request = self.api.register(data, url)
                if request is True:
                    QtWidgets.QMessageBox.information(
                        self.loginWindow,
                        "Info", 'User is Added.'
                    )
                    self.loginWindow.destroy()
                    self.loginWindow = None
                    return self.login()
                else:
                    txt = self.detail_request(request)
                    QtWidgets.QMessageBox.information(
                        self.loginWindow,
                        "Warning",
                        txt
                    )

            else:
                QtWidgets.QMessageBox.information(
                    self.loginWindow,
                    "Warning",
                    "Those passwords didn't match. please try again"
                )
        else:
            QtWidgets.QMessageBox.information(
                self.loginWindow,
                "Warning",
                "Fields can not empty"
            )

    def login_click(self):
        user = self.loginWindow.userLine.text().lower()
        password = self.loginWindow.passLine.text()
        if user and password:
            data = {
                "username": f"{user}",
                "password": f"{password}"
            }
            url = f'{BASE_URL}/login/'
            request = self.api.login(data=data, url=url)
            if request is True:
                self.admin_name = user
                self.home_app()
                # return True
            else:
                QtWidgets.QMessageBox.information(
                    self.loginWindow,
                    "Warning",
                    str(request['detail'])
                )
        else:
            QtWidgets.QMessageBox.information(
                self.loginWindow,
                "Warning",
                "Fields can not empty"
            )
    # ########## end login page options <<

    @staticmethod
    def detail_request(request: dict):
        txt = ''
        print(request)
        for i in request:
            txt += str(request[i]) + '\n'
        return txt


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.setStyle('QtCurve')
    app.setFont(QtGui.QFont("Noto Sans", 10))
    # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    sys.exit(app.exec_())
