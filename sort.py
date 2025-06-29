import time
import random
from IPython.display import clear_output

class SortGame:
    """
    ソートゲームのクラス
    """
    def __init__(self, array, shuffle=False, delay=0, check_option=1):
        self.array = array.copy()
        self.sorted_array = sorted(array.copy())
        self.comparisons = 0
        self.swaps = 0
        self.delay = delay
        self.check_option = check_option
        self.sorted_indices = set()
        self.shuffle = shuffle
        if shuffle:
            random.shuffle(self.array)
            self.display(title='シャッフルしました')
        else:
            self.display()

    def __len__(self):
        return len(self.array)


    def to_string(self, block = "🟦", highlight_indices=None, highlight="🟥", title="リストの状態"):
        """配列を横棒グラフで可視化"""
        sb = []
        sb.append(f"{title}")

        for i, value in enumerate(self.array):
            # 棒グラフの作成
            if highlight_indices and i in highlight_indices:
                bar = highlight * value
            elif i in self.sorted_indices:
                bar = "🟩" * value
            else:
                bar = block * value
            sb.append(f"[{i:2d}] {bar}")

        # 統計情報
        sb.append(f"📊 比較回数: {self.comparisons}, 交換回数: {self.swaps}")
        sb.append("-" * 60)
        return '\n'.join(sb)

    def __repr__(self):
        return self.to_string()

    def display(self, block="🟦", highlight_indices=None, highlight="🟥", title="リストの状態"):
        print(self.to_string(block=block, highlight_indices=highlight_indices, highlight=highlight, title=title))

    def compare(self, i, j, swap=False):
        """要素を比較し、結果を可視化"""
        self.comparisons += 1
        result = self.array[i] > self.array[j]

        block = "" if self.shuffle else "🟦"
        if result:
            self.display(block, highlight_indices=[i, j], highlight="🟥", title=f"🔍 [{i}]と[{j}]を比較")
        else:
            self.display(block, highlight_indices=[i, j], highlight="🟨", title=f"🔍 [{i}]と[{j}]を比較")

        if self.delay > 0:
            time.sleep(self.delay)
            clear_output()

        if swap:
            self.swap(i, j)
        else:
            return result

    def swap(self, i, j):
        self.swaps += 1

        # 交換実行
        self.array[i], self.array[j] = self.array[j], self.array[i]

        # 交換前の状態
        if self.delay > 0:
            if self.check_option == 1:
                self.check_sorted(0, 1)
            elif self.check_option == -1:
                self.check_sorted(-1, -1)

        block = "" if self.shuffle else "🟦"

        self.display(block=block, highlight_indices=[i, j], highlight="🟨", title=f"🔄 [{i}]と[{j}]を交換")

        if self.delay > 0:
            time.sleep(self.delay)
            clear_output()
        elif self.shuffle:
            self.check_sorted(0, 1)
            if len(self.sorted_indices) != len(self.array):
                self.sorted_indices = set()
            else:
                self.display(block="🟩", title=f"☑️ ソート完了")


    def check_sorted(self, start=-1, delta=-1):
        if start < 0:
            start = len(self.array) + start
        if delta < 0:
            for i in range(start, -1, -1):
                if self.sorted_array[i] != self.array[i]:
                    return
                self.sorted_indices.add(i)
        else:
            for i in range(start, len(self.array)):
                if self.sorted_array[i] != self.array[i]:
                    return
                self.sorted_indices.add(i)

