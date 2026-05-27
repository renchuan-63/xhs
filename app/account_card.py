from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout
)


class AccountCard(QWidget):

    def __init__(self, account, open_callback, run_callback, delete_callback):
        super().__init__()

        self.account = account

        layout = QVBoxLayout()

        self.setLayout(layout)

        title = QLabel(account['name'])

        layout.addWidget(title)

        btn_layout = QHBoxLayout()

        open_btn = QPushButton('打开')

        open_btn.clicked.connect(
            lambda: open_callback(account)
        )

        btn_layout.addWidget(open_btn)

        run_btn = QPushButton('执行')

        run_btn.clicked.connect(
            lambda: run_callback(account)
        )

        btn_layout.addWidget(run_btn)

        delete_btn = QPushButton('删除')

        delete_btn.clicked.connect(
            lambda: delete_callback(account)
        )

        btn_layout.addWidget(delete_btn)

        layout.addLayout(btn_layout)