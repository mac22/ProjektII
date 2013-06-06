#!/usr/bin/python
# -*- coding: UTF-8 -*-
from chain import Chain
from flow import Flow
from data_writer import Data_writer
from graph_painter import Graph_painter
from config_reader import Config_reader

def main():
  dw = Data_writer()
  cr = Config_reader()
  cc = cr.read()
  dw.reset(cc.filename)
  (chains, flows) = prepare(cc)
  t = 0
  while t < cc.simT:
    updateConnectionsWindows(chains, t)
    updateLenghtOfQueues(chains, t)
    saveData(chains, flows, cc, t, dw)
    t = round(t + cc.h, cc.roundDegree)
  gp = Graph_painter()
  gp.paint(chains, cc.graphFilename)
  dw.writePlotFile(cc.filename, cc.plotFilename)

def prepare(cc):
  chains = set()
  for i in range(cc.k):
    chain = Chain(i)
    chain.updateParams(cc.data)
    chains.add(chain)
  for j in range(cc.n):
    flow = Flow(j)
    flow.updateParams(cc.data)
    flow.connectWithChain(chains)
  flows = set()
  for chain in chains:
    for flow in chain.flows:
      flows.add(flow)
    
  return (chains, flows)

def updateConnectionsWindows(chains, t):
  for chain in chains:
    for flow in chain.flows:
      flow.e_dW(t)

def updateLenghtOfQueues(chains, t):
  for chain in chains:
    chain.e_dQ(t)

def saveData(chains, flows, cc, t, dw):
  for chain in chains:
    if 'q' in chain.printVal:
      dw.collect(chain.name + ' q', chain.qHist.get(t))
    x = chain.x(t)
    if 'x' in chain.printVal:
      dw.collect(chain.name + ' x', x)
    if 'p' in chain.printVal:
      dw.collect(chain.name + ' p', chain.p(x))
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
