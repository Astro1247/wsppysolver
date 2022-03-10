import hashlib
from copy import copy, deepcopy

import action as action

import solver
from solver import Solver
from threading import Thread

active_threads = []
done_moves = 0
skipped_maps = 0


def move_colors(solver, from_bottle, to_bottle):
    global done_moves
    done_moves += 1
    new_solver = Solver(solver.get_map(), solver.moves)
    #print('Moving: {} => {}'.format(solver.bottles[from_bottle].get_mapped_data(), solver.bottles[to_bottle].get_mapped_data()))
    result = new_solver.move_water(from_bottle, to_bottle)
    #print('Done moves: ', done_moves)
    return result


if __name__ == '__main__':
    print("Welcome to Water Sorting Puzzle Solver developed by Astro1247 [WIP]")  # TODO remove [WIP] tag
    print("Please, input colors or just press ENTER, when done")
    #map = [[1, 1, 1, 0], [2, 2, 2, 1], [2, 0, 0, 0], [0, 0, 0, 0]]
    map = [
        [1,2,3,4],
        [3,5,6,6],
        [7,8,9,4],
        [8,1,2,5],
        [5,8,9,7],
        [7,3,5,4],

        [3,9,6,1],
        [9,6,4,7],
        [2,8,2,1],
        [0,0,0,0],
        [0,0,0,0]
    ]
    map3 = [
        [1,2,1,2],
        [2,1,2,1],
        [0,0,0,0]
    ]
    map2 = [
        [1,2,3,4],
        [5,4,6,6],
        [7,8,1,3],
        [5,4,9,4],
        [10,7,11,7],
        [12,4,5,3],
        [11,5,2,7],

        [7,11,6,9],
        [8,9,3,7],
        [12,1,12,12],
        [1,6,11,8],
        [12,7,2,2],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]
    data = ''  # input("Enter color (or just press ENTER):")
    while data != '':
        try:
            data = int(data)
            if data not in range(-1000, 1000):
                print('Please, enter value between -1000 and 1000')
            elif len(map[-1]) < 4:
                map[-1].append(data)
            else:
                map.append([data])
            print(map[-1])
        except ValueError:
            print("Invalid input, please try again")
        data = input("Enter color (or just press ENTER):")
    init_slv = Solver(map)
    init_slv.find_actions()
    slvs = [init_slv]
    known_maps = []
    solved = []
    while len(slvs) > 0:
        new_slvs = []
        for slv in slvs:
            slv_map_hash = hashlib.sha256(str(slv.get_map()).encode('utf-8')).hexdigest()
            if slv_map_hash in known_maps:
                skipped_maps += 1
                #print(f'skipped_maps: {skipped_maps}')
                slvs.pop(slvs.index(slv))
                continue
            else:
                known_maps.append(slv_map_hash)
            slv.check_solved()
            if slv.solved:
                solved.append(slv)
                if slv in slvs:
                    slvs.pop(slvs.index(slv))
                continue
            slv.find_actions()
            dumped = list(slv.get_map())
            for action in slv.actions:
                new_slv = move_colors(Solver(list(slv.get_map()), slv.moves),
                                      action['water'].bottle.index,
                                      action['compatible'].bottle.index)
                new_slv.check_solved()
                if new_slv.solved:
                    solved.append(slv)
                    if slv in slvs:
                        slvs.pop(slvs.index(slv))
                    continue
                new_slv.find_actions()
                if len(new_slv.actions) > 0:
                    new_slvs.append(new_slv)
        slvs = new_slvs
    print(f'Found {len(solved)} solutions\n'
          f'Done {done_moves} moves\n'
          f'Learned {len(known_maps)} maps')
    for i in range(0,len(solved)):
        print(f'#{i} Solved in {solved[i].moves} moves')
    print('Job finished')
