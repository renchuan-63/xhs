import asyncio


class XHSOperator:

    def __init__(self, browser_manager):

        self.browser_manager = browser_manager

    async def goto_notes(self, account_id):

        page = self.browser_manager.pages.get(account_id)

        if not page:
            return

        await page.goto(
            'https://creator.xiaohongshu.com/publish/published'
        )

    async def relaunch_note(self, account_id):

        page = self.browser_manager.pages.get(account_id)

        if not page:
            return

        try:

            await page.goto(
                'https://creator.xiaohongshu.com/publish/published'
            )

            await page.wait_for_timeout(3000)

            # 点击重新编辑
            relaunch_btn = page.locator('text=重新编辑').first

            await relaunch_btn.click()

            await page.wait_for_timeout(5000)

            # 点击发布
            publish_btn = page.locator('text=发布').first

            await publish_btn.click()

            print(f'账号 {account_id} 发布成功')

        except Exception as e:

            print(f'账号 {account_id} 操作失败: {e}')

    async def relaunch_all(self, account_ids):

        tasks = []

        delay = 0

        for account_id in account_ids:

            tasks.append(
                self.delay_run(account_id, delay)
            )

            delay += 5

        await asyncio.gather(*tasks)

    async def delay_run(self, account_id, delay):

        await asyncio.sleep(delay)

        await self.relaunch_note(account_id)