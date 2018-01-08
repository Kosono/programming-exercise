class RingBuffer(object):
    """リングバッファのクラス"""

    def __init__(self, capacity):
        self.capacity = capacity
        self.lst = [0] * capacity
        self.begin = 0
        self.end = 0
        self.judge_full = 0  # リングバッファが全て埋まっているかどうかを判別する変数
        # 埋まっている時に1,埋まっていない時に0を返す

    def append_front(self, item):
        self.begin = (self.begin + self.capacity - 1) % self.capacity
        self.lst[self.begin] = item
        if self.judge_full == 1:
            self.end = self.begin
        if self.begin == self.end:
            self.judge_full = 1

    def append_back(self, item):
        self.lst[self.end] = item
        self.end = (self.end + 1) % self.capacity
        if self.judge_full == 1:
            self.begin = self.end
        if self.begin == self.end:
            self.judge_full = 1

    def pop_front(self):
        number = self.lst[self.begin]
        self.begin = (self.begin + 1) % self.capacity
        self.judge_full = 0
        return number

    def pop_back(self):
        self.end = (self.end + self.capacity - 1) % self.capacity
        number = self.lst[self.end]
        self.judge_full = 0
        return number

    def get_list(self):
        """num_element:リングバッファ内の要素の数
           lst:リングバッファ内の配列"""

        if self.judge_full == 0:
            num_element = (
                self.end - self.begin + self.capacity) % self.capacity
        else:
            num_element = self.capacity
        lst = [
            self.lst[(self.begin + i) % self.capacity]
            for i in range(num_element)
        ]
        print(lst)

    @classmethod
    def sample(cls, capacity):
        buf_ring = cls(capacity=capacity)
        buf_ring.append_front(1)
        buf_ring.append_front(2)
        buf_ring.append_front(3)
        buf_ring.get_list()
        buf_ring.append_back(4)
        buf_ring.append_back(5)
        buf_ring.append_back(6)
        buf_ring.append_back(7)
        buf_ring.get_list()
        buf_ring.pop_front()
        buf_ring.pop_front()
        buf_ring.get_list()
        buf_ring.pop_back()
        buf_ring.get_list()
        buf_ring.append_front(8)
        buf_ring.get_list()


def main():
    RingBuffer.sample(5)


if __name__ == '__main__':
    main()