class Water(object):
    def __init__(self, color, size, pos_from, bottle):
        if not isinstance(color, int):
            raise TypeError("Color must be an integer")
        elif not isinstance(size, int):
            raise TypeError("Size must be an integer")
        elif size not in range(1, 5):
            raise ValueError("Size must be in range 1-4, inclusive")
        elif pos_from not in range(1, 5):
            raise ValueError("Pos_from must be in range 1-4, inclusive")
        elif not isinstance(bottle, Bottle):
            raise TypeError('Bottle must be Bottle class instance')
        self.size = size
        self.color = color
        self.bottle_position = {
            'from': pos_from,
            'to': pos_from + size - 1
        }
        self.bottle = bottle
        if self.bottle_position['to'] > 4:
            raise OverflowError("Bottle position must be in range 1-4")

    def increase(self, count):
        if self.bottle_position['to'] == 4:
            raise OverflowError("Water is already at bottle top")
        elif self.bottle_position['to'] + count > 4 or self.size + count > 4:
            raise OverflowError("Water position/size cannot overlap 4")
        else:
            self.size += count
            self.bottle_position['to'] = self.bottle_position['from'] + self.size - 1
        return self.size


class Bottle(object):
    def __init__(self, data, solver):
        if not isinstance(data, list):
            raise TypeError("data must be a list")
        elif len(data) != 4:
            raise ValueError("data must have 4 values")
        elif not all(isinstance(elem, int) for elem in data):
            raise ValueError("data must contain elements of type int")
        self.data = []
        self.solved = False
        self.index = len(solver.bottles)
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
            self.data.append(Water(elem['color'], elem['size'], self.get_fullness() + 1, self))
        self.check_solved()

    def check_solved(self):
        if (len(self.data) == 1 and self.data[0].size == 4) or len(self.data) == 0:
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
            return Water(0, 1, 1, self)

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
        elif len(self.data) == 0 or self.data[-1].color != color.color:
            color.bottle = self
            self.data.append(color)
            self.check_solved()
        else:
            self.data[-1].size += color.size
            self.data[-1].bottle_position['to'] += color.size
            self.check_solved()
            del color

    def get_mapped_data(self):
        mapped = []
        if len(self.data) == 0:
            return [0,0,0,0]
        for color in self.data:
            for i in range(0,color.size):
                mapped.append(color.color)
        for i in range(len(mapped),4):
            mapped.append(0)
        return mapped


class Solver(object):
    def __init__(self, map):
        # validating map Expected to be like [[1,1,2,1], [2,2,1,2], [3,5,3,0], [0,0,0,0]], starting from bottle bottom
        # where 0 = empty
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
        self.map = map
        self.bottles = []
        self.solved = False
        for data in map:
            x = Bottle(data, self)
            self.bottles.append(x)
        if not self.check_solved():
            self.actions = self.find_actions()
        else:
            self.actions = []

    def check_solved(self):
        for bottle in self.bottles:
            bottle.check_solved()
        self.solved = all(bottle.solved for bottle in self.bottles)
        return self.solved

    def find_actions(self):
        self.check_solved()
        if self.solved:
            return []
        #bottles_tops = [bottle.get_top_data() for bottle in self.bottles]
        #from copy import copy
        #dumped = copy(bottles_tops)
        possible_actions = []
        for bottle in self.bottles:
            top = bottle.get_top_data()
            #if [bottle.get_mapped_data() for bottle in self.bottles] != [bottle.bottle.get_mapped_data() for bottle in dumped]:
            if top.color != self.bottles[top.bottle.index].get_top_data().color:
                print("ACHTUNG!!!") #TODO change water bottle after moving
            if top.color == 0:
                continue
            #compatibles = list(filter(
            #    lambda target: (target.color == 0 or target.color == top.color) and target.bottle_position['to'] + top.size <= 4,
            #    bottles_tops))
            compatibles = []
            for target_bottle in self.bottles:
                target = target_bottle.get_top_data()
                if top.bottle == target.bottle:
                    continue
                if (target.color == 0 or target.color == top.color) and target.bottle_position['to'] + top.size <= 4:
                    compatibles.append(target)
            if len(compatibles) > 0:
                for compatible in compatibles:
                    if compatible.bottle != top.bottle \
                            and top.size != 4 \
                            and not (compatible.color == 0 and len(top.bottle.data) == 1):
                        possible_actions.append({'compatible': compatible, 'water': top})
        self.actions = possible_actions
        #[print('Possible action found. {} ({}) bottle {} into {} ({}) bottle {}'.format(action['water'].color,
        #                                                                                action['water'].size,
        #                                                                                action['water'].bottle,
        #                                                                                action['compatible'].color,
        #                                                                                action['compatible'].size,
        #                                                                                action['compatible'].bottle))
        # for action in self.actions]
        return possible_actions

    def move_water(self, from_bottle, to_bottle):
        #from_bottle = source_bottle.index
        #to_bottle = target_bottle.index
        source_bottle = self.bottles[from_bottle]
        target_bottle = self.bottles[to_bottle]
        if from_bottle not in range(0,len(self.bottles)):
            raise IndexError('Index "from_bottle" is out of range')
        elif to_bottle not in range(0,len(self.bottles)):
            raise IndexError('Index "to_bottle" is out of range')
        elif source_bottle.get_top_data().color == 0:
            raise ValueError('Cannot move water from empty bottle')
        elif source_bottle.get_top_data().color != target_bottle.get_top_data().color \
                and target_bottle.get_top_data().color != 0:
            raise ValueError(f'Colors in bottles are incompatible {source_bottle.get_mapped_data()} into {target_bottle.get_mapped_data()}')
        elif source_bottle.get_top_data().size + target_bottle.get_top_data().bottle_position['to'] > 4:
            raise OverflowError("Target bottle will be overflowed")
        target_water = target_bottle.get_top_data()
        if target_water.color == 0:
            target_bottle.push_color(source_bottle.pull_top_color())
        else:
            target_water.increase(source_bottle.pull_top_color().size)
        return self

    def get_map(self):
        self.map = [bottle.get_mapped_data() for bottle in self.bottles]
        return self.map
