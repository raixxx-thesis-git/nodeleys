from __future__ import annotations

from nodeleys.system import secure_type
from typing import TYPE_CHECKING, Optional, Union, List
from cupy import ndarray

import operator
import cupy
import re

if TYPE_CHECKING:
  from nodeleys import Node

def complete_adic_func(l_operand: Node, r_operand: Optional[Node], 
                       operator: str, outcome: ndarray, name: str) -> Node:
  from nodeleys import Node
  from nodeleys.graph import Triplet, Duplet
  outcome_node = Node(outcome, name=name)

  if r_operand == None:
    # create a Duplet D[n](L, O; op)
    adic = Duplet(l_operand, outcome_node, operator)

    # connect D[n] with D[n-1]
    adic.set_prev(l_operand.get_adic())

    if l_operand.get_adic() != None:
      # connect D[n-1] with D[n] if D[n-1] exists
      l_operand.get_adic().set_next(adic)
  else:
    # create a Duplet T[n](L, O; op)
    adic = Triplet(l_operand, r_operand, outcome_node, operator)

    # connect T[n] with T0[n-1] and T1[n-1]
    adic.set_prev((l_operand.get_adic(), r_operand.get_adic()))

    if l_operand.adic != None:
      # connect T0[n-1] with T[n] if T0[n-1] exists
      l_operand.get_adic().set_next(adic)
    elif r_operand.adic != None:
      # connect T1[n-1] with T[n] if T1[n-1] exists
      r_operand.get_adic().set_next(adic)
  
  outcome_node.set_adic(adic)
  return outcome_node

def secure_operands(l_operand: Union[Node, float], r_operand: Union[Node, float]):
  return secure_type(l_operand), secure_type(r_operand)

def node_add(l_operand: Union[Node, float], r_operand: Union[Node, float], name: str='') -> Node:
  l_operand, r_operand = secure_operands(l_operand, r_operand)
  outcome = operator.add(l_operand.tensor, r_operand.tensor)
  return complete_adic_func(l_operand, r_operand, '+', outcome, name)

def node_sub(l_operand: Union[Node, float], r_operand: Union[Node, float], name: str='') -> Node:
  l_operand, r_operand = secure_operands(l_operand, r_operand)
  outcome = operator.sub(l_operand.tensor, r_operand.tensor)
  return complete_adic_func(l_operand, r_operand, '-', outcome, name)

def node_mul(l_operand: Union[Node, float], r_operand: Union[Node, float], name: str='') -> Node:
  l_operand, r_operand = secure_operands(l_operand, r_operand)
  outcome = operator.mul(l_operand.tensor, r_operand.tensor)
  return complete_adic_func(l_operand, r_operand, '*', outcome, name)

def node_div(l_operand: Union[Node, float], r_operand: Union[Node, float], name: str='') -> Node:
  l_operand, r_operand = secure_operands(l_operand, r_operand)
  outcome = operator.truediv(l_operand.tensor, r_operand.tensor)
  return complete_adic_func(l_operand, r_operand, '/', outcome, name)

def node_matmul(l_operand: Union[Node, float], r_operand: Union[Node, float], name: str='') -> Node:
  l_operand, r_operand = secure_operands(l_operand, r_operand)
  outcome = l_operand.tensor @ r_operand. tensor
  return complete_adic_func(l_operand, r_operand, '@', outcome, name)

def node_pow(l_operand: Union[Node, float], r_operand: Union[Node, float], name: str='') -> Node:
  l_operand, r_operand = secure_operands(l_operand, r_operand)
  outcome = l_operand.tensor ** r_operand.tensor
  return complete_adic_func(l_operand, r_operand, '**', outcome, name)

def node_redsum(l_operand: Union[Node, float], axis: int, name: str='') -> Node:
  l_operand = secure_type(l_operand)
  outcome = cupy.sum(l_operand.tensor, axis=axis, keepdims=True)
  return complete_adic_func(l_operand, None, 'redsum', outcome, name)

def node_ln(l_operand: Union[Node, float], name: str='') -> Node:
  l_operand = secure_type(l_operand)
  outcome = cupy.log(l_operand.tensor)
  return complete_adic_func(l_operand, None, 'ln', outcome, name)

