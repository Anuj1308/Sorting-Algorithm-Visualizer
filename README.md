#Advanced Sorting Algorithm Visualizer

A professional, feature-rich, and educational Python tool to **visualize sorting algorithms** in real time using an interactive and modern UI with tkinter and matplotlib. Designed for students, teachers, interview preparation, and data structure enthusiasts.

---

##Features

- **Real-Time Sorting Animation**: Visualize each step of Bubble Sort, Merge Sort, Quick Sort, Insertion Sort, and Selection Sort
- **Matplotlib Integration**: Professional bar chart animation embedded in the tkinter GUI
- **Algorithm Statistics**: Tracks and displays element comparisons and swaps in real-time
- **Interactive UI**: Modern controls for algorithm selection, array size, animation speed, and process management (Generate, Start, Stop, Reset)
- **Color-Coded Bars**: Highlights comparisons, swaps, pivots, sorted/unsorted regions
- **Responsive Design**: Seamlessly adapts to any array size (10-200 elements)
- **Robust & Threaded**: Background sorting keeps the GUI smooth and interactive


---

##Getting Started

### 1. Prerequisites

Ensure you have **Python 3.6+** and the following libraries:
- tkinter (usually included with Python)
- matplotlib
- numpy

Install missing libraries with:
```bash
pip install tkinter matplotlib numpy
```

### 2. Run the Visualizer
```bash
python advanced_sorting_visualizer.py
```

---

##Usage

1. **Select Algorithm**: Choose from Bubble, Quick, Merge, Insertion, or Selection sort
2. **Adjust Settings**: Set array size (10-200) and animation speed (1-500ms)
3. **Generate Array**: Click to create a new randomized array
4. **Sort**: Click start and watch the algorithm animate step-by-step
5. **Monitor Stats**: Observe swap and comparison counters in real-time

---

##Supported Algorithms

| Algorithm        | Average Time   | Worst Case    | Space    | Stable?  |
|------------------|---------------|--------------|----------|----------|
| Bubble Sort      | O(n²)         | O(n²)        | O(1)     | Yes      |
| Quick Sort       | O(n log n)    | O(n²)        | O(log n) | No       |
| Merge Sort       | O(n log n)    | O(n log n)   | O(n)     | Yes      |
| Insertion Sort   | O(n²)         | O(n²)        | O(1)     | Yes      |
| Selection Sort   | O(n²)         | O(n²)        | O(1)     | No       |

