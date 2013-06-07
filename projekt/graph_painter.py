#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pydot

class Graph_painter:

  def paint(self, nodes, filename):
    graph = pydot.Dot(graph_type='graph')
    for node in nodes:
      for flow in node.flows:
        edge = pydot.Edge(node.name, flow.name)
        graph.add_edge(edge)
    graph.write_png(filename)

