from helpers import *

maze, dest = build_maze_sp()
adj_nodes = get_adj_nodes(get_pos_x(), get_pos_y(), maze)

quick_print(adj_nodes, maze[adj_nodes[0]])