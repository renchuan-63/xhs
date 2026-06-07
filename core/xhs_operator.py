import asyncio
import json
import random

from core.progress_manager import ProgressManager
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
    move_to_locator,
    simulate_editor_reading,
    get_random_word
)


class XHSOperator:

    def __init__(self, browser_manager, main_window):

        self.browser_manager = browser_manager
        self.main_window = main_window
        self.progress = ProgressManager()
        self.stop_flags = {}

    async def enter_note_manager(self, account_id):
        page = self.browser_manager.pages.get(account_id)
        if not page:
            return
        current_url = page.url
        if (
            "note-manager"
            in page.url
        ):
            print("已在笔记管理，无需再次进入")
            return
        # 如果不是笔记管理页，则判断是否在首页
        if "/home" not in current_url:
            print("不是首页，跳转到首页")
            try:
                await page.goto("https://creator.xiaohongshu.com/new/home", wait_until="domcontentloaded", timeout=60000)
            except Exception as e:
                print("进入首页失败:", e)
                return

        # print("进入首页停留")
        # await page.goto("https://creator.xiaohongshu.com/new/home")
        print("首页加载完成")
        await page.wait_for_timeout(2000)
        body_locator = page.locator('body')
        await move_to_locator(page, body_locator)
        await simulate_reading(page)            # 模拟浏览首页
        # await random_wait(1, 3)       # 停留
        # 确保鼠标在页面中央
        

        print("准备点击笔记管理")
        note_btn = page.locator("span.menu-title-wrapper", has_text="笔记管理").first
        try:
            await note_btn.scroll_into_view_if_needed()
            await page.wait_for_timeout(500)
            # 增加重试点击机制
            for attempt in range(3):
                try:
                    await human_click(page, note_btn)
                    break
                except Exception as e:
                    print(f"点击笔记管理失败，第{attempt+1}次重试: {e}")
                    await page.wait_for_timeout(1000)
            else:
                print("连续3次点击失败，退出")
                return
        except Exception as e:
            print("获取笔记管理按钮失败:", e)
            return
        await page.wait_for_timeout(3000)       # 等待笔记管理页面加载
        print("已进入笔记管理")


    async def goto_notes(self, account_id):

            page = self.browser_manager.pages.get(account_id)

            if not page:
                return

            await page.goto(
                'https://creator.xiaohongshu.com/publish/published'
            )
    
    async def test_edit(self, account_id):

        page = self.browser_manager.pages.get(account_id)

        cards = page.locator(".note-card")

        count = await cards.count()

        print("作品数量:", count)

        card = cards.nth(0)

        await card.hover()

        await page.wait_for_timeout(1000)

        edit_btn = card.locator(
            ".note-card__action-btn"
        ).nth(2)

        await edit_btn.click()

        print("已点击编辑")

    # 编辑并发布笔记
    async def process_note(
        self,
        page,
        card,
        note_id
    ):
        start_time = start_timer()

        print(
            f"开始处理作品: {note_id}"
        )

        await card.hover()

        await page.wait_for_timeout(1500)

        btns = card.locator(
            ".note-card__action-btn"
        )

        edit_btn = btns.nth(2)

        # await simulate_reading(page)

        # await think_before_edit()

        await human_click(
            page,
            edit_btn
        )
        await page.wait_for_timeout(
            3000
        )
        print("编辑按钮点击成功")
        await page.wait_for_timeout(
            random.randint(
                3000,
                6000
            )
        )
        await simulate_editor_reading(page)


        await think_before_edit()

        editor = page.locator(
            'div[contenteditable="true"].tiptap.ProseMirror'
        ).first
        await editor.scroll_into_view_if_needed()

        await page.wait_for_timeout(
            random.randint(
                1000,
                3000
            )
        )
        old_text = await editor.inner_text()

        print("原正文:")
        print(old_text)

        # await think_before_edit()
        await move_to_locator(
            page,
            editor
        )

        await random_wait(
            1,
            3
        )
        await editor.click()
        print(
                await page.evaluate(
                    "document.activeElement.outerHTML"
                )
            )

        await editor.evaluate("""
        (node) => {
            node.focus();

            const range = document.createRange();
            const sel = window.getSelection();

            range.selectNodeContents(node);
            range.collapse(false);

            sel.removeAllRanges();
            sel.addRange(range);
        }
        """)

        await page.wait_for_timeout(1000)

        # await page.keyboard.press("Enter")

        word = get_random_word()
        print(
            f"本次追加内容: {word}"
        )

        await human_type(
            page,
            word
        )

        print("正文修改完成")
        await check_content()

        await page.wait_for_timeout(2000)

        publish_btn = page.locator(
            'xhs-publish-btn[is-publish="true"]'
        )

        await think_before_publish()
        try:
            await human_click(
                page,
                publish_btn
            )

            print("点击发布成功")

            await random_wait(
                10,
                30
            )
        except Exception as e:
            print("发布失败", e)
            await page.goto(
                "https://creator.xiaohongshu.com/new/note-manager"
            )

            raise Exception("发布失败")

        print(
            "发布后URL:",
            page.url
        )
        try:
            await finish_with_target_time(
                start_time,
                150,
                180
            )
        except Exception as e:
            print("补足时间失败", e)
    

    async def relaunch_note(self, account_id):
        await self.enter_note_manager(account_id)

        page = self.browser_manager.pages.get(account_id)

        if not page:
            print("页面不存在")
            return

        try:

            # print("进入首页")

            # await page.goto(
            #     "https://creator.xiaohongshu.com/new"
            # )

            # await randow_wait(2, 5)
            await self.enter_note_manager(page)

            # 点击笔记管理
            # note_manager_btn = page.locator('span.menu-title-wrapper', has_text="笔记管理")
            # await human_click(page, note_manager_btn)
            # await page.wait_for_timeout(3000)  # 等待页面加载

            print("进入笔记管理")

            cards = page.locator(".note-card")

            count = await cards.count()

            print(f"发现作品数量: {count}")

            if count == 0:
                return

            # 第一篇作品
            card = cards.nth(0)

            print("开始悬停")

            await card.hover()

            await page.wait_for_timeout(2000)

            print("悬停完成")

            # 打印按钮数量
            btns = card.locator(".note-card__action-btn")

            btn_count = await btns.count()

            print("操作按钮数量:", btn_count)

            for i in range(btn_count):

                txt = await btns.nth(i).inner_text()

                print(f"按钮{i}: {txt}")

            # 编辑按钮
            edit_btn = btns.nth(2)

            print("准备点击编辑")

            # await edit_btn.click()
            await human_click(page, edit_btn)
            await page.wait_for_timeout(
                3000
            )
            print("编辑按钮点击成功")
            await page.wait_for_timeout(
                random.randint(
                    3000,
                    6000
                )
            )
            await simulate_editor_reading(page)
            # await page.wait_for_timeout(5000)

            print("当前URL:", page.url)
            
            # 获取编辑器
            editor = page.locator(
        'div[contenteditable="true"].tiptap.ProseMirror').first
            await editor.scroll_into_view_if_needed()

            await page.wait_for_timeout(
                random.randint(
                    1000,
                    3000
                )
            )

            count = await editor.count()

            print("编辑器数量:", count)
            old_text = await editor.inner_text()

            print("原正文:")
            print(old_text)

            # 修改正文
            await move_to_locator(
                page,
                editor
            )

            await random_wait(
                1,
                3
            )
            await editor.click()
            print(
                await page.evaluate(
                    "document.activeElement.outerHTML"
                )
            )

            await editor.evaluate("""
            (node) => {
                node.focus();

                const range = document.createRange();
                const sel = window.getSelection();

                range.selectNodeContents(node);
                range.collapse(false);

                sel.removeAllRanges();
                sel.addRange(range);
            }
            """)

            # await editor.scroll_into_view_if_needed()
            await page.wait_for_timeout(1000)

            # await page.keyboard.press("End")
            # await page.keyboard.press("Enter")

            word = get_random_word()
            print(
                f"本次追加内容: {word}"
            )

            await page_type(
                page,
                word
            )

            await editor.scroll_into_view_if_needed()

            print("正文修改完成")

            # 等5秒观察
            await page.wait_for_timeout(5000)

            # 点击发布
            print("准备点击发布")

            publish_btn = page.locator(
                'xhs-publish-btn[is-publish="true"]'
            )

            print(
                "发布按钮数量:",
                await publish_btn.count()
            )

            await publish_btn.click()

            print("点击发布成功")

            # 等待返回
            await page.wait_for_timeout(10000)

            print("发布后URL:", page.url)



        except Exception as e:

            print("执行失败:", e)

    async def relaunch_all(self, account_ids):

        # 便利多个账号执行，每个账号先停留首页在进入笔记管理
        tasks = []

        delay = 0

        for account_id in account_ids:

            # 每个账号错峰启动
            await startup_delay()
            tasks.append(
                self.delay_run(account_id)
            )

            # delay += 5

        await asyncio.gather(*tasks)

    async def delay_run(self, account_id, delay=0):

        # await asyncio.sleep(delay)

        # await self.relaunch_note(account_id)
        """
        延迟执行单账号（用于错峰启动）
        """
        if delay > 0:
            await asyncio.sleep(delay)

        page = self.browser_manager.pages.get(account_id)
        if not page:
            print(f"{account_id} 页面不存在")
            return

        # 先停留首页再进入笔记管理
        await self.enter_note_manager(page)

        # 执行单账号的 relaunch_note（保留原逻辑）
        await self.relaunch_note(account_id)

    async def get_note_list(self, page):

        cards = page.locator("[data-impression]")

        count = await cards.count()

        result = []

        for i in range(count):

            card = cards.nth(i)

            try:

                impression = await card.get_attribute(
                    "data-impression"
                )

                if not impression:
                    continue

                data = json.loads(impression)

                note_id = (
                    data["noteTarget"]
                    ["value"]
                    ["noteId"]
                )

                result.append({
                    "note_id": note_id,
                    "card": card
                })

            except Exception as e:
                print(e)
            
            continue

        return result

    async def continue_round(
        self,
        account_id,
        batch_size
    ):
        # continue_round 开头
        # await self.enter_note_manager(account_id)
        self.stop_flags[
            account_id
        ] = False

        page = self.browser_manager.pages.get(
            account_id
        )

        if not page:
            return
        
        await self.enter_note_manager(account_id)

        progress = self.progress.get_progress(
            account_id
        )

        last_note_id = progress["last_note_id"]

        print("上次执行到:", last_note_id)
        # print("进入首页停留")
        # self.main_window.update_status(account_id, "首页浏览中")

        # # 打开首页（如果当前不是首页）
        # if "home" not in page.url:
        #     await page.goto("https://creator.xiaohongshu.com/new/home")
        #     await page.wait_for_timeout(3000)

        # # 模拟浏览首页
        # await simulate_reading(page)
        # await random_wait(3, 8)

        # print("准备点击笔记管理")
        # self.main_window.update_status(account_id, "进入笔记管理")

        # 点击“笔记管理”
        # note_btn = page.locator("text=笔记管理").first
        # 先停留首页
        # await page.goto(
        #     "https://creator.xiaohongshu.com/new"
        # )
        # await self.enter_note_manager(page)

        # await random_wait(
        #     5,
        #     15
        # )

        # # 点击笔记管理
        # note_manager_btn = page.locator('span.menu-title-wrapper', has_text="笔记管理")
        # await human_click(page, note_manager_btn)
        # await page.wait_for_timeout(3000)

        # print("进入笔记管理")
        notes = await self.get_note_list(page)

        start_index = 0

        if last_note_id:

            for i, note in enumerate(notes):

                if note["note_id"] == last_note_id:

                    start_index = i + 1

                    break

        print("开始位置:", start_index)

        target_notes = notes[
            start_index:
            start_index + batch_size
        ]

        # 开始执行时初始化状态
        self.main_window.update_status(
            account_id,
            "运行中"
        )

        self.main_window.update_progress(
            account_id,
            0,
            len(target_notes)
        )

        self.main_window.update_fail(
            account_id,
            0
        )

        if not target_notes:

            self.main_window.update_progress(
                account_id,
                len(notes),
                len(notes)
            )

            self.main_window.update_status(
                account_id,
                
                f"本轮已全部执行完成(共{len(notes)}篇)"
            )

            return

     

        total = len(target_notes)

        success_count = 0
        fail_count = 0
        completed_count = 0
        # 下次休息阈值
        next_rest_count = random.randint(
            3,
            7
        )

        print(
            f"计划发布 {next_rest_count} 篇后休息"
        )

        # for index, note in enumerate(
        #     target_notes,
        #     start=1):

        for note in target_notes:

            # 用户主动停止
            if self.stop_flags.get(
                account_id
            ):
                raise Exception("用户终止")

                print(
                    "用户终止任务"
                )

                self.main_window.update_status(
                    account_id,
                    (
                        f"已停止    "
                        f"成功:{success_count}   "
                        f"失败:{fail_count}"
                    )
                )

                return

            note_id = note["note_id"]

            print(f"处理作品{note_id}")

            # card = note["card"]

            try:

                # await page.goto(
                #     "https://creator.xiaohongshu.com/new/note-manager"
                # )

                # await page.wait_for_timeout(
                #     5000
                # )

                # 刷新笔记管理
                await self.enter_note_manager(page)

                fresh_notes = (
                    await self.get_note_list(
                        page
                    )
                )

                current_card = None

                for item in fresh_notes:

                    if (
                        item["note_id"]
                        == note_id
                    ):

                        current_card = item[
                            "card"
                        ]

                        break

                if not current_card:

                    fail_count += 1
                    completed_count += 1

                    self.main_window.update_fail(
                        account_id,
                        fail_count
                    )

                    print(
                        f"找不到作品:{note_id}"
                    )

                    continue

                await self.process_note(
                    page,
                    current_card,
                    note_id
                )

                self.progress.update_note(
                    account_id,
                    note_id
                )

                success_count += 1

                if success_count >= next_rest_count:
                    print(
                        f"已发布{success_count}篇，开始休息"
                    )

                    self.main_window.update_status(
                        account_id,
                        "模拟休息中"
                    )

                    await rest_after_batch()
                    next_rest_count += random.randint(
                        3,
                        7
                    )

                    print(
                        f"下一次将在 {next_rest_count} 篇后休息"
                    )

                    self.main_window.update_status(
                        account_id,
                        "恢复工作"
                    )

                completed_count += 1


            except Exception as e:

                fail_count += 1

                completed_count += 1

                self.main_window.update_fail(
                    account_id,
                    fail_count
                )

                print(
                    f"处理失败, {note_id}"
                )

                print(e)
                continue
            
            finally:

                self.main_window.update_progress(
                    account_id,
                    completed_count,
                    total
                )

                self.main_window.update_fail(
                    account_id,
                    fail_count
                )

                self.main_window.update_status(
                    account_id,
                    (
                        f"进行中 "
                        f"{completed_count}/{total} "
                        f"成功:{success_count} "
                        f"失败:{fail_count}"
                    )
                )

        self.main_window.update_progress(
            account_id,
            total,
            total
        )

        self.main_window.update_fail(
            account_id,
            fail_count
        )

        self.main_window.update_status(
            account_id,
            (
                f"执行完成 "
                f"成功:{success_count} "
                f"失败:{fail_count}"
            )
        )

    def stop_task(
        self,
        account_id
    ):

        self.stop_flags[
            account_id
        ] = True

        print(
            f"{account_id} 请求停止"
        )

    async def restart_round(
        self,
        account_id
    ):

        self.progress.restart_round(
            account_id
        )

        print("已开启新一轮")

    