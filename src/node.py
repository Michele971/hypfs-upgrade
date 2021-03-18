from src.hypercube import Hypercube
from src.utils import *


class Node:
    def __init__(self, int_id):
        self.id = create_binary_id(int_id)
        self.hypercube = Hypercube()
        self.objects = []

    def insert(self, keyword, obj):
        bit_keyword = create_binary_id(keyword)
        if bit_keyword == self.id:
            if obj not in self.objects:
                self.objects.append(obj)
        else:
            best_path = self.hypercube.get_shortest_path(self.id, bit_keyword)
            neighbor = best_path[1]
            request(neighbor, INSERT, {'keyword': str(keyword), 'obj': obj})

    def remove(self, keyword, obj):
        bit_keyword = create_binary_id(keyword)
        if bit_keyword == self.id:
            if obj in self.objects:
                self.objects.remove(obj)
        else:
            best_path = self.hypercube.get_shortest_path(self.id, bit_keyword)
            neighbor = best_path[1]
            request(neighbor, REMOVE, {'keyword': str(keyword), 'obj': obj})

    def pin_search(self, keyword, threshold=-1):
        bit_keyword = create_binary_id(keyword)
        if bit_keyword == self.id:
            if 0 < threshold < len(self.objects):
                return self.objects[:threshold]
            else:
                return self.objects
        else:
            best_path = self.hypercube.get_shortest_path(self.id, bit_keyword)
            neighbor = best_path[1]
            return request(neighbor, PIN_SEARCH, {'keyword': str(keyword), 'threshold': threshold})

    def superset_search(self, keyword, threshold):
        results = []
        bit_keyword = create_binary_id(keyword)
        superset = self.hypercube.breadth_first_search(bit_keyword)
        for target in superset:
            if threshold <= 0:
                break
            if self.id == target:
                results.extend(self.objects)
            else:
                best_path = self.hypercube.get_shortest_path(self.id, target)
                neighbor = best_path[1]
                result = list(
                    request(neighbor, PIN_SEARCH, {'keyword': int(target, 2), 'threshold': threshold}).text.split(','))
                threshold -= len(result)
                results.extend(result)
        return results
