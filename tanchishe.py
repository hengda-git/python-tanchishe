# pip install pygame # 安装pygame 库
# 如果此命令安装失败则尝试使用下面的命令安装
# python3 -m pip install pygame

# 1. 引入所需包
import pygame, sys, random
from pygame.locals import *

# 2. 定义全局变量
# 2.01 定义颜色
white = pygame.Color(255, 255, 255)
blue = pygame.Color(0, 0, 200)
black = pygame.Color(0, 0, 0)
green = pygame.Color(0, 255, 0)
yellow = pygame.Color(255,255,0)
spanColor = black  # 界面背景颜色 黑 r g b 取值范围 0 -255
snakeColor = yellow  # 蛇的颜色 蓝
appleColor = green  # 苹果的颜色 绿

# 2.02 定义游戏界面尺寸
wWidth = 640 #　游戏界面窗口像素宽度
wHeight = 480 #　游戏界面窗口像素高度
blockSize = 20 # 方格边长像素数，苹果边长和蛇身的宽度都是这个尺寸
#wWidth = 1280 #　游戏界面窗口像素宽度
#wHeight = 960 #　游戏界面窗口像素高度
#blockSize = 20 # 方格边长像素数，苹果边长和蛇身的宽度都是这个尺寸
wBlocksNum = wWidth / blockSize #横向方格数 32
hBlocksNum = wHeight / blockSize #纵向方格数 24

# 2.03 定义存储蛇和苹果等数据变量并初始化
snakeBody = [[0,0]] #蛇的位置（存储蛇身体所占坐标的列表数据）
applePosition = [1,1] #苹果位置

# 2.04 定义默认运动方向和速度
direction = 'right'  # 蛇运动的默认初始方向
speed = 10 # 初始化爬行速度单位每秒爬行步数，数越大 跑的越快
score = 0 # 成绩
isShowXYInfo = False #是否显示界面坐标信息 用户调试界面

# 2.05 打印信息模板
infoList = list([
    "GAME OVER!!!",
    " ",
    "成绩:   %d 分",
    " ",
	"名称:  《贪吃蛇》",
    "语言:   Python ",
	"作者:   Hengda ",#版权所有",
	"时间:   2020/04/22",
    "github: hengda-git",
	"1.按Enter继续游戏",
	"2.按ESC退出"
])
# 可显示为中文的字体
chineseFontList = list([
    #windows （win10 中搜索到的中文字体）
    "microsoftyaheimicrosoftyaheiui",
    "microsoftjhengheimicrosoftjhengheiui",
    "microsoftjhengheimicrosoftjhengheiuibold",
    "microsoftjhengheimicrosoftjhengheiuilight",
    "microsoftyaheimicrosoftyaheiui",
    "microsoftyaheimicrosoftyaheiuibold",
    "microsoftyaheimicrosoftyaheiuilight",
    "simsunnsimsun",
    "dengxian",
    "fangsong",
    "kaiti",
    "simhei",
    "方正舒体",
    "方正姚体",
    "隶书",
    "幼圆",
    "华文彩云",
    "华文仿宋",
    "华文琥珀",
    "华文楷体",
    "华文隶书",
    "华文宋体",
    "华文细黑",
    "华文行楷",
    "华文新魏",
    "华文中宋",
    "小米兰亭",
    "adobefangsongstdregularopentype",
    "adobeheitistdregularopentype",
    "adobekaitistdregularopentype",
    "adobesongstdlightopentype",
    "方正粗黑宋简体",
    #linux (deepin 15.11 中搜索到的中文字体)
    "notosanscjkjp",
    "notosansmonocjkkr",
    "notosanscjktc",
    "notosanscjkkr",
    "notosansmonocjkjp",
    "notosanscjksc",
    "notosansmonocjktc",
    "unifont",
    "notosansmonocjksc"
    #mac (本人屌丝，没有mac，你们自己添加吧)
    # （找到test_font() 这一行 ，取消注释，放开运行，然后查看print打印信息）
    # （每测试一个字体 ，在游戏界面按enter即可进入下一个字体测试）
])
# 系统存在的中文字体作为界面字体，默认为微软雅黑，启动程序会自动去系统匹配可用字体
defaultFontName = "microsoftyaheimicrosoftyaheiui"

# 2.06 定义其他变量
playSurface = None #界面
fpsClock = None #时钟

# 3. 定义基本函数

# 3.01 游戏结束退出
def gameOver():
    pygame.quit()
    sys.exit()

# 3.02 获取键盘输入，判断下一步应该运动的方向（包含获取键盘按下的方向）
def getKeyboardDirection():
    global direction
    for event in pygame.event.get():
        if event.type == QUIT:
            gameOver()
        elif event.type == KEYDOWN:# 判断键盘事件，确定方向，移动蛇头坐标
            if event.key == K_RIGHT:  # 向右
                if not direction == 'left':direction = 'right'
            elif event.key == K_LEFT:  # 向左
                if not direction == 'right':direction = 'left'
            elif event.key == K_UP:  # 向上
                if not direction == 'down':direction = 'up'
            elif event.key == K_DOWN:  # 向下
                if not direction == 'up':direction = 'down'
            elif event.key == K_SPACE: #空格
                return 'space'
            elif event.key == K_RETURN: #回车
                return 'return'
            elif event.key == K_ESCAPE: #ESC
                gameOver()
        return direction

# 3.03 初始化程序延时时钟 #用来控制游戏的速度
def init_Clock():
    global fpsClock
    fpsClock = pygame.time.Clock()

# 3.04 执行延时
def exec_delay():
    global speed
    global fpsClock
    fpsClock.tick(speed) # 爬行动作频次时钟控制

# 3.05 初始化界面
def init_playSurface():
    global playSurface
    global wWidth
    global wHeight
    pygame.init() # 初始化Pygame
    init_Clock() # 初始化程序延时时钟 #用来控制游戏的速度
    playSurface = pygame.display.set_mode((wWidth, wHeight)) # 创建pygame的显示层
    pygame.display.set_caption('贪吃蛇') # 窗口标题

# 3.06 在界面的x y坐标处打印对应的坐标值
def display_XY(x,y):
    global playSurface
    myfont = pygame.font.Font(None, int(blockSize/2))
    textImage = myfont.render(("%d,%d"%(x,y)), True, white)
    playSurface.blit(textImage, (x*blockSize, y*blockSize))

# 3.07 画一个颜色块
def draw_color_rect(color, position, width, height):
    global isShowXYInfo
    global playSurface
    pygame.draw.rect(playSurface, color, Rect(position[0], position[1], width, height))

    if isShowXYInfo :#打印界面坐标信息，每一个方格都可以打上对应的坐标，用于调试
        for j in range(int(position[1]/blockSize),int((position[1]+height)/blockSize)):
            for i in range(int(position[0]/blockSize), int((position[0]+width)/blockSize)):
                display_XY(i,j);

# 3.08 指定位置画指定颜色且尺寸为blockSize
def draw_color_block_with_position(color,position):
    global blockSize
    pixPosition = list([position[0] * blockSize,position[1] * blockSize])
    draw_color_rect(color, pixPosition, blockSize, blockSize)

# 3.09 初始化背景
def init_span():
    global wWidth
    global wHeight
    global spanColor
    draw_color_rect(spanColor, [0,0], wWidth, wHeight)

# 3.10 判断苹果与蛇是否重合
def is_snake_cover_new_apple():
    global snakeBody
    global applePosition
    for s in snakeBody[1:]:  # 遍历蛇身，判断蛇头是否与蛇身重合
        if applePosition[0] == s[0] and applePosition[1] == s[1]: return 1
    return 0

# 3.11 判断蛇头是否与苹果重合
def is_snake_next_head_cover_apple(nextSnakeHead):
    global applePosition
    if nextSnakeHead[0] == applePosition[0] and nextSnakeHead[1] == applePosition[1] : return 1
    else : return 0

# 3.12 判断蛇自己的身体是否覆盖了蛇头
def is_snake_next_head_cover_body(nextSnakeHead):
    global snakeBody
    for s in snakeBody[1:]:  # 遍历蛇身，判断蛇头是否与蛇身重合
        if nextSnakeHead[0] == s[0] and nextSnakeHead[1] == s[1]: return 1
    return 0

# 3.13 在空区域随机生成苹果的位置（该函数请在蛇的位置确定后再调用）
def get_new_apple_position():
    global applePosition
    global wBlocksNum
    global hBlocksNum
    while True: # 生成新的苹果位置
        x = random.randrange(0, wBlocksNum-1) # 新苹果所在方块　水平序号x
        y = random.randrange(0, hBlocksNum-1) # 新苹果所在方块　垂直序号y
        applePosition = list([x, y])  # 新苹果的位置
        if not is_snake_cover_new_apple() : break #如果检查该苹果捕鱼蛇的身体重合，则说明苹果有效，则结束

# 3.14 根据行走方向 获取下一步蛇头的位置
def get_next_head_with_direction():
    global direction
    global snakeBody
    nextSnakeHead = list(snakeBody[0]);
    # 根据方向修改蛇头的新坐标数据
    if direction == 'right': nextSnakeHead[0] += 1
    if direction == 'left': nextSnakeHead[0] -= 1
    if direction == 'down': nextSnakeHead[1] += 1
    if direction == 'up': nextSnakeHead[1] -= 1
    return nextSnakeHead

# 3.15 判断下一步是否是围墙
def is_next_step_touch_the_wall(nextSnakeHead):
    global wBlocksNum
    global hBlocksNum
    if (nextSnakeHead[0] > wBlocksNum - 1 or nextSnakeHead[0] < 0 or nextSnakeHead[1] > hBlocksNum - 1 or nextSnakeHead[1] < 0) : return 1
    else : return 0

# 3.16 累加成绩
def increment_score():
    global score
    score+=1

# 3.16 读取游戏信息 调试用
def get_game_over_info():
    global score
    global infoList
    newInfolist = list(infoList)
    newInfolist[2] = newInfolist[2] % score
    return newInfolist

# 3.17 恢复成绩
def clear_score():
    global score
    score = 0

# 3.18 读取分数
def get_score():
    return score

# 3.19 初始化苹果
def init_apple():
    get_new_apple_position() # 随机获取一个新苹果位置
    draw_apple()# 画新的苹果

# 3.20 初始化蛇
def init_snake():
    global direction
    global snakeColor
    global snakeBody
    x = wBlocksNum/2
    y = hBlocksNum/2
    while len(snakeBody): snakeBody.pop() # 删除原数据
    ## 重新初始化蛇数据
    if direction == 'left': snakeBody = list([[x - 1, y], [x, y], [x + 1, y]])
    elif direction == 'right': snakeBody = list([[x + 1, y], [x, y], [x - 1, y]])
    elif direction == 'up': snakeBody = list([[x, y - 1], [x, y], [x, y + 1]])
    elif direction == 'down': snakeBody = list([[x, y + 1], [x, y], [x, y - 1]])
    for position in snakeBody: draw_color_block_with_position(snakeColor, position) # 初始化蛇的每一节

# 3.21 画蛇头
def draw_snake_head():
    global snakeColor
    global snakeBody
    snakeHead = snakeBody[0]
    draw_color_block_with_position(snakeColor, snakeHead) # 画新的蛇头（身体不需要重新画）

# 3.22 添加蛇头 爬行经过的每个地方都会先变为蛇头，所以所经之处皆应加到列表蛇数据的头部
def add_snake_head(nextSnakeHead):
    global snakeBody
    snakeBody.insert(0, list(nextSnakeHead))

# 3.23 打印数据列表 调试用
def dump_snake_data(flag):
    print("%d开始-》" % flag)
    for position in snakeBody:
        print("#### %d,%d" % (position[0], position[1]))
    print("%d结束《-" % flag)

# 3.24 清空蛇尾
def clear_snake_tail():
    global snakeBody
    global spanColor
    snakeTail = list(snakeBody[len(snakeBody)-1])#　得到蛇尾巴坐标
    draw_color_block_with_position(spanColor, snakeTail)  # 把原尾巴的位置的颜色设置为背景色

# 3.25 画苹果
def draw_apple():
    global appleColor
    global applePosition
    draw_color_block_with_position(appleColor, applePosition)# 画新的苹果

# 3.26 删掉蛇尾
def drop_snake_tail():
    snakeBody.pop()  # 将原尾巴数据删去

# 3.27 更新显示画面
def display():
    pygame.display.flip()

# 3.28 打印信息
def display_info(infoList,fontName,fontSize,backgroundColor,fontColor,isWaitKeyBord):
    global playSurface
    playSurface.fill(backgroundColor)
    myfont = pygame.font.SysFont(fontName, fontSize)
    infoLen = len(infoList)
    i = 0
    textX = (wWidth / fontSize) / 3
    for info in infoList:
        textImage = myfont.render(info, True, fontColor)
        textY = 1 + i*2
        playSurface.blit(textImage, (textX*fontSize, textY*fontSize))
        i = i+1
    display();

    if(isWaitKeyBord):
        while getKeyboardDirection()!='return': None

# 3.29 查看系统字体列表 并用信息模板测试显示效果
def get_usefull_sys_font():
    global defaultFontName
    ZiTi = pygame.font.get_fonts()
    for fontName in ZiTi:
        if is_font_in_chinese_fontlist(fontName) :
            defaultFontName = fontName
            return True
    return False

# 判断字体是可用
def is_font_in_chinese_fontlist(theFontName):
    for fontName in chineseFontList:
        if fontName==theFontName: return True
    return False

def test_font():
    ZiTi = pygame.font.get_fonts()
    for fontName in ZiTi:
        print(fontName)
        display_info(infoList, fontName, 20, white, black, False)
        #exec_delay()  # 延时
        while getKeyboardDirection() != 'return': None #敲击Enter则开始下一个字体的测试

# 4. 实现主体函数循环
def main():

    # 4.01 使用全局变量
    global snakeBody
    global infoList

    # 4.02 初始化窗口
    init_playSurface()
    # 获取系统可用的带中文的字体
    get_usefull_sys_font()

    # 系统字体测试 找到可用的中文字体
    # test_font()

    # 4.03 进入程序主循环
    while True :

        init_span() # 4.03.01 初始化背景
        init_snake()  # 4.03.03 初始化蛇
        init_apple() # 4.03.02 初始化苹果
        display() # 4.03.04 更新界面显示（画的新图像需要重新显示）
        clear_score() # 4.03.05 清空成绩

        # 4.03.06 循环以完成蛇不断地爬行
        while True: # 每次循环，意味着蛇爬行一步，并且在每次循环中要读取键盘所按方向键，未按方向键则按原来方向继续爬行，如果改变了方向，则调整爬行方向

            display()  # 4.03.06.01 更新显示画面
            exec_delay()  # 4.03.06.02 爬行动作频次时钟控制，实现每一步之间的延时
            getKeyboardDirection() # 4.03.06.03 读取蛇运动方向（当键盘按方向键后，direction 值会及时更新）
            nextSnakeHead = get_next_head_with_direction() # 4.03.06.04 得到下步蛇头要走的位置

            if is_next_step_touch_the_wall(nextSnakeHead): break;  # 4.03.06.05 遇到围墙，即将越界则结束 本局结束

            if is_snake_next_head_cover_apple(nextSnakeHead): # 4.03.06.06 # 如果我们的贪吃蛇的位置和苹果重合了，说明吃到了苹果

                add_snake_head(nextSnakeHead) # 4.03.06.06.01 新的蛇头数据放入蛇列表数据开头
                draw_snake_head() # 4.03.06.06.02 画新的蛇头（身体不需要重新画）
                get_new_apple_position() # 4.03.06.06.03 # 获取新苹果位置
                draw_apple() # 4.03.06.06.04 # 画新的苹果
                increment_score()  # 增加成绩

            else : # 4.03.06.07 如果下一步没有遇到苹果 也没有遇到墙，那么可能是遇到了 空白区域 或者 遇到了自己的身体

                clear_snake_tail() # 4.03.06.07.01 前行一步 意味着 自己原来的尾巴位置 应该 变成空白区域，所以删掉旧的尾巴
                drop_snake_tail() # 4.03.06.07.02

                if is_snake_next_head_cover_body(nextSnakeHead): break # 4.03.06.07.03 如果碰到了自己的身体则 本局结束

                else :# 4.03.06.07.04 什么都没有碰到也没吃到苹果，则蛇头顺利前行一步，下一个位置变成蛇头

                    add_snake_head(nextSnakeHead) # 4.03.06.07.04.01 新的蛇头数据放入蛇列表数据开头
                    draw_snake_head() # 4.03.06.07.04.02 画新的蛇头（身体不需要重新画）

        # 4.03.07 打印游戏信息，包括分数
        #windows 可以使用微软雅黑microsoftyaheimicrosoftyaheiui字体
        display_info(get_game_over_info(), defaultFontName, 20, yellow, black,True)

# 程序入口
if __name__ == '__main__':
    main()