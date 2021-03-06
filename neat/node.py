import functools
from itertools import groupby
from typing import Callable, Union, List, TYPE_CHECKING
import copy
from enum import Enum

def passthrough(x):
    return x

@functools.total_ordering
class NodeType(Enum):
    INPUT = 1
    BIAS = 2
    HIDDEN = 3
    OUTPUT = 4

    def __gt__(self, other):
        return self.value > other.value


class Node(object):
    def __init__(self, id: int, type: NodeType,
                 activation: Callable[[float], float] = passthrough,
                 value: float = 0.0,
                 depth: float = 0.0):
        self.id = id
        self.type = type
        self.activation = activation
        self.value = value
        self.depth = depth
        self.visited = False

        if TYPE_CHECKING:
            from .connection import Connection
        self.inputs: List[Connection] = []

    def __hash__(self):
        return hash(str(self.id))

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.id == other.id
        else:
            raise ValueError(f'Value type should be Node, got {type(other)}')

    def __add__(self, other: Union['Node', int]) -> int:
        if isinstance(other, Node):
            return self.id + other.id
        elif isinstance(other, int):
            return self.id + other
        else:
            raise ValueError(f'Value type should be Node or int, got {type(other)}')

    def copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        return f'{self.id}:{self.type}'

    def __repr__(self):
        return str(self.id)

def group_nodes_by_type(nodes: List[Node]) -> List[List[Node]]:
    sorted_nodes = sorted(nodes, key = lambda x: x.type)
    grouped_nodes = [list(it) for k, it in groupby(sorted_nodes, lambda x: x.type)]
    return grouped_nodes

def group_nodes_by_depth(nodes: List[Node]) -> List[List[Node]]:
    sorted_nodes = sorted(nodes, key = lambda x: x.depth)
    grouped_nodes = [list(it) for k, it in groupby(sorted_nodes, lambda x: x.depth)]
    return grouped_nodes
