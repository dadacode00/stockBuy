from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config import errCode


class Kiwoom(QAxWidget):
    def __init__(self):
        super(Kiwoom, self).__init__()
        print("Kiwoom Class 실행")

        # Event loop
        self.login_event_loop = QEventLoop()
        ####

        self.get_ocx_instance()
        self.event_slots()
        self.signal_login_commConnect()


    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")


    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot)


    def login_slot(self, errCode):
        print(errCode(errCode))
        self.login_event_loop.exit()


    def signal_login_commConnect(self):
        print("Login 중")
        self.dynamicCall("CommConnect()")
        self.login_event_loop.exec_()