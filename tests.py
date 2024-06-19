def plant_trees():
    ws = get_world_size()
    for i in range(ws ** 2):
        if (i % ws + i // ws) % 2 == 0:
            x, y = one_d_two_d(i)
            move_self(x, y)
            plant(Entities.Tree)
            
plant_trees()
    