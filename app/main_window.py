import asyncio

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
    QLabel,
    QSpinBox
)

from core.account_manager import AccountManager
from core.browser_manager import BrowserManager
from core.xhs_operator import XHSOperator
from app.account_card import AccountCard


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Renchuan')

        self.resize(520, 800)

        self.account_manager = AccountManager()

        self.browser_manager = BrowserManager()

        self.operator = XHSOperator(self.browser_manager, self)

        # 保存账号卡片引用
        self.cards = {}

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

        # restart_btn = QPushButton("重新开始")

        # restart_btn.clicked.connect(
        #     lambda:
        #     asyncio.create_task(
        #         self.restart_round_all()
        #     )
        # )

        # layout.addWidget(
        #     restart_btn
        # )

        run_all_btn.clicked.connect(
            lambda: asyncio.create_task(
                self.run_all()
            )
        )

        layout.addWidget(run_all_btn)


        self.batch_input = QSpinBox()

        self.batch_input.setMinimum(2)
 
        self.batch_input.setMaximum(500)

        self.batch_input.setValue(2)

        layout.addWidget(
            QLabel("数量")
        )

        layout.addWidget(
            self.batch_input
        )

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

        self.cards.clear()

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
                self.continue_account,
                self.restart_account,
                self.stop_account,
                self.delete_account
            )

            # 保存引用
            self.cards[
                account["id"]
            ] = card

            self.container_layout.addWidget(card)

        self.container_layout.addStretch()

    def update_status(
        self,
        account_id,
        status
    ):

        card = self.cards.get(
            account_id
        )

        if card:

            card.status_label.setText(
                f"状态：{status}"
            )

    def update_progress(
        self,
        account_id,
        current,
        total
    ):

        card = self.cards.get(
            account_id
        )

        if card:

            card.progress_label.setText(
                f"进度：{current}/{total}"
            )

    def update_fail(
        self,
        account_id,
        fail_count
    ):

        card = self.cards.get(
            account_id
        )

        if card:

            card.fail_label.setText(
                f"失败：{fail_count}"
            )


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

        print("点击执行按钮")

        count = self.batch_input.value()

        print(
            f"本次处理数量: {count}"
        )

        asyncio.create_task(
            self.operator.relaunch_note(account['id'],
            count
            )
        )

    def continue_account(self, account):

        asyncio.create_task(
            self.operator.continue_round(
                account["id"],
                self.batch_input.value()
            )
        )

    
    def stop_account(
        self,
        account
    ):

        self.operator.stop_task(
            account["id"]
        )


    def restart_account(self, account):

        asyncio.create_task(
        self.restart_and_run(account)
    )

    async def restart_and_run(self, account):

        batch_size = self.batch_input.value()

        await self.operator.restart_round(
            account["id"]
        )

        print(
            "重新开始后执行数量:",
            batch_size
        )

        await self.operator.continue_round(
            account["id"],
            batch_size
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

        batch_size = self.batch_input.value()

        tasks = []

        for account in self.account_manager.accounts:

            tasks.append(
                self.operator.continue_round(
                    account['id'],
                    batch_size
                )
            )

        await asyncio.gather(*tasks)


    async def restart_round_all(self):

        for account in self.account_manager.accounts:

            await self.operator.restart_round(
                account["id"]
            )

        print(
            "所有账号已重新开始新一轮"
        )
