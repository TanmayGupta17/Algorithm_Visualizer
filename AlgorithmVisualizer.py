import pygame
import random
import math
import collections

pygame.init()

class DrawInformation:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 25)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_value = min(lst)
        self.max_value = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = round((self.height - self.TOP_PAD) / (self.max_value - self.min_value))
        self.start_x = self.SIDE_PAD // 2

def generate_list(min_value, max_value, n):
    return [random.randint(min_value, max_value) for _ in range(n)]

def draw_sort(draw_info, algo_name, ascending, speed):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.RED)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))
    
    controls = draw_info.FONT.render("R - Reset | Space - Start Sorting | A - Ascending | D - Descending | +/- - Speed", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 33))
    
    more1 = draw_info.FONT.render("I - Insertion sort | B - Bubble Sort | S - Selection Sort", 1, draw_info.BLACK)
    draw_info.window.blit(more1, (draw_info.width / 2 - more1.get_width() / 2, 60))
    
    more2 = draw_info.FONT.render("Q - Quick Sort | M - Merge Sort | H - Heap Sort", 1, draw_info.BLACK)
    draw_info.window.blit(more2, (draw_info.width / 2 - more2.get_width() / 2, 85))

    speed_text = draw_info.FONT.render(f"Speed: {speed}x", 1, draw_info.BLACK)
    draw_info.window.blit(speed_text, (draw_info.width - speed_text.get_width() - 10, 5))

    draw_list(draw_info)
    pygame.display.update()

def draw_graph_screen(draw_info, algo_name, speed):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    
    title = draw_info.FONT.render(f"{algo_name}", 1, draw_info.RED)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))
    
    controls = draw_info.FONT.render("R - Reset | Space - Start Traversal | A - BFS | D - DFS | +/- - Speed", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 33))

    speed_text = draw_info.FONT.render(f"Speed: {speed}x", 1, draw_info.BLACK)
    draw_info.window.blit(speed_text, (draw_info.width - speed_text.get_width() - 10, 5))

    draw_graph(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_value) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]
        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height - y))

    if clear_bg:
        pygame.display.update()

def draw_graph(draw_info, graph=None, visited=None, current_node=None):
    if graph is None:
        graph = {
            'A': ['B', 'C'],
            'B': ['A', 'D', 'E'],
            'C': ['A', 'F'],
            'D': ['B'],
            'E': ['B', 'F'],
            'F': ['C', 'E']
        }
    if visited is None:
        visited = []

    node_radius = 20
    graph_center_x = draw_info.width / 2
    graph_center_y = draw_info.height / 2
    angle_step = 360 / len(graph)
    angle = 0

    node_positions = {}
    for node in graph:
        angle_rad = math.radians(angle)
        x = graph_center_x + 200 * math.cos(angle_rad)
        y = graph_center_y + 200 * math.sin(angle_rad)
        node_positions[node] = (x, y)
        angle += angle_step

    for node in graph:
        for neighbor in graph[node]:
            start_pos = node_positions[node]
            end_pos = node_positions[neighbor]
            pygame.draw.line(draw_info.window, draw_info.BLACK, start_pos, end_pos, 2)

    for node, (x, y) in node_positions.items():
        color = draw_info.RED if node == current_node else (draw_info.GREEN if node in visited else draw_info.BLACK)
        pygame.draw.circle(draw_info.window, color, (int(x), int(y)), node_radius)
        label = draw_info.FONT.render(str(node), 1, draw_info.WHITE)
        draw_info.window.blit(label, (x - label.get_width() / 2, y - label.get_height() / 2))

    pygame.display.update()

def bfs(draw_info, graph, start_node, speed):
    visited = []
    queue = collections.deque([start_node])
    
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.append(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
            draw_graph(draw_info, graph, visited, node)
            pygame.time.wait(int(500 / speed))
            yield True
    
def dfs(draw_info, graph, start_node, speed):
    visited = []
    stack = [start_node]

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.append(node)
            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)
            draw_graph(draw_info, graph, visited, node)
            pygame.time.wait(int(500 / speed))
            yield True

def draw_home(draw_info):
    draw_info.window.fill(draw_info.WHITE)

    title = draw_info.LARGE_FONT.render("Welcome to Algorithm Visualizer", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 100))

    title1 = draw_info.FONT.render("Press 1 for Graph Traversal", 1, draw_info.BLACK)
    draw_info.window.blit(title1, (draw_info.width / 2 - title1.get_width() / 2, 300))
    
    title2 = draw_info.FONT.render("Press 2 for Sorting Algorithms", 1, draw_info.BLACK)
    draw_info.window.blit(title2, (draw_info.width / 2 - title2.get_width() / 2, 350))

    pygame.display.update()

def bubble_sort(draw_info, ascending=True, speed=1):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                pygame.time.wait(int(500 / speed))
                yield True
    return lst

def insertion_sort(draw_info, ascending=True, speed=1):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]
        j = i - 1

        while j >= 0 and ((lst[j] > current and ascending) or (lst[j] < current and not ascending)):
            lst[j + 1] = lst[j]
            j -= 1
            lst[j + 1] = current
            draw_list(draw_info, {j: draw_info.GREEN, i: draw_info.RED}, True)
            pygame.time.wait(int(500 / speed))
            yield True
    return lst

def selection_sort(draw_info, ascending=True, speed=1):
    lst = draw_info.lst

    for i in range(len(lst)):
        min_idx = i
        for j in range(i + 1, len(lst)):
            if (lst[j] < lst[min_idx] and ascending) or (lst[j] > lst[min_idx] and not ascending):
                min_idx = j
                draw_list(draw_info, {j: draw_info.RED, min_idx: draw_info.GREEN}, True)
                pygame.time.wait(int(500 / speed))
                yield True
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, min_idx: draw_info.RED}, True)
        pygame.time.wait(int(500 / speed))
        yield True
    return lst

def quick_sort(draw_info, ascending=True, speed=1):
    lst = draw_info.lst

    def partition(low, high):
        pivot = lst[high]
        i = low - 1

        for j in range(low, high):
            if (lst[j] <= pivot and ascending) or (lst[j] >= pivot and not ascending):
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
                draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
                pygame.time.wait(int(500 / speed))
                yield True

        lst[i + 1], lst[high] = lst[high], lst[i + 1]
        draw_list(draw_info, {i + 1: draw_info.GREEN, high: draw_info.RED}, True)
        pygame.time.wait(int(500 / speed))
        yield True

        return i + 1

    def quick_sort_recursive(low, high):
        if low < high:
            pi = yield from partition(low, high)
            yield from quick_sort_recursive(low, pi - 1)
            yield from quick_sort_recursive(pi + 1, high)

    yield from quick_sort_recursive(0, len(lst) - 1)
    return lst

def merge_sort(draw_info, ascending=True, speed=1):
    lst = draw_info.lst

    def merge(left, right):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if (left[i] < right[j] and ascending) or (left[i] > right[j] and not ascending):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
            draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
            pygame.time.wait(int(500 / speed))
            yield True

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def merge_sort_recursive(lst):
        if len(lst) <= 1:
            return lst

        mid = len(lst) // 2
        left = yield from merge_sort_recursive(lst[:mid])
        right = yield from merge_sort_recursive(lst[mid:])
        yield True

        return (yield from merge(left, right))

    sorted_list = yield from merge_sort_recursive(lst)
    for i, val in enumerate(sorted_list):
        lst[i] = val
        draw_list(draw_info, {i: draw_info.GREEN}, True)
        pygame.time.wait(int(500 / speed))
        yield True
    return lst

def heap_sort(draw_info, ascending=True, speed=1):
    lst = draw_info.lst
    n = len(lst)

    def heapify(n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and ((lst[left] > lst[largest] and ascending) or (lst[left] < lst[largest] and not ascending)):
            largest = left

        if right < n and ((lst[right] > lst[largest] and ascending) or (lst[right] < lst[largest] and not ascending)):
            largest = right

        if largest != i:
            lst[i], lst[largest] = lst[largest], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN, largest: draw_info.RED}, True)
            pygame.time.wait(int(500 / speed))
            yield True
            yield from heapify(n, largest)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(n, i)

    for i in range(n - 1, 0, -1):
        lst[i], lst[0] = lst[0], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, 0: draw_info.RED}, True)
        pygame.time.wait(int(500 / speed))
        yield True
        yield from heapify(i, 0)
    return lst

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100
    lst = generate_list(min_val, max_val, n)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algo = bubble_sort
    sorting_algo_name = "Bubble Sort"
    # sorting_algo_generator = None

    graph_mode = False
    graph_algo_name = "Breadth First Search"
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    start_node = 'A'
    # graph_algo_generator = None

    home_screen = True
    speed = 1  # Initial speed factor

    while run:
        clock.tick(60)

        if home_screen:
            draw_home(draw_info)
        elif graph_mode:
            if sorting:
                try:
                    next(graph_algo_generator)
                except StopIteration:
                    sorting = False
            else:
                draw_graph_screen(draw_info, graph_algo_name, speed)
        else:
            if sorting:
                try:
                    next(sorting_algo_generator)
                except StopIteration:
                    sorting = False
            else:
                draw_sort(draw_info, sorting_algo_name, ascending, speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and not home_screen:
                    lst = generate_list(min_val, max_val, n)
                    draw_info.set_list(lst)
                    sorting = False
                elif event.key == pygame.K_SPACE and not sorting and not home_screen:
                    sorting = True
                    if graph_mode:
                        graph_algo_generator = bfs(draw_info, graph, start_node, speed) if graph_algo_name == "BFS" else dfs(draw_info, graph, start_node, speed)
                    else:
                        sorting_algo_generator = sorting_algo(draw_info, ascending, speed)
                elif event.key == pygame.K_a and not sorting and not home_screen:
                    if graph_mode:
                        graph_algo_name = "Breadth First Search"
                    else:
                        ascending = True
                elif event.key == pygame.K_d and not sorting and not home_screen:
                    if graph_mode:
                        graph_algo_name = "Depth First Search"
                    else:
                        ascending = False
                elif event.key == pygame.K_i and not sorting and not home_screen:
                    sorting_algo = insertion_sort
                    sorting_algo_name = "Insertion Sort"
                elif event.key == pygame.K_b and not sorting and not home_screen:
                    sorting_algo = bubble_sort
                    sorting_algo_name = "Bubble Sort"
                elif event.key == pygame.K_s and not sorting and not home_screen:
                    sorting_algo = selection_sort
                    sorting_algo_name = "Selection Sort"
                elif event.key == pygame.K_q and not sorting and not home_screen:
                    sorting_algo = quick_sort
                    sorting_algo_name = "Quick Sort"
                elif event.key == pygame.K_m and not sorting and not home_screen:
                    sorting_algo = merge_sort
                    sorting_algo_name = "Merge Sort"
                elif event.key == pygame.K_h and not sorting and not home_screen:
                    sorting_algo = heap_sort
                    sorting_algo_name = "Heap Sort"
                elif event.key == pygame.K_1 and not sorting:
                    home_screen = False
                    graph_mode = True
                    draw_home(draw_info)
                elif event.key == pygame.K_2 and not sorting:
                    home_screen = False
                    graph_mode = False
                    draw_home(draw_info)
                elif event.key == pygame.K_f and graph_mode and not sorting:
                    graph_algo_name = "Breadth First Search"
                    sorting = True
                    graph_algo_generator = bfs(draw_info, graph, start_node, speed)
                elif event.key == pygame.K_d and graph_mode and not sorting:
                    graph_algo_name = "Depth First Search"
                    sorting = True
                    graph_algo_generator = dfs(draw_info, graph, start_node, speed)
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS and not home_screen:
                    speed = min(50, speed + 1)
                elif event.key == pygame.K_MINUS and not home_screen:
                    speed = max(1, speed - 1)

    pygame.quit()

if __name__ == "__main__":
    main()
