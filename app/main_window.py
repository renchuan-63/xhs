import asyncio

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
    QLabel
)

from core.account_manager import AccountManager
from core.browser_manager import BrowserManager
from core.xhs_operator import XHSOperator
from app.account_card import AccountCard


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('小红书多账号助手')

        self.resize(420, 800)

        self.account_manager = AccountManager()

        self.browser_manager = BrowserManager()

        self.operator = XHSOperator(self.browser_manager)

        self.main_layout = QVBoxLayout()

        self.setLayout(self.main_layout)

        self.init_top_bar()

        self.init_account_area()

        self.render_accounts()

    def init_top_bar(self):

        layout = QHBoxLayout()

        add_btn = QPushButton('+')

        add_btn.clicked.connect(self.add_account)

        layout.addWidget(add_btn)

        open_all_btn = QPushButton('一键打开')

        open_all_btn.clicked.connect(
            lambda: asyncio.create_task(
                self.open_all_accounts()
            )
        )

        layout.addWidget(open_all_btn)

        run_all_btn = QPushButton('一键执行')

        run_all_btn.clicked.connect(
            lambda: asyncio.create_task(
                self.run_all()
            )
        )

        layout.addWidget(run_all_btn)

        close_all_btn = QPushButton('一键关闭')

        close_all_btn.clicked.connect(
            lambda: asyncio.create_task(
                self.browser_manager.close_all()
            )
        )

        layout.addWidget(close_all_btn)

        self.main_layout.addLayout(layout)

    def init_account_area(self):

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(True)

        self.container = QWidget()

        self.container_layout = QVBoxLayout()

        self.container.setLayout(self.container_layout)

        self.scroll.setWidget(self.container)

        self.main_layout.addWidget(self.scroll)

    def render_accounts(self):

        while self.container_layout.count():

            item = self.container_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        title = QLabel(
            f'账号工作区（{len(self.account_manager.accounts)}个账号）'
        )

        self.container_layout.addWidget(title)

        for account in self.account_manager.accounts:

            card = AccountCard(
                account,
                self.open_account,
                self.run_account,
                self.delete_account
            )

            self.container_layout.addWidget(card)

        self.container_layout.addStretch()

    def add_account(self):

        self.account_manager.add_account()

        self.render_accounts()

    def open_account(self, account):

        asyncio.create_task(
            self.browser_manager.open_account(account)
        )

    async def open_all_accounts(self):

        tasks = []

        for account in self.account_manager.accounts:

            tasks.append(
                self.browser_manager.open_account(account)
            )

        await asyncio.gather(*tasks)

    def run_account(self, account):

        asyncio.create_task(
            self.operator.relaunch_note(account['id'])
        )

    def delete_account(self, account):

        asyncio.create_task(
                self.delete_account_async(account)
        )

    async def delete_account_async(self, account):

        try:

            # 关闭浏览器
            await self.browser_manager.close_account(
                account['id']
            )

        except:
            pass

        # 删除配置
        self.account_manager.delete_account(
            account['id']
        )

        # 刷新UI
        self.render_accounts()

    async def run_all(self):

        account_ids = [
            acc['id']
            for acc in self.account_manager.accounts
        ]

        await self.operator.relaunch_all(account_ids)
