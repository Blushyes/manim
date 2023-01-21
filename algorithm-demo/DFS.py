from manimlib import *
import random

# 渐变所需时间
FADE_TIME = 0.3
# 滑块移动时间
MOVE_TIME = 0.3

# 生成得意黑文本（需要安装得意黑字体）
def create_text(text = '', font = 'Smiley Sans', font_size = 30):
    return Text(text, font=font, font_size=font_size)

# 生成陆地或者海洋块
def create_block(tp):
    sq = Square(0.7)
    sq.set_fill(BLUE if tp == 0 else GREEN, 2)
    label = Text(str(tp), font_size=30, font='Smiley Sans')
    sq.add(label)
    return sq

# 根据矩阵生成VGroup
def create_block_group(grid):
    res = VGroup()
    for i in grid:
        inner = VGroup()
        for j in i:
            inner.add(create_block(j))
        inner.arrange(RIGHT, buff=0)
        res.add(inner)
    res.arrange(DOWN, buff=0)
    return res

# 生成新滑块
def create_slider(x, y, z = 0):
    sq =  Square(0.7, fill_opacity=0.5, color=RED)
    sq.set_x(x)
    sq.set_y(y)
    sq.set_z(z)
    return sq

# 生成随机测试集
def create_grid(x, y):
    random.seed()
    grid = []
    for i in range(x):
        inner = []
        for j in range(y):
            inner.append(0 if random.random() < 0.7 else 1)
        grid.append(inner)
    return grid


class DFS(Scene):
    def construct(self):
        # 调整相机距离
        # self.camera.frame.set_width(23)

        self.camera.frame.set_width(30)

        # grid = [[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        #         [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
        #         [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        #         [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]]

        grid = create_grid(20, 35)
        print(grid)

        group = create_block_group(grid)
        # group.shift(UP * 0.3)
        self.add(group)

        slider = create_slider(group[0][0].get_x(), group[0][0].get_y())
        self.add(slider)

        ans_text = create_text('max ans = 0')
        ans_text.next_to(group, UP)
        self.add(ans_text)

        ans = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                tmp = ans
                self.remove(slider)
                self.play(slider.animate.move_to(group[i][j]), run_time=MOVE_TIME)
                ans = max(self.dfs(grid, i, j, group, slider), ans)
                new_text = create_text('max ans = ' + str(ans))
                new_text.next_to(group, UP)
                if ans != tmp:
                    self.play(Transform(ans_text, new_text), run_time=0.5)

    # LeetCode官方题解改
    def dfs(self, grid, cur_i, cur_j, group, slider):
        if grid[cur_i][cur_j] != 1:
            return 0

        # 替换
        now = group[cur_i][cur_j]
        grid[cur_i][cur_j] = 0
        newBLock = create_block(0)
        newBLock.set_x(now.get_x())
        newBLock.set_y(now.get_y())
        grid[cur_i][cur_j] = newBLock

        self.remove(now)
        self.add(newBLock, slider)
        self.bring_to_back(newBLock)

        ans = 1
        for di, dj in [[0, -1], [1, 0], [-1, 0], [0, 1]]:
            sliders = []
            next_i, next_j = cur_i + di, cur_j + dj

            if 0 <= next_i < len(grid) and 0 <= next_j < len(grid[0]) and grid[next_i][next_j] == 1:
                group_next = group[next_i][next_j]
                newSlider = create_slider(group_next.get_x(), group_next.get_y())
                sliders.append(newSlider)

                self.play(FadeIn(newSlider), run_time=FADE_TIME)

                ans += self.dfs(grid, next_i, next_j, group, newSlider)

                self.play(FadeOut(newSlider), run_time=FADE_TIME)

        return ans