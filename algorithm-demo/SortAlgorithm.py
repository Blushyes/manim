from manimlib import *

# 交换一次所需要的时间
MOVE_TIME = 1

# 排序算法演示
class SortAlgorithm(object):
    def __init__(self, arr, scene : Scene, color=RED, width=0.2, move_time=0.1, buff=0.1, scan=False):
        self._run_time = move_time
        self._width = width
        self._color = color
        self._buff = buff
        self._scan = scan
        self.__size = 0.7
        self.scene = scene
        self.arr = list(arr)
        self._max = max(arr)
        self.group = self._group()
        scene.add(self.group)

    # 设置柱体属性
    def set_pillar(self, color):
        self._color = color

    # 按索引设置柱体颜色，有些排序可能会用到，比如说快速排序标出哨兵
    def set_color(self, index, color):
        self.group[index].set_fill(color=color)

    # 设置柱体宽度
    def set_width(self, width):
        self._width = width

    # 设置柱体间距
    def set_buff(self, buff):
        self._buff = buff

    # 设置arr
    def set_arr(self, arr):
        self.arr = list(arr)

    # 生成一个排序柱
    def _pillar(self, height):
        # height / 15
        rect = Rectangle(height=FRAME_HEIGHT * (height / self._max), width=self._width)
        rect.set_fill(self._color, opacity=100)
        rect.set_stroke(opacity=0)
        return rect

    # 根据arr创建一个VGroup
    def _group(self):
        res = VGroup()
        res.add(*[self._pillar(block) for block in self.arr])
        res.arrange(RIGHT, aligned_edge=DOWN, buff=self._buff)
        return res

    # 交换
    def _exchange(self, a, b):
        if self._scan:
            self.group[a].set_fill(color=YELLOW)
            self.group[b].set_fill(color=YELLOW)
        
        self.scene.play(self.group[a].animate.shift((self.group[b].get_x() - self.group[a].get_x()) * RIGHT), self.group[b].animate.shift((self.group[a].get_x() - self.group[b].get_x()) * RIGHT), run_time=self._run_time)

    # 获取所有的柱体
    def get_group(self):
        return self.group

    # 交换后更新
    def update(self, arr):
        res = None
        for i in range(len(arr)):
            if self.arr[i] == arr[i]:
                continue
            if res is None:
                res = i
            else:
                self._exchange(res, i)
                self.arr[res], self.arr[i] = self.arr[i], self.arr[res]
                self.scene.remove(self.group)
                self.group = self._group()
                self.scene.add(self.group)
                break

    # 静态更新
    def static_update(self, arr):
        for i in range(len(arr)):
            if self.arr[i] == arr[i]:
                continue

            self.arr[i] = arr[i]
            tmp = self._group()
            self.scene.play(FadeTransform(self.group, tmp), run_time=self._run_time)
            self.group = tmp
            break

# 用选择排序举例
def select_sort(arr, sa):
    for i in range(len(arr)):
        mi = i
        for j in range(i, len(arr)):
            if arr[j] < arr[mi]:
                mi = j
        arr[mi], arr[i] = arr[i], arr[mi]
        # 交换后进行更新
        sa.update(arr)


class SortAlgorithmDemo(Scene):
    def construct(self):
        arr = [3, 2, 2, 1, 5, 3, 6, 9, 1, 0]
        sa = SortAlgorithm(arr, self, BLUE, FRAME_WIDTH / len(arr), MOVE_TIME, 0)
        select_sort(arr, sa)
        print(arr)