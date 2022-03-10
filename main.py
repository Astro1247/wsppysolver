from copy import copy

import action as action

from solver import Solver
from threading import Thread

active_threads = []
done_moves = 0


def move_colors(solver, from_bottle, to_bottle):
    global done_moves
    done_moves += 1
    new_solver = copy(solver)#Solver(solver.get_map())
    print('Moving: {} => {}'.format(solver.bottles[from_bottle].get_mapped_data(), solver.bottles[to_bottle].get_mapped_data()))
    result = new_solver.move_water(from_bottle, to_bottle)
    #print('Done moves: ', done_moves)
    return result


if __name__ == '__main__':
    print("Welcome to Water Sorting Puzzle Solver developed by Astro1247 [WIP]")  # TODO remove [WIP] tag
    print("Please, input colors or enter empty iput when done")
    #map = [[1, 1, 1, 0], [2, 2, 2, 1], [2, 0, 0, 0], [0, 0, 0, 0]]  # [[]]
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
    solved = None
    while len(slvs) > 0 and solved is None:
        new_slvs = []
        for slv in slvs:
            slv.check_solved()
            if slv.solved:
                slvs = []
                solved = slv
                [print('SOLVED!\n') for _ in range(0,100)]
                break
            slv.find_actions()
            dumped = list(slv.get_map())
            for action in slv.actions:
                if done_moves == 214:
                    print('here')
                    slv.find_actions()
                new_slv = move_colors(Solver(list(slv.get_map())),
                                      action['water'].bottle.index,
                                      action['compatible'].bottle.index)
                new_slv.check_solved()
                if new_slv.solved:
                    slvs = []
                    solved = new_slv
                    [print('SOLVED!\n') for _ in range(0, 100)]
                    break
                new_slv.find_actions()
                if len(new_slv.actions) > 0:
                    new_slvs.append(new_slv)
        slvs = new_slvs
    print('Job finished')
