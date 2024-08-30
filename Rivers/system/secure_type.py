from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from Rivers import Node

def secure_type(node: Node | float) -> Node:
  from Rivers import Node
  if type(node) == float:
    node = Node(node, name=str(node), is_constant=True)
  return node
  