from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout
)


class AccountCard(QWidget):

    def __init__(
        self,
        account,
        open_callback,
        continue_callback,
        restart_callback,
        stop_callback,
        delete_callback
    ):
        super().__init__()

        self.account = account

        layout = QVBoxLayout()

        self.setLayout(layout)

        title = QLabel(account['name'])

        layout.addWidget(title)

        btn_layout = QHBoxLayout()

        self.status_label = QLabel("状态：待执行")

        layout.addWidget(self.status_label)

        self.progress_label = QLabel(
            "进度：0/0"
        )

        layout.addWidget(
            self.progress_label
        )

        self.fail_label = QLabel(
            "失败：0"
        )

        layout.addWidget(
            self.fail_label
        )



        # 打开
        open_btn = QPushButton('打开')

        open_btn.clicked.connect(
            lambda: open_callback(account)
        )

        btn_layout.addWidget(open_btn)

        # 继续上一轮
        continue_btn = QPushButton('继续上一轮')

        continue_btn.clicked.connect(
            lambda: continue_callback(account)
        )

        btn_layout.addWidget(continue_btn)

        # 重新开始
        restart_btn = QPushButton('重新开始')

        restart_btn.clicked.connect(
            lambda: restart_callback(account)
        )

        btn_layout.addWidget(restart_btn)

        # 停止
        stop_btn = QPushButton(
            "停止"
        )

        stop_btn.clicked.connect(
            lambda:
            stop_callback(account)
        )

        btn_layout.addWidget(
            stop_btn
        )

        # 删除
        delete_btn = QPushButton('删除')

        delete_btn.clicked.connect(
            lambda: delete_callback(account)
        )

        btn_layout.addWidget(delete_btn)

        layout.addLayout(btn_layout)
