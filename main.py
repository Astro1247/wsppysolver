from solver import Solver
from threading import Thread

if __name__ == '__main__':
    print("Welcome to Water Sorting Puzzle Solver developed by Astro1247 [WIP]")  # TODO remove [WIP] tag
    print("Please, input colors or enter empty iput when done")
    map = [[1,1,1,0],[2,2,2,1],[2,0,0,0]]#[[]]
    data = ''#input("Enter color (or just press ENTER):")
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
    print('Got:', slv)
