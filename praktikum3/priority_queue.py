from typing import List


class QueueItem(object):
    def __init__(self, state: str, cost: int, heuristic: int, way: List[str]) -> None:
        self.state = state
        self.cost = cost
        self.heuristic = heuristic
        self.way = way

    def __eq__(self, __o: object) -> bool:
        return self.state == __o.state


class PriorityQueue(object):
    def __init__(self) -> None:
        self.queue: List[QueueItem] = []

    def enqueue(self, item: QueueItem) -> None:
        """ Enqueue a new queue item """
        self.queue.append(item)
        self.queue.sort(key=lambda x: x.heuristic)

    def dequeue(self) -> QueueItem:
        """ Dequeues the item with the lowest cost. returns None if the queue is empty """
        if self.is_empty():
            return None
        return self.queue.pop(0)

    def is_empty(self) -> bool:
        """ Returns true if empty, else false (sorry raphael fuer den code) """
        return not self.queue
