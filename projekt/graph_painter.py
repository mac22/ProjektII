#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pydot

class Graph_painter:

  def paint(self, chains, filename):
    graph = pydot.Dot(graph_type='graph')
    for chain in chains:
      for flow in chain.flows:
        edge = pydot.Edge(chain.name, flow.name)
        graph.add_edge(edge)
    graph.write_png(filename)

