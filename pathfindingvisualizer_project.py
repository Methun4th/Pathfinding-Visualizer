import pygame
import heapq
from collections import deque
import time

pygame.init()

cell_size = 50

screen = pygame.display.set_mode((600, 750))

maze = [
    [1 for col in range(12)]
    for row in range(12)
]

colors = {
     0: (0, 0, 0),
    1: (255, 255, 255),
    2: (230, 230, 230),
    3: (205, 205, 205),
    4: (180, 180, 180),
    5: (155, 155, 155),
    6: (130, 130, 130),
    7: (105, 105, 105),
    8: (80, 80, 80),
    9: (55, 55, 55)
}

start = None
goal = None

current_algorithm = "A*"

explored_count = 0
path_length = 0
path_cost = 0
execution_time = 0

font = pygame.font.SysFont(None, 25)

pygame.display.set_caption("Pathfinding Visualizer")

def astar(maze, start, goal):

    heap = []

    heapq.heappush(heap,(0, start))

    g_score = {}
    g_score[start] = 0

    parent = {}
    parent[start] = None

    explored = []

    while heap:

        current_f, current = heapq.heappop(heap)

        if current == goal:
            break

        explored.append(current)

        row, col = current

        get_neighbors = [
            (row-1, col),
            (row+1, col),
            (row, col-1),
            (row, col+1)
        ]

        for neighbor in get_neighbors:

            neighbor_row, neighbor_col = neighbor

            if neighbor_row < 0 or neighbor_row >= len(maze):
                continue

            if neighbor_col < 0 or neighbor_col >= len(maze[0]):
                continue

            if maze[neighbor_row][neighbor_col] == 0:
                continue

            move_cost = maze[neighbor_row][neighbor_col]

            tentative_g = g_score[current] + move_cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:

                g_score[neighbor] = tentative_g

                parent[neighbor] = current

                h = abs(neighbor_row - goal[0]) + abs(neighbor_col - goal[1])

                f = tentative_g + h

                heapq.heappush(heap, (f, neighbor))

    path = []

    if goal in parent or start == goal:

        current = goal

        while current is not None:

            path.append(current)

            current = parent[current]

        path.reverse()

    return explored, path

def bfs(maze, start, goal):

    queue = deque()

    queue.append(start)

    visited = set()
    visited.add(start)

    parent = {}
    parent[start] = None

    explored = []

    while queue:

        current = queue.popleft()

        if current == goal:
            break

        explored.append(current)

        row, col = current

        neighbors = [
            (row-1, col),
            (row+1, col),
            (row, col-1),
            (row, col+1)
        ]

        for neighbor in neighbors:

            neighbor_row, neighbor_col = neighbor

            if neighbor_row < 0 or neighbor_row >= len(maze):
                continue

            if neighbor_col < 0 or neighbor_col >= len(maze[0]):
                continue

            if maze[neighbor_row][neighbor_col] == 0:
                continue

            if neighbor in visited:
                continue

            visited.add(neighbor)

            parent[neighbor] = current

            queue.append(neighbor)

    path = []

    if goal in parent:

        current = goal

        while current is not None:

            path.append(current)

            current = parent[current]

        path.reverse()

    return explored, path

def dfs(maze, start, goal):

    stack = []

    stack.append(start)

    visited = set()
    visited.add(start)

    parent = {}
    parent[start] = None

    explored = []

    while stack:

        current = stack.pop()

        if current == goal:
            break

        explored.append(current)

        row, col = current

        neighbors = [
            (row-1, col),
            (row+1, col),
            (row, col-1),
            (row, col+1)
        ]

        for neighbor in neighbors:

            neighbor_row, neighbor_col = neighbor

            if neighbor_row < 0 or neighbor_row >= len(maze):
                continue

            if neighbor_col < 0 or neighbor_col >= len(maze[0]):
                continue

            if maze[neighbor_row][neighbor_col] == 0:
                continue

            if neighbor in visited:
                continue

            visited.add(neighbor)

            parent[neighbor] = current

            stack.append(neighbor)

    path = []

    if goal in parent:

        current = goal

        while current is not None:

            path.append(current)

            current = parent[current]

        path.reverse()

    return explored, path

def dijkstra(maze, start, goal):

    heap = []

    heapq.heappush(heap, (0, start))

    g_score = {}
    g_score[start] = 0

    parent = {}
    parent[start] = None

    explored = []

    while heap:

        current_cost, current = heapq.heappop(heap)

        if current_cost > g_score[current]:
            continue

        if current == goal:
            break

        explored.append(current)

        row, col = current

        neighbors = [
            (row-1, col),
            (row+1, col),
            (row, col-1),
            (row, col+1)
        ]

        for neighbor in neighbors:

            neighbor_row, neighbor_col = neighbor

            if neighbor_row < 0 or neighbor_row >= len(maze):
                continue

            if neighbor_col < 0 or neighbor_col >= len(maze[0]):
                continue

            if maze[neighbor_row][neighbor_col] == 0:
                continue

            move_cost = maze[neighbor_row][neighbor_col]

            tentative_g = g_score[current] + move_cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:

                g_score[neighbor] = tentative_g

                parent[neighbor] = current

                heapq.heappush(heap, (tentative_g, neighbor))

    path = []

    if goal in parent:

        current = goal

        while current is not None:

            path.append(current)

            current = parent[current]

        path.reverse()

    return explored, path

explored_cells = []
final_path = []

explored_index = 0
path_index = 0

animation_index = 0
animation_timer = 0
animation_speed = 100
animation_active = False

warning_message = ""
warning_timer = 0
warning_font= pygame.font.SysFont(None, 30)

clock = pygame.time.Clock()

running = True

while running:

    delta_time = clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                current_algorithm = "BFS"

            elif event.key == pygame.K_2:
                current_algorithm = "DFS"

            elif event.key == pygame.K_3:
                current_algorithm = "Dijkstra"

            elif event.key == pygame.K_4:
                current_algorithm = "A*"

            elif event.key == pygame.K_r:

                explored_cells = []
                final_path = []

                explored_index = 0
                path_index = 0

                animation_timer = 0
                animation_active = False

            elif event.key == pygame.K_c:

                maze = [
                    [1 for col in range(15)]
                    for row in range(15)
                ]

            pygame.display.set_caption(
                f"Pathfinding Visualizer - {current_algorithm}"
            )

            if event.key == pygame.K_SPACE:

                if start and goal:

                    start_time = time.perf_counter()
                    
                    if current_algorithm == "BFS":

                        explored_cells, final_path = bfs(maze, start, goal)

                    elif current_algorithm == "DFS":

                        explored_cells, final_path = dfs(maze, start, goal)

                    elif current_algorithm == "Dijkstra":

                        explored_cells, final_path = dijkstra(maze, start, goal)

                    elif current_algorithm == "A*":

                        explored_cells, final_path = astar(maze, start, goal)

                    end_time = time.perf_counter()

                    execution_time = end_time - start_time

                    explored_count = len(explored_cells)

                    if final_path:

                        path_length = len(final_path) - 1

                        path_cost = sum(
                            maze[row][col]
                            for row, col in final_path[1:]
                        )

                    else:
                        path_length = 0
                        path_cost = 0

                    explored_index = 0
                    path_index = 0
                    animation_timer = 0
                    animation_active = True

                else:

                    warning_message = "Please select the start point and the destination first!"
                    warning_timer = 3000

        if event.type == pygame.MOUSEBUTTONDOWN:

            explored_cells = []
            final_path = []

            explored_index = 0
            path_index = 0
            animation_timer = 0
            animation_active = False

            mouse_X, mouse_Y = event.pos

            if mouse_Y >= 600:
                continue

            row = mouse_Y // cell_size
            col = mouse_X // cell_size

            position = (row, col)

            if event.button == 1:

                if maze[row][col] == 9:
                    maze[row][col] = 0

                else:
                    maze[row][col] += 1

            if event.button == 2:

                if maze[row][col] != 0:
                    start = position

                else:
                    warning_message = "You cannot place the start point on a wall!"
                    warning_timer = 3000

            if event.button == 3:

                if maze[row][col] != 0:
                    goal = position

                else:
                    warning_message = "You cannot place the goal on a wall!"
                    warning_timer = 3000

    if warning_timer > 0:

        warning_timer -= delta_time

    else:

        warning_message = ""
    
    if animation_active:

        animation_timer += delta_time

        if animation_timer >= animation_speed:

            animation_timer = 0

            if explored_index < len(explored_cells):

                explored_index += 1

            elif path_index < len(final_path):

                path_index += 1

            else: 

                animation_active = False

    screen.fill((255,255,255))

    for row in range(len(maze)):
        for col in range(len(maze[0])):

            x = col*cell_size
            y = row*cell_size

            cost = maze[row][col]

            color = colors[cost]

            if (row, col) == start:
                color = (0, 255, 0)

            elif (row, col) == goal:
                color = (255, 0, 0)

            elif (row, col) in final_path[:path_index]:
                color = (255, 255, 0)

            elif (row, col) in explored_cells[:explored_index]:
                color = (100, 150, 255)

            pygame.draw.rect(
                screen, color, (x, y, cell_size, cell_size)
            )

            pygame.draw.rect(
                screen, (100, 100, 100), (x, y, cell_size, cell_size), 1
            )

            if (row, col) == start:
                text_value = "S"

            elif (row, col) == goal:
                text_value = "G"

            elif cost == 0:
                text_value = ""

            else:
                text_value = str(cost)

            if (row, col) in explored_cells[:explored_index]:
                text_color = (0, 0, 0)

            elif (row, col) in final_path[:path_index]:
                text_color = (0, 0, 0)

            elif cost >= 6:
                text_color = (255,255,255)

            else:
                text_color = (0, 0, 0)

            text = font.render(text_value, True, text_color)

            text_rect = text.get_rect(
                center = (x + cell_size // 2, y + cell_size // 2)
            )

            screen.blit(text, text_rect)

    if warning_message:

        warning_text = warning_font.render(
            warning_message, True, (255, 255, 255)
        )

        warning_rect = warning_text.get_rect(
            center = (750 // 2, 30)
        )

        backgroung_rect = warning_rect.inflate(30, 20)

        pygame.draw.rect(
            screen, (255, 0, 0), backgroung_rect
        )

        screen.blit(warning_text, warning_rect)


    pygame.draw.rect(screen, (40, 40, 40), (0, 600, 750, 150))

    stats_font = pygame.font.SysFont(None, 25)

    stats_text = (
        f"Explored: {explored_count}  |  "
        f"Path Length: {path_length}  |  "
        f"Path Cost: {path_cost}  |  "
        f"Time: {execution_time:.6f}s"
    )

    stats_surface = stats_font.render(stats_text, True, (255, 255, 255))

    screen.blit(stats_surface, (30, 610))

    algorithm_text = font.render(
            f"Algorithm: {current_algorithm}",
            True,
            (255, 255, 255)
        )

    screen.blit(algorithm_text, (30, 645))
    
    controls_text = (
        "1- BFS   2- DFS   3- Dijkstra   4- A*  SPACE- Run   R- Reset   C- Clear"
    )

    controls_surface = stats_font.render(
        controls_text,
        True,
        (255, 255, 255)
    )

    screen.blit(controls_surface, (30, 680))

    mouseclick_text = (
        "Left Click- +1    Scroll Wheel- Start    Right Click- Goal"
    )

    mouseclick_surface = stats_font.render(
        mouseclick_text, True, (255, 255, 255)
    )

    screen.blit(mouseclick_surface, (30, 715))
    
    pygame.display.update()

pygame.quit()

