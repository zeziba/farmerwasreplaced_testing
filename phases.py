from helpers import *


def plant_cacti_field(max_pos):
    board = []
    for i in range(max_pos):
        x, y = one_d_two_d(i)
        if not plant_cacti(x, y):
            return False
        board.append(measure())
    return board


def plant_cacti_field_adv(max_pos, max_cal=2, min_val=2):
    board = []
    for i in range(max_pos):
        x, y = one_d_two_d(i)
        val = plant_cacti(x, y, True)
        board.append(val)
    return board


def gnome_basic(max_pos, cacti):
    move_self(0, 0)  # Start at the root node

    pos = 0
    board = cacti

    while pos < max_pos:
        x, y = one_d_two_d(pos)
        move_self(x, y)

        if x == 0 or board[pos] >= board[pos - 1]:
            pos += 1
        else:
            board[pos], board[pos - 1] = board[pos - 1], board[pos]
            swap(West)
            pos -= 1


def advanced_gnome_sort(cacti):
    ws = get_world_size()

    gnome_basic(ws**2, cacti)

    move_self(0, 0)  # Start at the root node

    pos = 0
    board = cacti

    while pos < ws**2:
        x, y = one_d_two_d(pos)
        move_self(x, y)

        if y > 0 and y != ws:
            pos_2 = two_d_one_d(x, y - 1)

            if board[pos_2] > board[pos]:
                swap(South)
                board[pos_2], board[pos] = board[pos], board[pos_2]
                pos = pos_2
                continue

        y += 1
        if y >= ws:
            y = 0
            x += 1
            if x >= ws:
                break
        pos = two_d_one_d(x, y)


def final_gnome_sort(cacti):
    # Reset drone to 0,0
    move_self(0, 0)
    ws = get_world_size()
    cacti_val = cacti

    # Sort all cacti using moddifed gnome sort
    pos = 0
    while pos < ws**2:
        # Swap pos to south
        x, y = one_d_two_d(pos)

        if y > 0 and y != ws:
            pos_2 = two_d_one_d(x, y - 1)
            if cacti_val[pos_2] > cacti_val[pos]:
                move_self(x, y)
                swap(South)
                cacti_val[pos_2], cacti_val[pos] = cacti_val[pos], cacti_val[pos_2]
                pos = pos_2
                continue
        # Swap pos to left
        if x == 0 or cacti_val[pos] >= cacti_val[pos - 1]:
            pos += 1
        else:
            move_self(x, y)
            cacti_val[pos], cacti_val[pos - 1] = cacti_val[pos - 1], cacti_val[pos]
            swap(West)
            pos -= 1


def cacti_main():
    start_time = get_time()

    clear()

    # cacti_board = plant_cacti_field(100)
    cacti_board = plant_cacti_field_adv(100)

    final_gnome_sort(cacti_board)

    pre_harvest = num_items(Items.Cactus)

    harvest()

    quick_print(num_items(Items.Cactus) - pre_harvest)
    quick_print(get_time() - start_time)


def maze_solve_single(node_network):
    create_maze_node(get_pos_x(), get_pos_y(), node_network)  # Create Root Node

    while get_entity_type() != Entities.Treasure:
        cx, cy = get_pos_x(), get_pos_y()
        least_dir = get_least_dir(cx, cy, node_network)
        if move(least_dir):
            add_maze_node(cx, cy, least_dir, node_network)
            continue
        else:
            set_maze_wall(cx, cy, least_dir, node_network)

    return node_network, measure()


def maze_solve_bfs(target, graph=None):
    visited = {}
    queue = []

    if target not in graph:
        return False

    node = (get_pos_x(), get_pos_y())
    visited[node] = None
    queue.append(node)

    while queue:
        cur_node = queue.pop(0)
        if cur_node == target:
            path = []
            while cur_node:
                path.append(cur_node)
                cur_node = visited[cur_node]
            return path[::-1]

        if cur_node not in graph:
            return []
        for adj_node in graph[cur_node]:
            if adj_node not in visited:
                visited[adj_node] = cur_node
                queue.append(adj_node)
    return []


def walk_bfs(path_):
    cnode = path_.pop(0)
    while len(path_) > 0:
        cnode = path_.pop(0)
        x, y = cnode
        fx, fy = move_self(x, y)
        if fx != x or fy != y:
            path_.insert(0, cnode)
    return True


def get_gold(runs=300):
    plant_maze(get_pos_x(), get_pos_y())
    path = []
    for i in range(runs - 2):
        if i % 100 == 0:
            maze, dest = build_maze_sp()
        path = maze_solve_bfs(dest, build_graph(maze))
        if not walk_bfs(path):
            quick_print("Failed")
            return
        dest = measure()
        if dest == None:
            return
        if not fertilize_treasure():
            quick_print("Run Failed")
            return False

        quick_print(i / runs * 100, "% Complete")
    path = maze_solve_bfs(dest, build_graph(maze))
    walk_bfs(path)

    harvest()
