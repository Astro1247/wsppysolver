from copy import copy

import action as action

from solver import Solver
from threading import Thread

active_threads = []
done_moves = 0


def move_colors(solver, from_bottle, to_bottle):
    global done_moves
    done_moves += 1
    result = solver.move_water(from_bottle, to_bottle)
    print('Done moves: ', done_moves)
    return result


def find_solutions_thread(solver):
    global active_threads
    solver.check_solved()
    if solver.solved:
        print('SOLVED! ', solver.get_map())
    if len(solver.actions) > 0:
        for action in solver.actions:
            result = move_colors(Solver(solver.get_map()), action['water'].bottle.index, action['compatible'].bottle.index)
            result.find_actions()
            thread = Thread(target=find_solutions_thread, args=(result,))
            thread.start()
            active_threads.append(thread)
    else:
        print('Thread stopped! No solutions in', solver.get_map())


if __name__ == '__main__':
    print("Welcome to Water Sorting Puzzle Solver developed by Astro1247 [WIP]")  # TODO remove [WIP] tag
    print("Please, input colors or enter empty iput when done")
    map = [[1, 1, 1, 0], [2, 2, 2, 1], [2, 0, 0, 0], [0, 0, 0, 0]]  # [[]]
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
    slv = Solver(map)
    find_solutions_thread(slv)
    for thread in active_threads:
        thread.join()
    print('Job finished')
