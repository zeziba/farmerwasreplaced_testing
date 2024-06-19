def one_d_two_d(pos):
    world_size = get_world_size()
    return pos % world_size, pos // world_size


def two_d_one_d(x, y):
    world_size = get_world_size()
    return x + y * world_size


def timeit(func, args=None):
    start = get_time()

    if args:
        func(args)
    else:
        func()

    t_time = get_time() - start

    quick_print("Time Taken: ", t_time)

    return t_time


def move_self(tx, ty):
    ws = get_world_size()
    dx, dy = get_pos_x() - tx, get_pos_y() - ty

    ns = (None, South, North)
    we = (None, West, East)

    def inner_move(delta, move_dir):
        if abs(delta) > ws // 2:
            delta -= (delta / abs(delta)) * ws
        for i in range(0, delta, delta / abs(delta)):
            move(move_dir[delta / abs(delta)])

    inner_move(dx, we)
    inner_move(dy, ns)

    return get_pos_x(), get_pos_y()


def plant_crop(crop, replant=False):
    if get_ground_type() != Grounds.Soil:
        till()

    if replant or get_entity_type() != crop:
        harvest()
        return plant(crop)

    return False


def plant_cacti(x, y, replant=False):
    move_self(x, y)

    if num_items(Items.Cactus_Seed) > 0 or trade(Items.Cactus_Seed):
        if plant_crop(Entities.Cactus, replant):
            val = measure()

            return val

    return False


def plant_maze(x, y):
    move_self(x, y)

    if plant_crop(Entities.Bush, True):
        while get_entity_type() != Entities.Hedge:
            if num_items(Items.Fertilizer) > 0 or trade(Items.Fertilizer, 10):
                use_item(Items.Fertilizer)

        return True

    return False


def build_maze():
    ws = get_world_size()

    node_network = {}
    for i in range(ws**2):
        x, y = one_d_two_d(i)
        create_maze_node(x, y, node_network)

    return node_network


def build_maze_sp():
    ws = get_world_size()
    node_network = build_maze()
    visited = []
    dest = None

    while len(visited) < ws**2:
        cx, cy = get_pos_x(), get_pos_y()
        if get_entity_type() == Entities.Treasure:
            dest = (cx, cy)
        if (cx, cy) not in visited:
            visited.append((cx, cy))
        least_dir = get_least_dir(cx, cy, node_network)
        if move(least_dir):
            add_maze_nodes(cx, cy, least_dir, node_network)
            continue
        else:
            set_maze_walls(cx, cy, least_dir, node_network)

    return node_network, dest


def get_opposite_dir(dir_):
    ndirs = {North: South, South: North, East: West, West: East}

    return ndirs[dir_]


def get_dir_val(dir_):
    rvals = {North: (0, 1), South: (0, -1), East: (1, 0), West: (-1, 0)}

    return rvals[dir_]


def get_val_dir(dir_):
    rvals = {(0, 1): North, (0, -1): South, (1, 0): East, (-1, 0): West}

    return rvals[dir_]


def get_opposite_val(dir_):
    rvals = {North: (0, -1), South: (0, 1), East: (-1, 0), West: (1, 0)}

    return rvals[dir_]


def create_maze_node(x, y, node_network):
    node_network[(x, y)] = {North: 0, South: 0, East: 0, West: 0}


def add_maze_node(x, y, dir_, node_network):
    if (x, y) not in node_network:
        return
    if dir_ not in node_network[(x, y)]:
        return
    node_network[(x, y)][dir_] += 1


def add_maze_nodes(x, y, dir_, node_network):
    ox, oy = get_dir_val(dir_)
    odir = get_opposite_dir(dir_)

    add_maze_node(x, y, dir_, node_network)
    add_maze_node(x + ox, y + oy, odir, node_network)


def set_maze_wall(x, y, dir_, node_network):
    ws = get_world_size()

    if x >= 0 and x < ws and y >= 0 and y < ws:
        if dir_ in node_network[(x, y)]:
            node_network[(x, y)].pop(dir_)


def set_maze_walls(x, y, dir_, node_network):
    x2, y2 = get_dir_val(dir_)
    odir = get_opposite_dir(dir_)

    set_maze_wall(x, y, dir_, node_network)
    set_maze_wall(x + x2, y + y2, odir, node_network)


def get_least_dir(x, y, node_network):
    least_dir = None
    least_val = 100000

    for dir in node_network[(x, y)]:
        if node_network[(x, y)][dir] < least_val:
            least_val = node_network[(x, y)][dir]
            least_dir = dir

    return least_dir


def get_adj_nodes(x, y, node_network):
    adj_nodes = []
    if (x, y) in node_network:
        for dir in node_network[(x, y)]:
            if node_network[(x, y)][dir] > 0:
                dx, dy = get_dir_val(dir)
                adj_nodes.append((x + dx, y + dy))

    return adj_nodes


def build_graph(node_network):
    graph = {}

    # Build Graph
    for i in range(get_world_size() ** 2):
        x, y = one_d_two_d(i)
        graph[(x, y)] = set()

    # Build Connections
    for node in graph:
        adj_nodes = get_adj_nodes(node[0], node[1], node_network)
        for adj_node in adj_nodes:
            graph[node].add(adj_node)

    return graph


def fertilize_treasure(buy_amount=100):
    while get_entity_type() == Entities.Treasure:
        if num_items(Items.Fertilizer) > 0 or trade(Items.Fertilizer, buy_amount):
            use_item(Items.Fertilizer)
        else:
            return False

    return True
