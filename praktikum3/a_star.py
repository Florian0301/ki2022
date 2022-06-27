from copy import copy
from sys import path
from json import load
from queue import Queue
from typing import Dict
from priority_queue import PriorityQueue, QueueItem


class AStar(object):
    """ Zur Berechnung des kuerzesten Weges zwischen zwei Staedten """

    def __init__(self) -> None:
        """ Setzt den Graph und die Kosten fuer den kuerzesten Weg """
        with open(path[0] + "/graph.json", "r") as file:
            self.graph: Dict[str, Dict[str, int]] = load(file)
        self.start = self.ziel = ""
        self.min_path = min(
            [min(x) for x in [list(x.values()) for x in self.graph.values()]])

    def is_valid_city(self, city: str) -> bool:
        """ Testet, ob die eigegebene City eine valide ist """
        return city in self.graph.keys()

    def is_goal(self, city: str) -> bool:
        """ Testet, ob das Ziel erreicht wurde """
        return city == self.ziel

    def actions(self, city: str):
        """ Liefert alle Actions """
        return list(self.graph.get(city).keys())

    def result(self, node: QueueItem, new_city: str) -> QueueItem:
        """ Uebergangsfunktion von Node zur neuen City """
        if self.min_path == 0:
            new_heuristic = self.graph.get(
                node.state).get(new_city) + node.cost
        else:
            new_heuristic = self.graph.get(node.state).get(
                new_city) + self.min_path * self.shortest_path(new_city) + node.cost
        new_cost = node.cost + self.graph.get(node.state).get(new_city)
        new_way = copy(node.way)
        new_way.append(new_city)

        return QueueItem(new_city, new_cost, new_heuristic, new_way)

    def shortest_path(self, city: str) -> int:
        """ Bestimmt den kuerzesten Weg zwischen City und der Zielcity """
        explored = set()
        frontier = Queue()

        last_child = city
        counter = 0

        explored.add(city)

        while True:
            if self.is_goal(city):
                return counter

            childs = [x for x in self.actions(city) if not x in explored]
            if len(childs) != 0:
                last_child_buf = childs[-1]
            if city == last_child:
                counter = counter + 1
                if len(childs) == 0:
                    last_child = last_child_buf
                else:
                    last_child = childs[-1]

            for nodes in childs:
                frontier.put(nodes)
                explored.add(nodes)

            if frontier.empty():
                return None

            city = frontier.get()

    def astar(self) -> QueueItem:
        """ Berechnet den kuerzesten Weg zwischen City1 und City2 """
        node = QueueItem(self.start, 0, 0, [self.start])
        frontier = PriorityQueue()
        frontier.enqueue(node)
        explored = set()

        while True:
            if frontier.is_empty():
                return None

            node = frontier.dequeue()
            if(self.is_goal(node.state)):
                return node
            explored.add(node.state)

            for action in self.actions(node.state):
                child = self.result(node, action)
                if child.state not in explored or child not in frontier.queue:
                    frontier.enqueue(child)
                elif child in frontier.queue and child.cost < next(x.cost for x in frontier.queue if x.state == child.state):
                    frontier.queue.remove(child)
                    frontier.enqueue(child)

    def run(self) -> None:
        """ Konsoleneingabe zum Testen des Algorithmus """
        try:
            while True:
                print(f"Moegliche Ziele: {list(self.graph.keys())}")
                self.start = self.ziel = ""
                while not self.is_valid_city(self.start):
                    self.start = input("Startpunkt: ")
                while not self.is_valid_city(self.ziel):
                    self.ziel = input("Zielpunkt:  ")

                res = self.astar()
                print(
                    f"Von {self.start} nach {self.ziel} kostet mindestens {res.cost}!")
                print(f"Die Strecke ist: {' -> '.join(res.way)}\n")

        except KeyboardInterrupt:
            print("\nOk tschuess!\n")


if __name__ == "__main__":
    astar = AStar()
    astar.run()
