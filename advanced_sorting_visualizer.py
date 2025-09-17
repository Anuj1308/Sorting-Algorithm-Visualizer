
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time
import threading

class AdvancedSortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Sorting Algorithm Visualizer")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')

        # Initialize variables
        self.array = []
        self.array_size = 50
        self.speed = 100
        self.sorting = False
        self.algorithm = "Bubble Sort"
        self.comparisons = 0
        self.swaps = 0

        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.fig.patch.set_facecolor('#1a1a1a')
        self.ax.set_facecolor('#2d2d2d')

        # Create UI
        self.create_interface()
        self.generate_array()

    def create_interface(self):
        """Create the enhanced user interface"""
        # Title frame
        title_frame = tk.Frame(self.root, bg='#1a1a1a')
        title_frame.pack(pady=10)

        title_label = tk.Label(
            title_frame,
            text="🔄 Advanced Sorting Algorithm Visualizer",
            font=('Arial', 24, 'bold'),
            bg='#1a1a1a',
            fg='#00ff88'
        )
        title_label.pack()

        # Control panel frame
        control_panel = tk.Frame(self.root, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        control_panel.pack(pady=10, padx=20, fill=tk.X)

        # First row of controls
        row1_frame = tk.Frame(control_panel, bg='#2d2d2d')
        row1_frame.pack(pady=10)

        # Algorithm selection
        tk.Label(row1_frame, text="Algorithm:", font=('Arial', 12, 'bold'), bg='#2d2d2d', fg='white').grid(row=0, column=0, padx=10)
        self.algorithm_var = tk.StringVar(value="Bubble Sort")
        algorithm_menu = ttk.Combobox(
            row1_frame,
            textvariable=self.algorithm_var,
            values=["Bubble Sort", "Quick Sort", "Merge Sort", "Insertion Sort", "Selection Sort"],
            state="readonly",
            width=15,
            font=('Arial', 10)
        )
        algorithm_menu.grid(row=0, column=1, padx=10)

        # Array size
        tk.Label(row1_frame, text="Array Size:", font=('Arial', 12, 'bold'), bg='#2d2d2d', fg='white').grid(row=0, column=2, padx=10)
        self.size_var = tk.IntVar(value=50)
        size_scale = tk.Scale(
            row1_frame,
            from_=10,
            to=200,
            orient=tk.HORIZONTAL,
            variable=self.size_var,
            bg='#2d2d2d',
            fg='white',
            highlightbackground='#2d2d2d',
            troughcolor='#4d4d4d',
            activebackground='#00ff88',
            length=150
        )
        size_scale.grid(row=0, column=3, padx=10)

        # Speed control
        tk.Label(row1_frame, text="Speed (ms):", font=('Arial', 12, 'bold'), bg='#2d2d2d', fg='white').grid(row=0, column=4, padx=10)
        self.speed_var = tk.IntVar(value=100)
        speed_scale = tk.Scale(
            row1_frame,
            from_=1,
            to=500,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            bg='#2d2d2d',
            fg='white',
            highlightbackground='#2d2d2d',
            troughcolor='#4d4d4d',
            activebackground='#ff6b6b',
            length=150
        )
        speed_scale.grid(row=0, column=5, padx=10)

        # Second row - buttons and stats
        row2_frame = tk.Frame(control_panel, bg='#2d2d2d')
        row2_frame.pack(pady=10)

        # Buttons
        button_style = {
            'font': ('Arial', 11, 'bold'),
            'padx': 15,
            'pady': 8,
            'relief': tk.FLAT,
            'bd': 0,
            'cursor': 'hand2'
        }

        generate_btn = tk.Button(
            row2_frame,
            text="🎲 Generate New Array",
            command=self.generate_array,
            bg='#4ecdc4',
            fg='white',
            **button_style
        )
        generate_btn.grid(row=0, column=0, padx=5)

        self.start_btn = tk.Button(
            row2_frame,
            text="▶️ Start Sorting",
            command=self.start_sorting,
            bg='#2ecc71',
            fg='white',
            **button_style
        )
        self.start_btn.grid(row=0, column=1, padx=5)

        self.stop_btn = tk.Button(
            row2_frame,
            text="⏹️ Stop",
            command=self.stop_sorting,
            bg='#e74c3c',
            fg='white',
            state=tk.DISABLED,
            **button_style
        )
        self.stop_btn.grid(row=0, column=2, padx=5)

        reset_btn = tk.Button(
            row2_frame,
            text="🔄 Reset",
            command=self.reset_stats,
            bg='#f39c12',
            fg='white',
            **button_style
        )
        reset_btn.grid(row=0, column=3, padx=5)

        # Statistics
        stats_frame = tk.Frame(row2_frame, bg='#2d2d2d')
        stats_frame.grid(row=0, column=4, padx=20)

        self.comparisons_label = tk.Label(
            stats_frame,
            text="Comparisons: 0",
            font=('Arial', 11, 'bold'),
            bg='#2d2d2d',
            fg='#3498db'
        )
        self.comparisons_label.pack(side=tk.LEFT, padx=10)

        self.swaps_label = tk.Label(
            stats_frame,
            text="Swaps: 0",
            font=('Arial', 11, 'bold'),
            bg='#2d2d2d',
            fg='#e74c3c'
        )
        self.swaps_label.pack(side=tk.LEFT, padx=10)

        # Status label
        self.status_label = tk.Label(
            self.root,
            text="🎯 Ready to sort - Select an algorithm and click Start Sorting",
            font=('Arial', 12, 'bold'),
            bg='#1a1a1a',
            fg='#00ff88'
        )
        self.status_label.pack(pady=5)

        # Matplotlib canvas
        canvas_frame = tk.Frame(self.root, bg='#1a1a1a')
        canvas_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def generate_array(self):
        """Generate a new random array"""
        if self.sorting:
            return

        self.array_size = self.size_var.get()
        self.array = list(range(1, self.array_size + 1))
        random.shuffle(self.array)
        self.reset_stats()
        self.draw_array()
        self.status_label.config(text=f"🎲 Generated new array with {self.array_size} elements")

    def draw_array(self, colors=None, title="Array Visualization"):
        """Draw the array using matplotlib"""
        self.ax.clear()

        if colors is None:
            colors = ['#3498db'] * len(self.array)

        bars = self.ax.bar(range(len(self.array)), self.array, color=colors, edgecolor='#1a1a1a')

        self.ax.set_xlim(-0.6, len(self.array))
        self.ax.set_ylim(0, max(self.array) * 1.1)
        self.ax.set_title(title, color='white', fontsize=16, fontweight='bold')
        self.ax.set_facecolor('#2d2d2d')
        self.ax.tick_params(colors='white')

        # Remove ticks for cleaner look
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        self.canvas.draw()

    def start_sorting(self):
        """Start the sorting animation"""
        if self.sorting or not self.array:
            return

        self.sorting = True
        self.start_btn.config(state=tk.DISABLED, bg='#95a5a6')
        self.stop_btn.config(state=tk.NORMAL, bg='#e74c3c')

        self.algorithm = self.algorithm_var.get()
        self.speed = self.speed_var.get()

        self.status_label.config(text=f"🔄 Running {self.algorithm}...")

        # Start sorting in a separate thread
        thread = threading.Thread(target=self.execute_sorting)
        thread.daemon = True
        thread.start()

    def stop_sorting(self):
        """Stop the sorting process"""
        self.sorting = False
        self.start_btn.config(state=tk.NORMAL, bg='#2ecc71')
        self.stop_btn.config(state=tk.DISABLED, bg='#95a5a6')
        self.status_label.config(text="⏹️ Sorting stopped")

    def reset_stats(self):
        """Reset sorting statistics"""
        self.comparisons = 0
        self.swaps = 0
        self.update_stats()

    def update_stats(self):
        """Update statistics display"""
        self.comparisons_label.config(text=f"Comparisons: {self.comparisons}")
        self.swaps_label.config(text=f"Swaps: {self.swaps}")

    def execute_sorting(self):
        """Execute the selected sorting algorithm"""
        try:
            if self.algorithm == "Bubble Sort":
                self.bubble_sort()
            elif self.algorithm == "Quick Sort":
                self.quick_sort(0, len(self.array) - 1)
            elif self.algorithm == "Merge Sort":
                self.merge_sort_wrapper()
            elif self.algorithm == "Insertion Sort":
                self.insertion_sort()
            elif self.algorithm == "Selection Sort":
                self.selection_sort()

            if self.sorting:
                self.draw_array(['#2ecc71'] * len(self.array), f"✅ {self.algorithm} Complete!")
                self.status_label.config(text=f"✅ {self.algorithm} completed successfully!")

        except Exception as e:
            self.status_label.config(text=f"❌ Error: {str(e)}")

        finally:
            self.sorting = False
            self.start_btn.config(state=tk.NORMAL, bg='#2ecc71')
            self.stop_btn.config(state=tk.DISABLED, bg='#95a5a6')

    def bubble_sort(self):
        """Bubble sort with enhanced visualization"""
        n = len(self.array)
        for i in range(n):
            if not self.sorting:
                break

            swapped = False
            for j in range(0, n - i - 1):
                if not self.sorting:
                    break

                self.comparisons += 1
                colors = ['#3498db'] * len(self.array)
                colors[j] = '#f39c12'  # Current element
                colors[j + 1] = '#f39c12'  # Comparing element

                # Already sorted elements in green
                for k in range(n - i, n):
                    colors[k] = '#2ecc71'

                self.draw_array(colors, f"Bubble Sort - Pass {i+1}, Comparing {self.array[j]} and {self.array[j+1]}")
                self.update_stats()
                time.sleep(self.speed / 1000.0)

                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                    self.swaps += 1
                    swapped = True

                    # Show swap with red color
                    colors[j] = '#e74c3c'
                    colors[j + 1] = '#e74c3c'
                    self.draw_array(colors, f"Bubble Sort - Swapped {self.array[j+1]} and {self.array[j]}")
                    self.update_stats()
                    time.sleep(self.speed / 1000.0)

            if not swapped:  # Array is already sorted
                break

    def quick_sort(self, low, high):
        """Quick sort with visualization"""
        if not self.sorting or low >= high:
            return

        pivot_index = self.partition(low, high)
        if not self.sorting:
            return

        self.quick_sort(low, pivot_index - 1)
        self.quick_sort(pivot_index + 1, high)

    def partition(self, low, high):
        """Partition function for quick sort"""
        pivot = self.array[high]
        i = low - 1

        for j in range(low, high):
            if not self.sorting:
                break

            self.comparisons += 1
            colors = ['#3498db'] * len(self.array)
            colors[high] = '#f39c12'  # Pivot
            colors[j] = '#9b59b6'     # Current element
            if i >= 0:
                colors[i] = '#e74c3c'  # Last smaller element

            self.draw_array(colors, f"Quick Sort - Pivot: {pivot}, Comparing: {self.array[j]}")
            self.update_stats()
            time.sleep(self.speed / 1000.0)

            if self.array[j] <= pivot:
                i += 1
                if i != j:
                    self.array[i], self.array[j] = self.array[j], self.array[i]
                    self.swaps += 1

        # Place pivot in correct position
        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        self.swaps += 1

        colors = ['#3498db'] * len(self.array)
        colors[i + 1] = '#2ecc71'  # Pivot in correct position
        self.draw_array(colors, f"Quick Sort - Pivot {pivot} placed at position {i+1}")
        self.update_stats()
        time.sleep(self.speed / 1000.0)

        return i + 1

    def merge_sort_wrapper(self):
        """Wrapper for merge sort"""
        self.merge_sort(0, len(self.array) - 1)

    def merge_sort(self, left, right):
        """Merge sort with visualization"""
        if not self.sorting or left >= right:
            return

        mid = (left + right) // 2

        # Highlight current section
        colors = ['#3498db'] * len(self.array)
        for i in range(left, right + 1):
            colors[i] = '#f39c12'

        self.draw_array(colors, f"Merge Sort - Dividing: [{left}..{right}]")
        time.sleep(self.speed / 1000.0)

        self.merge_sort(left, mid)
        self.merge_sort(mid + 1, right)
        self.merge(left, mid, right)

    def merge(self, left, mid, right):
        """Merge function for merge sort"""
        if not self.sorting:
            return

        left_arr = self.array[left:mid + 1]
        right_arr = self.array[mid + 1:right + 1]

        i = j = 0
        k = left

        while i < len(left_arr) and j < len(right_arr):
            if not self.sorting:
                return

            self.comparisons += 1
            colors = ['#3498db'] * len(self.array)

            # Color the two subarrays being merged
            for idx in range(left, mid + 1):
                colors[idx] = '#e74c3c'
            for idx in range(mid + 1, right + 1):
                colors[idx] = '#9b59b6'
            colors[k] = '#2ecc71'  # Current merge position

            self.draw_array(colors, f"Merge Sort - Merging: {left_arr[i]} vs {right_arr[j]}")
            self.update_stats()
            time.sleep(self.speed / 1000.0)

            if left_arr[i] <= right_arr[j]:
                self.array[k] = left_arr[i]
                i += 1
            else:
                self.array[k] = right_arr[j]
                j += 1
            k += 1

        # Copy remaining elements
        while i < len(left_arr):
            if not self.sorting:
                return
            self.array[k] = left_arr[i]
            i += 1
            k += 1

        while j < len(right_arr):
            if not self.sorting:
                return
            self.array[k] = right_arr[j]
            j += 1
            k += 1

        # Show completed merge
        colors = ['#3498db'] * len(self.array)
        for i in range(left, right + 1):
            colors[i] = '#2ecc71'
        self.draw_array(colors, f"Merge Sort - Merged [{left}..{right}]")
        time.sleep(self.speed / 1000.0)

    def insertion_sort(self):
        """Insertion sort with visualization"""
        for i in range(1, len(self.array)):
            if not self.sorting:
                break

            key = self.array[i]
            j = i - 1

            colors = ['#3498db'] * len(self.array)
            colors[i] = '#f39c12'  # Current element to insert

            # Already sorted part in green
            for k in range(i):
                colors[k] = '#2ecc71'

            self.draw_array(colors, f"Insertion Sort - Inserting {key}")
            time.sleep(self.speed / 1000.0)

            while j >= 0 and self.array[j] > key:
                if not self.sorting:
                    break

                self.comparisons += 1
                self.swaps += 1

                self.array[j + 1] = self.array[j]

                colors = ['#2ecc71'] * (j + 1) + ['#e74c3c'] + ['#3498db'] * (len(self.array) - j - 2)
                colors[i] = '#f39c12'

                self.draw_array(colors, f"Insertion Sort - Moving {self.array[j]} right")
                self.update_stats()
                time.sleep(self.speed / 1000.0)

                j -= 1

            self.array[j + 1] = key

    def selection_sort(self):
        """Selection sort with visualization"""
        for i in range(len(self.array)):
            if not self.sorting:
                break

            min_idx = i
            colors = ['#3498db'] * len(self.array)
            colors[i] = '#f39c12'  # Current position

            # Already sorted part in green
            for k in range(i):
                colors[k] = '#2ecc71'

            for j in range(i + 1, len(self.array)):
                if not self.sorting:
                    break

                self.comparisons += 1
                colors[j] = '#9b59b6'  # Current comparison
                colors[min_idx] = '#e74c3c'  # Current minimum

                self.draw_array(colors, f"Selection Sort - Finding minimum, current: {self.array[j]}")
                self.update_stats()
                time.sleep(self.speed / 1000.0)

                if self.array[j] < self.array[min_idx]:
                    min_idx = j

                colors[j] = '#3498db'  # Reset color

            if min_idx != i:
                self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
                self.swaps += 1

                colors = ['#3498db'] * len(self.array)
                colors[i] = '#2ecc71'
                colors[min_idx] = '#e74c3c'

                self.draw_array(colors, f"Selection Sort - Swapped {self.array[min_idx]} with {self.array[i]}")
                self.update_stats()
                time.sleep(self.speed / 1000.0)

def main():
    root = tk.Tk()
    app = AdvancedSortingVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
