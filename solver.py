class Water(object):
    color = None
    size = 1
    bottle_position = {
        'from': None,
        'to': None
    }

    def __init__(self, color, size, pos_from):
        if not isinstance(color, int):
            raise TypeError("Color must be an integer")
        elif not isinstance(size, int):
            raise TypeError("Size must be an integer")
        elif size not in range(1,5):
            raise ValueError("Size must be in range 1-4, inclusive")
        elif pos_from not in range(1,5):
            raise ValueError("Pos_from must be in range 1-4, inclusive")
        self.size = size
        self.color = color
        self.bottle_position['from'] = pos_from
        self.bottle_position['to'] = pos_from+size-1

class Bottle(object):
    data = []
    solved = False
    index = None

    def __init__(self, data):
        if not isinstance(data, list):
            raise TypeError("data must be a list")
        elif len(data) != 4:
            raise ValueError("data must have 4 values")
        elif not all(isinstance(elem, int) for elem in data):
            raise ValueError("data must contain elements of type int")
        #self.data = list(filter(lambda x: x != 0, data))
        data = list(filter(lambda x: x != 0, data))
        groupped_data = []
        for elem in data:
            if len(groupped_data) == 0:
                groupped_data.append({'color': elem, 'size': 1})
            else:
                if groupped_data[-1]['color'] == elem:
                    groupped_data[-1]['size'] += 1
                else:
                    groupped_data.append({'color': elem, 'size': 1})
        for elem in groupped_data:
            self.data.append(Water(elem['color'], elem['size'], self.get_fullness()+1))
        self.check_solved()

    def check_solved(self):
        if len(set(self.data)) == 1 and len(self.data) == 4:
            self.solved = True
        return self.solved

    def get_fullness(self):
        if len(self.data) > 0:
            return sum([elem.size for elem in self.data])
        else:
            return 0

    def get_top_data(self):
        if self.get_fullness() > 0:
            return self.data[-1]
        else:
            return None

    def pull_top_color(self):
        if self.solved:
            raise PermissionError("Cannot pull from solved bottle")
        elif self.get_fullness() > 0:
            return self.data.pop(-1)
        else:
            raise IndexError("Cannot pull top color from empty bottle")

    def push_color(self, color):
        if len(self.data) > 4:
            raise OverflowError("Bottle has too many elements {}".format(len(self.data)))
        elif len(self.data) == 4:
            raise OverflowError("Bottle is already full")
        else:
            self.data.append(color)
            self.check_solved()


class Solver(object):
    bottles = []
    solved = False
    finished = False

    def __init__(self, map):
        # validating map Expected to be like [[1,1,2,1], [2,2,1,2], [3,5,3,9], [0,0,0,0]], starting from bottle bottom
        if not isinstance(map, list):
            raise TypeError("map must be a list")
        elif len(map) < 1:
            raise ValueError("map cannot be empty")
        else:
            if not all(isinstance(bottle, list) for bottle in map):
                raise TypeError("Map elements must be lists")
            elif not all(all(isinstance(elem, int) for elem in bottle) for bottle in map):
                raise TypeError("Bottle elements must be integers")
            elif any(len(bottle) != 4 for bottle in map):
                raise TypeError("Bottle must contain 4 elements")
        for data in map:
            self.bottles.append(Bottle(data))
        #self.bottles = [Bottle(data) for data in map]
        if not self.check_solved():
            self.find_actions()

    def check_solved(self):
        self.solved = all(bottle.solved for bottle in self.bottles)
        return self.solved

    def find_actions(self):
        bottles_tops = [bottle.get_top_data() for bottle in self.bottles]
        return bottles_tops
