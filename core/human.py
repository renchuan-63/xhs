import asyncio
import random
import time


# 随机词库
RANDOM_WORDS = [
    "good",
    "nice",
    "准确",
    "ok",
    "房源还在",
    "awesome",
    "cool",
    "excellent",
    "amazing",
    "近期可看",
    "价格真实",
    "record",
    "记录一下",
    "随时看房",
    "欢迎看房",
    "持续更新",
    "今日记录",
    "内容更新",
    ""
]

def get_random_word():

    return random.choice(
        RANDOM_WORDS
    )

# =========================
# 基础等待
# =========================

async def random_wait(
    min_seconds,
    max_seconds
):
    """
    随机等待
    """

    seconds = random.uniform(
        min_seconds,
        max_seconds
    )

    await asyncio.sleep(seconds)


async def short_wait():

    await random_wait(
        1,
        3
    )


async def medium_wait():

    await random_wait(
        5,
        15
    )


async def long_wait():

    await random_wait(
        30,
        90
    )


# =========================
# 模拟阅读
# =========================

async def simulate_reading(
    page
):
    """
    模拟阅读内容
    """

    scroll_count = random.randint(
        2,
        4
    )

    for _ in range(scroll_count):

        await page.mouse.wheel(
            0,
            random.randint(
                200,
                800
            )
        )

        await random_wait(
            1,
            2
        )

    # 偶尔回滚

    if random.random() > 0.7:

        await page.mouse.wheel(
            0,
            -random.randint(
                100,
                400
            )
        )

        await random_wait(
            1,
            2
        )


# =========================
# 模拟鼠标移动
# =========================

async def move_to_locator(
    page,
    locator
):
    """
    缓慢移动鼠标到元素
    """

    box = await locator.bounding_box()

    if not box:
        return
    # 宽度和高度最小 10px，保证 randrange 有效
    min_x = int(box["x"]) + 1
    max_x = int(box["x"] + max(5, box["width"] - 5))

    min_y = int(box["y"]) + 1
    max_y = int(box["y"] + max(5, box["height"] - 5))

    target_x = random.randint(min_x, max_x)
    target_y = random.randint(min_y, max_y)


    await page.mouse.move(
        target_x,
        target_y,
        steps=random.randint(
            20,
            60
        )
    )

# =========================
# 模拟点击
# =========================

async def human_click(
    page,
    locator
):
    """
    真人点击
    """

    await move_to_locator(
        page,
        locator
    )

    await random_wait(
        0.5,
        2
    )

    await locator.click(
        delay=random.randint(
            80,
            250
        )
    )


# =========================
# 模拟输入
# =========================

async def human_type(
    page,
    text
):
    """
    真人打字
    """

    for char in text:

        await page.keyboard.type(char, delay=random.randint(
                200,
                500
            )
        )

        await asyncio.sleep(
            random.uniform(
                0.3,
                0.8
            )
        )


# =========================
# 编辑前思考
# =========================

async def think_before_edit():
    """
    模拟看内容
    """

    await random_wait(
        10,
        25
    )


# =========================
# 编辑后检查
# =========================

async def check_content():
    """
    模拟检查内容
    """

    await random_wait(
        15,
        35
    )


# =========================
# 发布前犹豫
# =========================

async def think_before_publish():
    """
    模拟确认发布
    """

    await random_wait(
        5,
        12
    )


# =========================
# 计时器
# =========================

def start_timer():

    return time.time()


async def finish_with_target_time(
    start_time,
    min_seconds=150,
    max_seconds=180
):
    """
    保证整篇作品耗时
    2.5~3分钟
    """

    target_time = random.randint(
        min_seconds,
        max_seconds
    )

    elapsed = (
        time.time()
        - start_time
    )

    remain = (
        target_time
        - elapsed
    )

    if remain > 0:

        print(
            f"补足真人时间: {remain:.0f}秒"
        )

        await asyncio.sleep(remain)


# =========================
# 连续发文休息
# =========================

async def rest_after_batch():
    """
    每发几篇休息一次
    """

    rest_seconds = random.choice([
        random.randint(180, 300),   # 3~5分钟
        random.randint(300, 600),   # 5~10分钟
        random.randint(600, 1200)   # 10~20分钟
    ])

    print(
        f"模拟休息: {rest_seconds}秒"
    )

    await asyncio.sleep(
        rest_seconds
    )
    return rest_seconds


# =========================
# 多账号错峰启动
# =========================

async def startup_delay():
    """
    多账号启动间隔
    """

    delay = random.randint(
        60,
        120
    )

    print(
        f"启动延迟: {delay}秒"
    )

    await asyncio.sleep(
        delay
    )



async def human_type_with_typo(
    page,
    text
):

    for char in text:

        if random.random() < 0.05:

            await page.keyboard.type("x")

            await asyncio.sleep(
                random.uniform(
                    0.2,
                    0.5
                )
            )

            await page.keyboard.press(
                "Backspace"
            )

        await page.keyboard.type(char)

        await asyncio.sleep(
            random.uniform(
                0.1,
                0.4
            )
        )

async def simulate_editor_reading(
    page
):
    """
    编辑页浏览
    """

    # 小幅下滑

    await page.mouse.wheel(
        0,
        random.randint(
            200,
            500
        )
    )

    await random_wait(
        2,
        4
    )

    # 小幅回滚

    await page.mouse.wheel(
        0,
        -random.randint(
            100,
            300
        )
    )

    await random_wait(
        2,
        4
    )