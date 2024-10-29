import pygame
import sys

# 初始化 Pygame
pygame.init()

# 设置窗口大小
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 设置窗口标题
pygame.display.set_caption("Pygame Template")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 设置帧率
clock = pygame.time.Clock()
FPS = 60

# 按钮属性
button_bomb_position = (200, 500)
button_bomb_radius = 30
button_bomb_color = RED

# 主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 点击关闭按钮退出
            running = False

    # 更新游戏逻辑
    # 在这里添加你的游戏逻辑更新

    # 绘制图像
    screen.fill(WHITE)  # 背景填充为白色

    pygame.draw.circle(screen, button_bomb_color, button_bomb_position, button_bomb_radius)
    font = pygame.font.Font(None, 36)
    text = font.render("Bomb", True, BLACK)
    screen.blit(text, (button_bomb_position[0] - 20, button_bomb_position[1] + 30))

    # 在这里添加你的绘制代码

    # 刷新屏幕
    pygame.display.flip()

    # 控制帧率
    clock.tick(FPS)

# 退出 Pygame
pygame.quit()
sys.exit()
