"""
Sorting Algorithm Visualizer (Tkinter)
Run:  python sorting_visualizer.py
"""

import random
import tkinter as tk
from tkinter import ttk

# ---------------------------------------------------------------

def bubble_sort(a):
    n = len(a)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
            yield [j, j + 1]


def selection_sort(a):
    n = len(a)
    for i in range(n):
        smallest = i
        for j in range(i + 1, n):
            yield [i, j, smallest]
            if a[j] < a[smallest]:
                smallest = j
        a[i], a[smallest] = a[smallest], a[i]
        yield [i, smallest]


def insertion_sort(a):
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            yield [j, j + 1]
            j -= 1
        a[j + 1] = key
        yield [j + 1]


def quick_sort(a, low=0, high=None):
    if high is None:
        high = len(a) - 1
    if low < high:
        pivot = a[high]
        i = low
        for j in range(low, high):
            yield [j, high]
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
                yield [i, j]
        a[i], a[high] = a[high], a[i]
        yield [i, high]
        yield from quick_sort(a, low, i - 1)
        yield from quick_sort(a, i + 1, high)


def merge_sort(a, low=0, high=None):
    if high is None:
        high = len(a) - 1
    if low >= high:
        return
    mid = (low + high) // 2
    yield from merge_sort(a, low, mid)
    yield from merge_sort(a, mid + 1, high)

    left = a[low:mid + 1]
    right = a[mid + 1:high + 1]
    i = j = 0
    k = low
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            a[k] = left[i]
            i += 1
        else:
            a[k] = right[j]
            j += 1
        yield [k]
        k += 1
    while i < len(left):
        a[k] = left[i]
        i += 1
        yield [k]
        k += 1
    while j < len(right):
        a[k] = right[j]
        j += 1
        yield [k]
        k += 1


ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Quick Sort": quick_sort,
    "Merge Sort": merge_sort,
}


# ---------------------------------------------------------------
# The GUI
# ---------------------------------------------------------------

class SortingVisualizer:
    WIDTH = 800
    HEIGHT = 400

    def __init__(self, root):
        self.root = root
        root.title("Sorting Algorithm Visualizer")

        self.data = []
        self.generator = None
        self.running = False
        self.steps = 0

        self.build_controls()

        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT,
                                bg="white", highlightthickness=0)
        self.canvas.pack(padx=10, pady=(0, 10))

        self.status = tk.Label(root, text="Steps: 0", font=("Arial", 11))
        self.status.pack(pady=(0, 10))

        self.new_data()

    # ---- widgets ----
    def build_controls(self):
        bar = tk.Frame(self.root)
        bar.pack(pady=10)

        self.algo_box = ttk.Combobox(bar, values=list(ALGORITHMS),
                                     state="readonly", width=15)
        self.algo_box.current(0)
        self.algo_box.grid(row=0, column=0, padx=5)

        tk.Button(bar, text="New Array", command=self.new_data)\
            .grid(row=0, column=1, padx=5)

        self.start_btn = tk.Button(bar, text="Start", width=8,
                                   command=self.toggle)
        self.start_btn.grid(row=0, column=2, padx=5)

        tk.Label(bar, text="Size").grid(row=0, column=3)
        self.size_scale = tk.Scale(bar, from_=10, to=150, orient="horizontal",
                                   length=120, command=lambda _: self.new_data())
        self.size_scale.set(50)
        self.size_scale.grid(row=0, column=4, padx=5)

        tk.Label(bar, text="Speed").grid(row=0, column=5)
        self.speed_scale = tk.Scale(bar, from_=1, to=100, orient="horizontal",
                                    length=120)
        self.speed_scale.set(60)
        self.speed_scale.grid(row=0, column=6, padx=5)

    # ---- data ----
    def new_data(self):
        self.running = False
        self.generator = None
        self.steps = 0
        self.start_btn.config(text="Start")
        n = self.size_scale.get()
        self.data = random.sample(range(5, 400), n) if n <= 395 else []
        self.draw()

    # ---- drawing ----
    def draw(self, highlight=(), done=False):
        self.canvas.delete("all")
        n = len(self.data)
        if n == 0:
            return
        bar_w = self.WIDTH / n
        biggest = max(self.data)
        for i, value in enumerate(self.data):
            x0 = i * bar_w
            x1 = x0 + bar_w - 1
            h = value / biggest * (self.HEIGHT - 10)
            y0 = self.HEIGHT - h
            if done:
                color = "#2ecc71"       # green  = finished
            elif i in highlight:
                color = "#e74c3c"       # red    = being compared / moved
            else:
                color = "#3498db"       # blue   = normal
            self.canvas.create_rectangle(x0, y0, x1, self.HEIGHT,
                                         fill=color, outline="")
        self.status.config(text=f"Steps: {self.steps}")

    # ---- animation ----
    def toggle(self):
        if self.running:                       # pause
            self.running = False
            self.start_btn.config(text="Resume")
            return

        if self.generator is None:             # fresh start
            algo = ALGORITHMS[self.algo_box.get()]
            self.generator = algo(self.data)
            self.steps = 0

        self.running = True
        self.start_btn.config(text="Pause")
        self.animate()

    def animate(self):
        if not self.running:
            return
        try:
            highlight = next(self.generator)
            self.steps += 1
            self.draw(highlight)
            delay = max(1, 101 - self.speed_scale.get())   # higher speed = shorter delay
            self.root.after(delay, self.animate)
        except StopIteration:
            self.running = False
            self.generator = None
            self.start_btn.config(text="Start")
            self.draw(done=True)


if __name__ == "__main__":
    root = tk.Tk()
    SortingVisualizer(root)
    root.mainloop()