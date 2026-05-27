from playwright.async_api import async_playwright


class BrowserManager:

    def __init__(self):

        self.playwright = None

        self.contexts = {}

        self.pages = {}

    async def start(self):

        if not self.playwright:
            self.playwright = await async_playwright().start()

    async def open_account(self, account):

        await self.start()

        context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=account['user_data_dir'],
            headless=False,
            channel='chrome'
        )

        page = context.pages[0]

        self.contexts[account['id']] = context

        self.pages[account['id']] = page

        await page.goto(
            'https://creator.xiaohongshu.com/'
        )

                # 打开创作者平台
        await page.goto(
            'https://creator.xiaohongshu.com/'
        )

        print(f"{account['name']} 等待登录...")

        # 等待登录成功
        await self.wait_login_success(page)

        print(f"{account['name']} 登录成功")

        # 自动进入笔记管理
        await page.goto(
            'https://creator.xiaohongshu.com/new/note-manager'
        )

        print(f"{account['name']} 已进入笔记管理")

    async def close_account(self, account_id):

        context = self.contexts.get(account_id)

        if context:
            await context.close()

            del self.contexts[account_id]

            del self.pages[account_id]

    async def close_all(self):

        ids = list(self.contexts.keys())

        for account_id in ids:
            await self.close_account(account_id)

    async def wait_login_success(self, page):

        while True:

            try:

                current_url = page.url

                print("当前URL:", current_url)

                # 已进入创作者后台
                if 'creator.xiaohongshu.com' in current_url:

                    # 排除登录页
                    if 'login' not in current_url:

                        return

            except Exception as e:

                print("检测登录失败:", e)

            await page.wait_for_timeout(2000)