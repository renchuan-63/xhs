from playwright.async_api import async_playwright
from core.human import (
    simulate_reading,
    human_click,
    human_type,
    think_before_edit,
    check_content,
    think_before_publish,
    start_timer,
    finish_with_target_time,
    rest_after_batch,
    startup_delay,
    human_type_with_typo,
    random_wait,
    move_to_locator
)

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

        print(f"{account['name']} 等待登录...")
        try:
            await page.goto('https://creator.xiaohongshu.com/', wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print("首页加载失败:", e)
        # 等待登录成功
        await self.wait_login_success(page)

        print(f"{account['name']} 登录成功")

         # 首页停留逻辑
        # await page.goto('https://creator.xiaohongshu.com/new/home')
        print(f"{account['name']} 已进入首页")
        print("实际URL：", page.url)

        # 模拟首页浏览
        # 模拟首页浏览，但加鼠标移动到页面中间，避免固定元素遮挡
        # body_locator = page.locator('body')
        # await move_to_locator(page, body_locator)   # 确保鼠标在页面中间
        # await simulate_reading(page)
        # await random_wait(1, 3)

        # 点击“笔记管理”
        # note_btn = page.locator("text=笔记管理").first
        # await move_to_locator(page, note_btn)
        # await human_click(page, note_btn)
        # await page.wait_for_timeout(5000)
        # print(f"{account['name']} 已进入笔记管理")
        # print("实际URL：", page.url)

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