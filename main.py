import random
import pygame
import sys
import json

# 初始化 Pygame
pygame.init()

# 设置窗口大小
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 设置窗口标题
pygame.display.set_caption("Pygame Template with Moving Rectangle and Text")

# 定义颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# 加载tanmu massges
tanmu_msg = json.load(open("tanmu.json", "r", encoding="utf-8"))

# 杠精弹幕
gangjing_tanmu = tanmu_msg["gangjing_tanmu"]

# 友情弹幕
youqing_tanmu = tanmu_msg["youqing_tanmu"]

# 设置帧率
clock = pygame.time.Clock()
FPS = 60

gj_tanmu_timer = 0
gj_tanmu_interval = 120  # 每隔120帧（约2秒）生成一个新的弹幕

current_gj_tanmu = ""  # 当前弹幕
gj_tanmu_list = []  # 弹幕列表
gj_tanmu_speed = 1  # 弹幕移动速度
spacing = 25  # 每个弹幕之间的垂直间隔
available_y_positions = [y for y in range(spacing, SCREEN_HEIGHT, spacing)]
last_gj_y = 0  # 弹幕之间的最小距离

# 定义pos_tanmu的位置和移动速度
rect_x = 50  # 初始位置
rect_y = 100
rect_speed = 5  # 移动速度
pos_tanmu_list = []  # 发射的弹幕列表
pos_tanmu_speed = 1  # 发射后弹幕的速度

# 定义字体
font = pygame.font.Font("NotoSansSC-VariableFont_wght.ttf", 20)

# 定义按钮的位置和尺寸
button_x = SCREEN_WIDTH - 150
button_y = SCREEN_HEIGHT - 50
button_width = 100
button_height = 40
button_text = "发射弹幕"  # 按钮的文本

# 标志发射状态
shot_tanmu = False
can_shot_tanmu = False

positive_tanmu_full = random.choice(youqing_tanmu)  # 随机选择友情弹幕
current_positive_tanmu_text = ""
letter_timer = 0
letter_interval = 5

# 主循环
running = True
while running:

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 点击关闭按钮退出
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if button_x <= mouse_x <= button_x + button_width \
                and button_y <= mouse_y <= button_y + button_height \
                    and can_shot_tanmu:
                # 点击按钮时发射弹幕
                can_shot_tanmu = False
                shot_tanmu = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and can_shot_tanmu:
                # 按下空格键时发射弹幕
                can_shot_tanmu = False
                shot_tanmu = True

    if not can_shot_tanmu:
        letter_timer += 1
        if letter_timer >= letter_interval:
            if len(current_positive_tanmu_text) < len(positive_tanmu_full):
                current_positive_tanmu_text += positive_tanmu_full[len(current_positive_tanmu_text)]
            else:
                can_shot_tanmu = True
            letter_timer = 0

    # 获取按键
    keys = pygame.key.get_pressed()
    
    # 根据上下键调整长方形的 y 坐标
    if keys[pygame.K_UP]:
        rect_y -= rect_speed
    if keys[pygame.K_DOWN]:
        rect_y += rect_speed

    # 更新游戏逻辑：生成随机弹幕
    gj_tanmu_timer += 1
    if gj_tanmu_timer >= gj_tanmu_interval:
        # 确保弹幕位置之间保持足够的间隔
        possible_y_positions = [
            y for y in available_y_positions 
            if abs(y - last_gj_y) > 50
        ]
        
        # 只有在存在合适的Y坐标时生成新弹幕
        if possible_y_positions:
            new_y = random.choice(possible_y_positions)
            new_tanmu = {"text": random.choice(gangjing_tanmu), "x": SCREEN_WIDTH, "y": new_y}
            gj_tanmu_list.append(new_tanmu)
            last_gj_y = new_y

        gj_tanmu_timer = 0  # 重置计时器

    # 更新所有杠精弹幕位置
    for tanmu in gj_tanmu_list:
        tanmu["x"] -= gj_tanmu_speed  # 向左移动
        
    # 更新友情弹幕位置
    for tanmu in pos_tanmu_list:
        tanmu["x"] += pos_tanmu_speed  # 向右移动

    # 碰撞检测
    for pos_tanmu in pos_tanmu_list[:]:  # 遍历友情弹幕
        pos_rect = pygame.Rect(pos_tanmu["x"], pos_tanmu["y"], font.size(pos_tanmu["text"])[0], font.get_height())
        for gj_tanmu in gj_tanmu_list[:]:  # 遍历杠精弹幕
            gj_rect = pygame.Rect(gj_tanmu["x"], gj_tanmu["y"], font.size(gj_tanmu["text"])[0], font.get_height())
            
            # 如果发生碰撞
            if pos_rect.colliderect(gj_rect):
                # 删除友情弹幕的最后一个字符
                if len(pos_tanmu["text"]) > 1:
                    pos_tanmu["text"] = pos_tanmu["text"][:-1]
                else:
                    pos_tanmu_list.remove(pos_tanmu)  # 删除空的弹幕
                    break

                # 删除杠精弹幕的第一个字符
                if len(gj_tanmu["text"]) > 1:
                    gj_tanmu["text"] = gj_tanmu["text"][1:]
                else:
                    gj_tanmu_list.remove(gj_tanmu)  # 删除空的弹幕
                    break

    # 绘制图像
    screen.fill(WHITE)  # 背景填充为白色

    # 绘制按钮
    pygame.draw.rect(screen, BLUE, (button_x, button_y, button_width, button_height))
    button_surface = font.render(button_text, True, WHITE)
    button_rect = button_surface.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(button_surface, button_rect)

    # 绘制友情弹幕（显示在矩形内）
    color_here = RED if can_shot_tanmu else BLUE
    text_surface = font.render(current_positive_tanmu_text, True, color_here)
    screen.blit(text_surface, (rect_x, rect_y))  # 在当前rect位置显示

    # 发射后的弹幕逻辑
    if shot_tanmu:
        # 发射弹幕
        pos_tanmu = {"text": current_positive_tanmu_text, "x": rect_x, "y": rect_y}
        pos_tanmu_list.append(pos_tanmu)
        positive_tanmu_full = random.choice(youqing_tanmu)  # 随机选择友情弹幕
        shot_tanmu = False
        current_positive_tanmu_text = ""
        
        # rect_x += pos_tanmu_speed  # 发射弹幕向右移动
        # if rect_x > SCREEN_WIDTH:  # 如果弹幕移出了屏幕，重置弹幕状态
        #     shot_tanmu = False
        #     rect_x = 50  # 重置位置

    # 绘制发射后的弹幕
    for tanmu in pos_tanmu_list:
        tanmu_surface = font.render(tanmu["text"], True, RED)
        screen.blit(tanmu_surface, (tanmu["x"], tanmu["y"]))

    # 绘制所有杠精弹幕
    for tanmu in gj_tanmu_list:
        tanmu_surface = font.render(tanmu["text"], True, BLACK)
        screen.blit(tanmu_surface, (tanmu["x"], tanmu["y"]))

    # 刷新屏幕
    pygame.display.flip()

    # 控制帧率
    clock.tick(FPS)

# 退出 Pygame
pygame.quit()
sys.exit()
