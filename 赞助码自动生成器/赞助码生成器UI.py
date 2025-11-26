import sys
from data_mysql import database
import random
import string
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QTextEdit, QVBoxLayout, QMessageBox
)
from PyQt6.QtGui import QGuiApplication


class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        # 设置窗口标题和初始大小
        self.setWindowTitle("随机赞助码生成器")
        self.resize(400, 300)

        # 初始化用户界面
        self.init_ui()

    def init_ui(self):
        # 创建垂直布局管理器
        layout = QVBoxLayout()

        # 创建标签，提示用户输入赞助码长度
        self.label = QLabel("请输入赞助码长度：")
        layout.addWidget(self.label)

        # 创建文本输入框，用于接收用户输入的赞助码长度
        self.length_input = QLineEdit()
        layout.addWidget(self.length_input)

        # 创建生成赞助码按钮，并连接点击事件到生成赞助码方法
        self.generate_button = QPushButton("生成赞助码")
        self.generate_button.clicked.connect(self.generate_password)
        layout.addWidget(self.generate_button)

        # 创建文本显示区域，用于显示生成的赞助码，设置为只读
        self.password_output = QTextEdit()
        self.password_output.setReadOnly(True)
        layout.addWidget(self.password_output)

        # 创建复制赞助码按钮，并连接点击事件到复制赞助码方法
        self.copy_button = QPushButton("复制赞助码")
        self.copy_button.clicked.connect(self.copy_password)
        layout.addWidget(self.copy_button)

        # 将布局设置给当前窗口
        self.setLayout(layout)

    def generate_password(self):
        try:
            length = int(self.length_input.text())
            if length <= 0:
                raise ValueError("赞助码长度必须为正整数")
            # 定义赞助码字符集：字母、标点符号和数字
            chars = string.ascii_letters + string.punctuation + string.digits
            # 随机生成指定长度赞助码
            password = ''.join(random.choices(chars,k=length))
            # 将生成的赞助码显式在文本区域中
            self.password_output.setPlainText(password)
        except ValueError as e:
            # 处理输入错误，显示警告对话框
            QMessageBox.warning(self, "输入错误", str(e))

    def copy_password(self):
        # 获取当前显示的赞助码文本
        password = self.password_output.toPlainText()
        if password:
            # 将赞助码复制到系统剪贴板
            QGuiApplication.clipboard().setText(password)

            # 同时保存到数据库
            try:
                length = len(password)
                database.save_password(password, length)

            except Exception as e:
                print(f"❌ 保存到数据库时出错: {e}")

            # 显示复制成功提示
            QMessageBox.information(self, "复制成功", "赞助码已复制到剪贴板！")
        else:
            # 如果没有赞助码可复制，显示警告
            QMessageBox.warning(self, "无赞助码", "请先生成赞助码后再复制！")

if __name__ == "__main__":
    # 创建QApplication实例
    app = QApplication(sys.argv)

    # 创建赞助码生成器窗口
    window = PasswordGenerator()

    # 显示窗口
    window.show()

    # 进入应用程序的主循环
    sys.exit(app.exec())







