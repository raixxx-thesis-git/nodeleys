from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from nodeleys.graph import Duplet, Triplet, Virtual

class DynamicBackpropSystem():
  def __init__(self): pass
  
  def propagate(self: Virtual):
    idx = 0
    for virtual_graph, conditions in (self.virtual_graphs, self.conditions):
      '''
      This is a subsystem routine. We do not pass the inherited backprop states to
      simulate back propagation routines of virtual graphs (dynamic).
      Since the graphs are virtual, we do not record the back propagation traces.
      '''
      _, _ = virtual_graph.get_adic().propagate([], [], [], interrupts=self.vars, 
                                                is_virtually=True, idx=idx)
      
      '''
      All of the interrupt adics are updated.
      '''
      idx += 1
  pass