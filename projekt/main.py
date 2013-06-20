#!/usr/bin/python
# -*- coding: UTF-8 -*-
from node import Node
from flow import Flow
from data_writer import Data_writer
from graph_painter import Graph_painter
from config_reader import Config_reader

def main():
  dw = Data_writer()
  cr = Config_reader()
  cc = cr.read()
  dw.reset(cc.filename)
  (nodes, flows) = prepare(cc)
  t = 0
  while t < cc.simT:
    updateConnectionsWindows(flows, t)
    updateLenghtOfQueues(nodes, t)
    saveData(nodes, flows, cc, t, dw)
    t = round(t + cc.h, cc.roundDegree)
  gp = Graph_painter()
  gp.paint(nodes, cc.graphFilename)
  dw.writePlotFile(cc.filename, cc.plotFilename)

def prepare(cc):
  nodes = set()
  for i in range(cc.k):
    node = Node(i)
    node.updateParams(cc.data)
    nodes.add(node)
  for j in range(cc.n):
    flow = Flow(j)
    flow.updateParams(cc.data)
    flow.connectWithNode(nodes)
  flows = set()
  for node in nodes:
    for flow in node.flows:
      flows.add(flow)
    
  return (nodes, flows)

def updateConnectionsWindows(flows, t):
  for flow in flows:
    flow.e_dW(t)

def updateLenghtOfQueues(nodes, t):
  for node in nodes:
    node.e_dQ(t)

def saveData(nodes, flows, cc, t, dw):
  dw.collect('step', t)
  for node in nodes:
    if 'q' in node.printVal:
      dw.collect(node.name + ' q', node.qHist.get(t))
    x = node.x(t)
    if 'x' in node.printVal:
      dw.collect(node.name + ' x', x)
    if 'p' in node.printVal:
      dw.collect(node.name + ' p', node.p(x))
  for flow in flows:
    if 't' in flow.printVal:
      dw.collect(flow.name + ' t', flow.W(t)/flow.R(t))
    if 'w' in flow.printVal:
      dw.collect(flow.name + ' w', flow.W(t))
    if 'r' in flow.printVal:
      dw.collect(flow.name + ' r', flow.R(t))
  dw.write(cc.filename)

if __name__ == '__main__':
  main()
