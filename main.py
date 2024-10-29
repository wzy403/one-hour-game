import pygame
import sys
import random
import copy

# 初始化 Pygame
pygame.init()

# 设置窗口大小
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 设置窗口标题
pygame.display.set_caption("Pygame Template with Moving Rectangle and Text")

# 定义颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 杠精弹幕
gangjing_tanmu = [
    "你确定你懂这个吗？",
    "我劝你冷静一下！",
    "数据来源呢？有科学依据吗？",
    "我有不同意见，但我不说。",
    "这不可能是对的！",
    "你这么说有根据吗？",
    "先了解再来聊吧！",
    "从逻辑上讲，这不成立。",
    "凭什么这么说？",
    "我看你就是不懂装懂！",
    "大家都知道，你还真信？",
    "我上次听专家说，完全不是这么回事！",
    "你这是杠吗？我只是客观评价！",
    "照你这么说，世界早乱套了！",
    "呵呵，幼稚。",
    "没有证据，我不信！",
    "你再查查资料吧！",
    "别说得好像你很懂一样！",
    "我看你还是多了解一下再来吧！",
    "你这明显就是误解了！",
    "我笑死，怎么会有这种想法？",
    "再想想清楚吧！",
    "呵呵，你是不是不明白什么叫逻辑？",
    "这也敢说？",
    "有证据吗？还是随便说的？",
    "你确定吗？别闹了！"
]

# 友情弹幕
youqing_tanmu = [
    "咱们友善一点吧~",
    "来！抱一抱！",
    "笑一笑，十年少！",
    "冷静冷静，咱有话好好说！",
    "大哥别杠！消消气！",
    "和为贵啊！",
    "哥们，何必这么较真？",
    "没必要吧？友善一点！",
    "来一波友谊之光！",
    "哎呀，咱们都是朋友！",
    "和平！和平！",
    "这不值得争论啦~",
    "兄弟，握个手！",
    "送你一份正能量！",
    "冷静点，我请你吃顿饭！",
    "多一点友善，多一点温暖！",
    "哈哈，我们都开心一点！",
    "来，喝杯奶茶冷静冷静！",
    "抱抱不生气！",
    "世界这么美好，别动气啦！",
    "相互理解，一切迎刃而解！",
    "来，大家一起和睦相处！",
    "友好一点，生活更美好！",
    "冷静点，不值得生气的~",
    "感谢理解，拥抱友善！"
]

# 设置帧率
clock = pygame.time.Clock()
FPS = 60

# Bomb button
button_bomb_position = (200, 530)
try:
    bomb_image = pygame.image.load("bomb.webp")
except pygame.error:
    print("Cannot find bomb.webp")
    sys.exit()
bomb_image = pygame.transform.scale(bomb_image, (70, 70))
button_bomb_rect = bomb_image.get_rect(center = button_bomb_position)

# get a tanmu
def get_tanmu(tanmu_list):
    return random.choice(tanmu_list)

positive_tanmu = get_tanmu(youqing_tanmu)

# 定义长方形的位置和尺寸
rect_x = 50  # 距离左边 50 像素
rect_y = 100  # 距离顶部初始位置 100 像素
rect_width = 200  # 长方形宽度
rect_height = 50  # 长方形高度
border_width = 1  # 描边宽度
rect_speed = 5  # 长方形移动速度

# 定义字体
font = pygame.font.SysFont("SimHei", 20)

# 生成炸弹
creating_bomb = False
def creating_bomb_draw():
    creating_bomb_pos = pygame.mouse.get_pos()
    screen.blit(bomb_image, creating_bomb_pos)

#Bomb instances
setted_bombs = []
def create_a_bomb():
    new_bomb = {"position": pygame.mouse.get_pos(), "scale": 70, "img": bomb_image}
    setted_bombs.append(new_bomb)


# 主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 点击关闭按钮退出
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_bomb_rect.collidepoint(event.pos): #Want to set a bomb by clicking
                if not creating_bomb:
                    creating_bomb = True
                else:
                    creating_bomb = False
            elif creating_bomb: #Set a bomb
                create_a_bomb()
                creating_bomb = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e: #Want to set a bomb by pressing E
                if not creating_bomb:
                    creating_bomb = True
                else:
                    creating_bomb = False

    # 获取按键
    keys = pygame.key.get_pressed()
    
    # 根据上下键调整长方形的 y 坐标
    if keys[pygame.K_UP]:
        rect_y -= rect_speed
    if keys[pygame.K_DOWN]:
        rect_y += rect_speed

    # 更新游戏逻辑
    # 在这里添加你的游戏逻辑更新

    # 绘制图像
    screen.fill(WHITE)  # 背景填充为白色

    # 绘制炸弹按钮
    screen.blit(bomb_image, button_bomb_rect)
    font_bomb = pygame.font.SysFont("SimHei", 18)
    text = font_bomb.render("那咋了？[E]", True, BLACK)
    screen.blit(text, (button_bomb_rect.x - 20, button_bomb_rect.y + 70))

    #Draw a preview of dropping a bomb
    if creating_bomb:
        creating_bomb_draw()

    #Draw the setted bumb
    for bomb in setted_bombs:
        screen.blit(bomb["img"], bomb["position"])

    # 在这里添加你的绘制代码
    # 绘制带红色描边的长方形
    pygame.draw.rect(screen, RED, (rect_x, rect_y, rect_width, rect_height), border_width)

    # 在长方形中绘制文字
    
    text = font.render(positive_tanmu, True, BLACK)
    text_rect = text.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height // 2))
    screen.blit(text, text_rect)

    # 刷新屏幕
    pygame.display.flip()

    # 控制帧率
    clock.tick(FPS)

# 退出 Pygame
pygame.quit()
sys.exit()
