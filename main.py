from copy import copy

import action as action

from solver import Solver
from threading import Thread

active_threads = []
done_moves = 0

def move_colors(solver, from_bottle, to_bottle):
    global done_moves
    done_moves += 1
    new_solver = Solver(solver.get_map())
    result = new_solver.move_water(from_bottle, to_bottle)
    #print('Done moves: ', done_moves)
    return result


def find_solutions(initial_solvers):
    solvers = []
    solved = None
    for s in initial_solvers:
        if solved is None:
            s.find_actions()
            for action in s.actions:
                print(f'Found {len(s.actions)} actions')
                try:
                    new_solver = (move_colors(s, action['water'].bottle.index, action['compatible'].bottle.index))
                except Exception as e:
                    continue
                new_solver.check_solved()
                new_solver.find_actions()
                if new_solver.solved:
                    solved = new_solver
                    print('SOLVED! {}'.format(new_solver.get_map()))
                    return new_solver
                elif len(new_solver.actions) > 0:
                    solvers.append(new_solver)
                else:
                    print('No actions in {}'.format(new_solver.get_map()))
    if len(solvers) > 0:
        return solvers
    else:
        print('No more actions.')
        return None



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
    slvs = [Solver(map)]
    slvs = find_solutions(slvs)
    while slvs is not None:
        slvs = find_solutions(slvs)
    print('Job finished')
