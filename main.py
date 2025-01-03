import random
import pygame
import sys
import math
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

# 初始心态值和最大心态值
max_heart_rate = 100  # 最大心态值
current_heart_rate = max_heart_rate  # 当前心态值

# 心态条位置和尺寸
heart_bar_width = 200  # 心态条的总宽度
heart_bar_height = 20  # 心态条高度
heart_bar_x = SCREEN_WIDTH - heart_bar_width - 20  # 靠右上角显示
heart_bar_y = 20  # 距离顶部的距离

# 心态条颜色
heart_bar_color = (0, 255, 0)  # 绿色
heart_bar_bg_color = (200, 200, 200)  # 背景灰色

# Bomb button
button_bomb_position = (250, 500)
try:
    bomb_image = pygame.image.load("bomb.webp")
except pygame.error:
    print("Cannot find bomb.webp")
    sys.exit()
bomb_image = pygame.transform.scale(bomb_image, (70, 70))
button_bomb_rect = bomb_image.get_rect(center = button_bomb_position)
gj_tanmu_timer = 0
gj_tanmu_interval = 120  # 每隔120帧（约2秒）生成一个新的弹幕

le_position = (100,500)
le_image = pygame.image.load("le.png")
le_image = pygame.transform.scale(le_image, (70, 70))
le_rect = le_image.get_rect(center = le_position)

yuanshen_position = (550,300)
yuanshen_image = pygame.image.load("yuanshen.webp")
yuanshen_image = pygame.transform.scale(yuanshen_image, (320, 140))
yuanshen_rect = yuanshen_image.get_rect(center = yuanshen_position)

current_gj_tanmu = ""  # 当前弹幕
gj_tanmu_list = []  # 弹幕列表
gj_tanmu_speed = 1  # 弹幕移动速度
spacing = 25  # 每个弹幕之间的垂直间隔
available_y_positions = [y for y in range(spacing, SCREEN_HEIGHT-100, spacing)]
last_gj_y = 0  # 弹幕之间的最小距离

# 定义pos_tanmu的位置和移动速度
rect_x = 50  # 初始位置
rect_y = 100
rect_speed = 5  # 移动速度
pos_tanmu_list = []  # 发射的弹幕列表
pos_tanmu_speed = 1  # 发射后弹幕的速度

# 生成炸弹
bomb_set_cd = 0
creating_bomb = False
def creating_bomb_draw():
    creating_bomb_pos = pygame.mouse.get_pos()
    bomb_rect = bomb_image.get_rect(center = creating_bomb_pos)
    screen.blit(bomb_image, bomb_rect)

#Bomb instances
setted_bombs = []
def create_a_bomb():
    new_bomb = {"position": pygame.mouse.get_pos(), "scale": 70, "img": bomb_image}
    setted_bombs.append(new_bomb)
    global bomb_set_cd
    bomb_set_cd = 600
bomb_scale_increasing_speed = 1

naZaLe = []
def explosion(pos: tuple[int]):
    for i in range(0, 18):
        naZaLe.append({"text": "  那  咋  了", "time": 0, "position": pos, "id": i})


font = pygame.font.Font("NotoSansSC-VariableFont_wght.ttf", 20)
font_nazale = pygame.font.Font("NotoSansSC-VariableFont_wght.ttf", 20)

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
            if button_bomb_rect.collidepoint(event.pos): #Want to set a bomb by clicking
                if (not creating_bomb) and bomb_set_cd == 0:
                    creating_bomb = True
                else:
                    creating_bomb = False
            elif creating_bomb: #Set a bomb
                create_a_bomb()
                creating_bomb = False
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
            elif event.key == pygame.K_e: #Want to set a bomb by pressing E
                if (not creating_bomb) and bomb_set_cd == 0:
                    creating_bomb = True
                else:
                    creating_bomb = False

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
    if keys[pygame.K_w]:
        rect_y -= rect_speed
    if keys[pygame.K_s]:
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

    # 更新心态值
    for tanmu in gj_tanmu_list:
        if tanmu["x"] < 10:
            if len(tanmu["text"]) > 1:
                tanmu["text"] = tanmu["text"][1:]
                current_heart_rate -= 1
            else:
                gj_tanmu_list.remove(tanmu)

    # 绘制图像
    screen.fill(WHITE)  # 背景填充为白色

    # 绘制心态条背景
    pygame.draw.rect(screen, heart_bar_bg_color, (heart_bar_x, heart_bar_y, heart_bar_width, heart_bar_height))

    # 根据当前心态值绘制心态条
    current_bar_width = int(heart_bar_width * (current_heart_rate / max_heart_rate))
    pygame.draw.rect(screen, heart_bar_color, (heart_bar_x, heart_bar_y, current_bar_width, heart_bar_height))

    # 在屏幕上显示心态条数值（可选）
    text_surface = font.render(f"心态: {current_heart_rate}/{max_heart_rate}", True, BLACK)
    screen.blit(text_surface, (heart_bar_x + heart_bar_width // 2 - text_surface.get_width() // 2, heart_bar_y - 25))


    # 绘制炸弹按钮
    screen.blit(bomb_image, button_bomb_rect)
    text = font.render("那咋了？[E]", True, BLACK)
    screen.blit(text, (button_bomb_rect.x - 20, button_bomb_rect.y + 70))
    if bomb_set_cd != 0:
        text_cd = font.render("冷却中……", True, BLACK)
        screen.blit(text_cd, (button_bomb_rect.x - 20, button_bomb_rect.y + 90))


    #Draw a preview of dropping a bomb
    if creating_bomb and bomb_set_cd == 0:
        creating_bomb_draw()
    
    if bomb_set_cd != 0:
        bomb_set_cd -= 1

    #Draw the setted bumb
    for bomb in setted_bombs:
        bomb_rect = bomb["img"].get_rect(center = bomb["position"])
        screen.blit(bomb["img"], bomb_rect)
        bomb["scale"] += bomb_scale_increasing_speed
        bomb["img"] = pygame.transform.scale(bomb_image, (bomb["scale"], bomb["scale"]))
        if bomb["scale"] == 120:
            setted_bombs.remove(bomb)
            explosion(bomb["position"])
    
    #dispaly na za le
    for nazaleItem in naZaLe:
        nazaleItem["time"] += 1
        if nazaleItem["time"] < nazaleItem["id"]:
            continue
        text_nazale = font.render(nazaleItem["text"], True, RED)
        angle_nazale = nazaleItem["id"] * 20
        text_nazale = pygame.transform.rotate(text_nazale, - angle_nazale)
        radian_nazale = math.radians(angle_nazale)
        x_nazale = nazaleItem["position"][0] + 75 * math.cos(radian_nazale)
        y_nazale = nazaleItem["position"][1] + 75 * math.sin(radian_nazale)
        rec_nazale = text_nazale.get_rect(center = (x_nazale, y_nazale))
        screen.blit(text_nazale, rec_nazale)
        if nazaleItem["time"] == 120 + nazaleItem["id"]:
            naZaLe.remove(nazaleItem)
        for gj_tanmu in gj_tanmu_list[:]:  # 遍历杠精弹幕
            gj_rect = pygame.Rect(gj_tanmu["x"], gj_tanmu["y"], font.size(gj_tanmu["text"])[0], font.get_height())
            if rec_nazale.colliderect(gj_rect):
                gj_tanmu_list.remove(gj_tanmu)

    screen.blit(le_image, le_rect)
    text = font.render("乐[Q]", True, BLACK)
    screen.blit(text, (le_rect.x + 10, le_rect.y + 65))
    if bomb_set_cd != 0:
        text_cd = font.render("冷却中……", True, BLACK)
        screen.blit(text_cd, (button_bomb_rect.x - 20, button_bomb_rect.y + 90))

    screen.blit(yuanshen_image,yuanshen_rect)


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

    if (current_heart_rate <= 0):
        running = False

    # 刷新屏幕
    pygame.display.flip()

    # 控制帧率
    clock.tick(FPS)

# 退出 Pygame
pygame.quit()
sys.exit()
