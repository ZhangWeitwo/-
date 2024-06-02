import sys
from PyQt5.QtGui import QIcon, QFont
import smtplib
import imaplib
import email
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QGraphicsDropShadowEffect, QSpinBox, QCheckBox, QPushButton, \
    QApplication, QFileDialog, QLabel, \
    QMessageBox, \
    QTextEdit, QHBoxLayout, QTextBrowser, QComboBox, QDesktopWidget, QLineEdit
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from PyQt5.QtWidgets import QApplication, QWidget
from imbox import Imbox
from itertools import islice
from multiprocessing import Pool
import traceback
sender=''
password=''
host=''

def handle_message(uid_message_tuple):
    try:
        uid, message = uid_message_tuple
        output = ["Subject: " + message.subject,
                  "From: " + str(message.sent_from),
                  "To: " + str(message.sent_to),
                  "Body: " + str(message.body['plain']),
                  "<div style='color:red;'>" + ("-" * 50) + "</div>"]
        return output
    except Exception:
        error_message = ["An error occurred: " + traceback.format_exc()]
        return error_message
class SendWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.attachments = []
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setFixedSize(900, 700)
        # 设置icon
        self.setWindowIcon(QIcon('windowpic.png'))
        self.setWindowTitle("发送邮件")
        # 外层容器
        container = QVBoxLayout()

        form_layout = QFormLayout()

        # 发件人名字
        self.sendername_edit = QLineEdit()
        self.sendername_edit.setPlaceholderText("请输入发件人名字")
        form_layout.addRow("发件人：", self.sendername_edit)

        # 收件人输入框
        self.receiver_edit = QLineEdit()
        self.receiver_edit.setPlaceholderText("请输入收件人邮箱")
        form_layout.addRow("收件人邮箱：", self.receiver_edit)

        # 标题
        self.subject_edit = QLineEdit()
        self.subject_edit.setPlaceholderText("请输入标题")
        form_layout.addRow("标题：", self.subject_edit)

        # 邮件内容输入框 - 使用QTextEdit代替QLineEdit
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("请输入邮件内容")
        self.content_edit.setFixedSize(600, 200)
        form_layout.addRow("邮件内容：", self.content_edit)
        # 选择附件
        # Label to show chosen file path
        self.filePathLabel = QLabel('附件路径')
        form_layout.addRow(self.filePathLabel)

        # 选择附件按钮
        chooseFileButton = QPushButton('选择附件')
        chooseFileButton.clicked.connect(self.openFileNameDialog)
        form_layout.addRow(chooseFileButton)

        #将form_layout添加到垂直布局器中
        container.addLayout(form_layout)
        button_layout = QHBoxLayout()
        # 发送按钮
        send_btn = QPushButton("发送")
        send_btn.clicked.connect(self.send_email)
        send_btn.setFixedSize(100, 30)
        # container.addWidget(send_btn, alignment=Qt.AlignCenter)
        button_layout.addWidget(send_btn, alignment=Qt.AlignCenter)
        # 返回按钮
        self.buttonreturn = QPushButton('返回', self)
        self.buttonreturn.clicked.connect(self.on_click)
        # form_layout.addRow(self.buttonreturn)
        button_layout.addWidget(self.buttonreturn, alignment=Qt.AlignCenter)
        form_layout.addRow(button_layout)
        # 设置布局器
        self.setLayout(container)
    def on_click(self):
        self.close()
        self.main_window.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # Open file choose dialog
        fileName, _ = QFileDialog.getOpenFileName(self, "选择附件", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.filePathLabel.setText(f'选中的文件: {fileName}')
            self.attachments.append(fileName)

    def send_email(self):
        # 邮件发送逻辑
        sendername=self.sendername_edit.text()
        sender1 = self.main_window.sender
        password1 = self.main_window.password
        receiver = self.receiver_edit.text()
        subjectname = self.subject_edit.text()
        content = self.content_edit.toPlainText()
        if self.main_window.host=='qq':
            host = 'smtp.qq.com'
        if self.main_window.host=='sina':
            host = 'smtp.sina.com'
        if self.main_window.host=='163':
            host = 'smtp.163.com'
        msg = MIMEMultipart()
        msg['From'] = formataddr([sendername, sender1])
        msg['To'] = formataddr(['收件人', receiver])
        msg['Subject'] = subjectname
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        print(sender1,password1)
        # Add attachments to message
        for file in self.attachments:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(file, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
            msg.attach(part)
        try:
            server = smtplib.SMTP_SSL(host, 465)
            server.login(sender1, password1)
            server.sendmail(sender1, [receiver], msg.as_string())
            server.quit()
            QMessageBox.information(self, '成功', '邮件发送成功')
        except Exception as e:
            QMessageBox.warning(self, '失败', f'邮件发送失败\n{e}')
# 下载邮件

class DownMail(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()
        self.initMail()
    def initUI(self):
        self.setFixedSize(800, 600)
        # 设置icon
        self.setWindowIcon(QIcon('scu.png'))
        self.setWindowTitle("下载邮件")
        # 创建布局
        container = QVBoxLayout()

        form_layout = QFormLayout()
        self.browser = QTextBrowser()
        # 在form_layout上添加文本框
        form_layout.addRow(self.browser)

        container.addLayout(form_layout)

        # 返回按钮
        self.buttonreturn = QPushButton('返回', self)
        self.buttonreturn.clicked.connect(self.on_click)
        # 在container上添加返回按钮
        container.addWidget(self.buttonreturn)

        # 设置布局器
        self.setLayout(container)

    def initMail(self):
        try:
            if self.main_window.host == 'qq':
                hostname = 'imap.qq.com'
            elif self.main_window.host == 'sina':
                hostname = 'imap.sina.com'
            elif self.main_window.host == '163':
                hostname = 'imap.163.com'
            username = self.main_window.sender  # 使用MainWindow中的sender和password
            password = self.main_window.password
            n=self.main_window.n
            with Imbox(hostname,
                       username=username,
                       password=password,
                       ssl=True,
                       ssl_context=None,
                       starttls=False) as imbox:
                # uid
                if hostname == 'imap.163.com':
                    imaplib.Commands['ID'] = ('AUTH')
                    args = ("name", "YYY", "contact", "YYY@163.com", "version", "1.0.0", "vendor", "Imbox")
                    imbox.connection._simple_command('ID', '("' + '" "'.join(args) + '")')
                    imbox.connection.select()

                all_inbox_messages = list(islice(imbox.messages(), n))
                results = [handle_message(msg) for msg in all_inbox_messages]
                with open('emails_output.txt', 'w', encoding='utf-8') as file:
                    for result in results:
                        for line in result:
                            if self.main_window.isd:
                                file.write(line + '\n')
                            self.browser.append(line)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            self.browser.append(error_message)
            return error_message

    def on_click(self):
        self.close()
        self.main_window.show()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.choices_to_strings = {
            "QQ邮箱": "qq",
            "网易邮箱":"163",
             "新浪邮箱": "sina"
        }
        self.selected_string = ""
        self.init_selection()
        self.initUI()

    def initUI(self):
        # 设置大小
       #self.setFixedSize(400, 450)
        self.setWindowTitle('邮件代理')
        self.setGeometry(50, 50, 400, 100)
        self.center()
        container = QVBoxLayout()
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
        form_layout = QFormLayout()
        # 邮箱选择
        self.combo = QComboBox()
        self.combo.addItem("QQ邮箱")
        self.combo.addItem("网易邮箱")
        self.combo.addItem("新浪邮箱")
        self.combo.currentIndexChanged.connect(self.selection_changed)

        # 将下拉列表添加到布局中
        form_layout.addRow("选择邮箱", self.combo)
        # 发件人输入框
        self.sender_edit = QLineEdit()
        self.sender_edit.setPlaceholderText("请输入发件人邮箱")
        form_layout.addRow("邮箱号", self.sender_edit)


        # 授权码输入框
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("请输入授权码")
        self.password_edit.setEchoMode(QLineEdit.Password)  # 密码模式
        form_layout.addRow("授权码：", self.password_edit)

        #进入发送界面
        self.button1 = QPushButton('发送邮件', self)
        self.button1.move(50, 20)
        self.button1.clicked.connect(self.open_send_window)
        self.button1.setStyleSheet(
            "QPushButton {"
            
            "background-color: rgba(150, 198, 231);"  # 设置为有透明度的白色，100是透明度（0~255）
            "border: none;"  # 无边框
            "border-radius: 10px;"  # 圆角按钮
            "padding: 5px;"
            "color: black;"  # 按钮文字颜色
            "}"
        )
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(5)  # 阴影模糊半径
        shadow_effect.setColor(QColor('gray'))  # 阴影颜色
        shadow_effect.setOffset(3, 3)  # x 和 y 方向上的偏移量

        # 将阴影效果应用于 button
        self.button1.setGraphicsEffect(shadow_effect)

        form_layout.addRow(self.button1)
        #选择下载邮件数量
        # 创建一个 QSpinBox 组件
        self.spinBox = QSpinBox()
        self.spinBox.setRange(1, 100)  # 设置最小值为 10，最大值为 100
        self.spinBox.setValue(20)  # 设置初始值为 50
        self.n = int(self.spinBox.value())
        # 创建需要改变大小的组件
        label = QLabel("设置下载邮件数量(过多会卡顿,请耐心等待)")
        label.setStyleSheet(
            "QLabel {"
            "background-color: lightblue;"
            "border: 1px solid gray;"
            "border-radius: 10px;"  # 设置圆角为10像素
            "padding: 4px;"  # 文本与边框的间隙
            "}"
        )
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(5)  # 阴影模糊半径
        shadow_effect.setColor(QColor('gray'))  # 阴影颜色
        shadow_effect.setOffset(3, 3)  # x 和 y 方向上的偏移量

        # 将阴影效果应用于 label
        label.setGraphicsEffect(shadow_effect)
        form_layout.addRow(label)

        form_layout.addRow(self.spinBox)
        #是否下载到文件
        self.checkBox = QCheckBox('是否下载邮件到文件中')
        self.checkBox.setChecked(False)

        form_layout.addRow(self.checkBox)
        #进入下载界面
        self.button2 = QPushButton('下载邮件', self)
        self.button2.move(200, 20)
        self.button2.clicked.connect(self.open_down_window)
        self.button2.setStyleSheet(
            "QPushButton {"

            "background-color: rgba(150, 198, 231);"  # 设置为有透明度的白色，100是透明度（0~255）
            "border: none;"  # 无边框
            "border-radius: 10px;"  # 圆角按钮
            "padding: 5px;"
            "color: black;"  # 按钮文字颜色
            "}"
        )
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(5)  # 阴影模糊半径
        shadow_effect.setColor(QColor('gray'))  # 阴影颜色
        shadow_effect.setOffset(3, 3)  # x 和 y 方向上的偏移量

        # 将阴影效果应用于 button2
        self.button2.setGraphicsEffect(shadow_effect)

        form_layout.addRow(self.button2)
        #声明
        # 创建 QLabel 并设置文本
        label2 = QLabel("声明：\n目前支持QQ，网易邮箱收发\nsina邮箱只支持下载邮件。\n@作者：刘俊伶 2022141461136")

        # 使用样式表设置背景颜色为浅蓝色，边框为1像素黑色实线
        label2.setStyleSheet(
            "QLabel {"
            "background-color: lightblue;"
            "border: 1px solid gray;"
            "border-radius: 10px;"  # 设置圆角为10像素
            "padding: 4px;"  # 文本与边框的间隙
            "}"
        )
        # 创建阴影效果，并设置参数
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(5)  # 阴影模糊半径
        shadow_effect.setColor(QColor('gray'))  # 阴影颜色
        shadow_effect.setOffset(3, 3)  # x 和 y 方向上的偏移量
        # 将阴影效果应用于 label
        label2.setGraphicsEffect(shadow_effect)

        form_layout.addRow(label2)

        container.addLayout(form_layout)
        self.setLayout(container)

    def init_selection(self):
        # 初始化时默认选择第一个选项
        #self.combo.setCurrentIndex(0)
        self.selected_string = self.choices_to_strings["QQ邮箱"]
        #print(f"Default stored string: {self.selected_string}")
    def selection_changed(self):
        # 获取当前选项的文本
        current_text = self.combo.currentText()
        # 根据当前选项的文本查找对应的字符串，并存储
        self.selected_string = self.choices_to_strings.get(current_text, "")
    #发送文件
    def open_send_window(self):
        self.sender=self.sender_edit.text()
        self.password=self.password_edit.text()
        self.host=self.selected_string
        self.send_window = SendWindow(self)
        self.send_window.show()
        self.hide()

    #接收
    def open_down_window(self):
        self.isd=self.checkBox.isChecked()
        self.n=self.spinBox.value()
        self.sender = self.sender_edit.text()
        self.password = self.password_edit.text()
        self.host = self.selected_string
        self.down_window = DownMail(self)
        self.down_window.show()
        self.hide()

    def center(self):
        # 获取屏幕的矩形尺寸
        qr = self.frameGeometry()
        # 获取屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 设置窗口的中心点
        qr.moveCenter(cp)
        # 移动窗口的左上角到计算出的位置，使窗口居中
        self.move(qr.topLeft())
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.resize(800,400)

    window.setWindowIcon(QIcon('scu.png'))
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
