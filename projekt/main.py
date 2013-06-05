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
  chains = prepare(cc)
  t = 0
  while t < cc.simT:
    updateConnectionsWindows(chains, t)
    updateLenghtOfQueues(chains, t)
    saveData(chains, cc, t, dw)
    t = round(t + cc.h, cc.roundDegree)
  gp = Graph_painter()
  gp.paint(chains, cc.graphFilename)
  dw.writePlotFile(cc.filename, cc.plotFilename)

def prepare(cc):
  chains = []
  for i in range(cc.k):
    chain = Chain(i)
    chain.updateParams(cc.data)
    chains.append(chain)
  for j in range(cc.n):
    flow = Flow(j)
    flow.updateParams(cc.data)
    for chain in chains:
      flow.chains.append(chains[i])
      chain.flows.append(flow)
  return chains

def updateConnectionsWindows(chains, t):
  for chain in chains:
    for flow in chain.flows:
      flow.e_dW(t)

def updateLenghtOfQueues(chains, t):
  for chain in chains:
    chain.e_dQ(t)

def saveData(chains, cc, t, dw):
  i = 0
  for chain in chains:
    dw.collect('q' + str(i), chain.qHist.get(t))
    x = chain.x(t)
    dw.collect('x' + str(i), x)
    dw.collect('p' + str(i), chain.p(x))
    i = i + 1
  i = 0
  for flow in chain.flows:
    #dw.collect('t' + str(i), flow.W(t)/flow.R(t))
    dw.collect('w' + str(i), flow.W(t))
    #dw.collect('r' + str(i), flow.R(t))
    i = i + 1
  dw.write(cc.filename)

if __name__ == '__main__':
  main()
