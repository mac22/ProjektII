#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from chain import Chain
from flow import Flow
from data_writer import Data_writer
from math import ceil, log
from config_container import Config_container
import configparser

CHAINS = []

def main():
  cc = Config_container()
  dw = Data_writer()
  load(cc)
  prepare(cc)
  t = 0
  cc.simT = 1000
  dw.reset(cc.filename)
  while t < cc.simT:
    updateConnectionsWindows(t)
    updateLenghtOfQueues(t)
    saveData(t, dw, cc)
    t = round(t + cc.h, cc.roundDegree)
  dw.writePlotFile(cc.filename, cc.plotFilename)

def load(cc):
  cp = configparser.ConfigParser()
  cp.readfp(open('config.ini'))
  try:
    cc.n = cp.getint('General', 'flows')
    cc.k = cp.getint('General', 'chains')
    cc.simT = cp.getint('General', 'simulation_time')
    cc.h = cp.getfloat('General', 'step')
    cc.filename = cp.get('General', 'data_filename')
    cc.plotFilename = cp.get('General', 'plot_filename')

    Chain.tMin = cp.getfloat('Chains', 'tMin')
    Chain.tMax = cp.getfloat('Chains', 'tMax')
    Chain.pMax = cp.getfloat('Chains', 'pMax')
    Chain.qStart = cp.getfloat('Chains', 'q')
    Chain.alfa = cp.getfloat('Chains', 'alfa')
    Chain.b = cp.getfloat('Chains', 'b')
    Chain.c = cp.getfloat('Chains', 'c')
    Chain.qmax = cp.getfloat('Chains', 'qmax')

    Flow.tp = cp.getfloat('Flows', 'tp')
    Flow.wStart = cp.getfloat('Flows', 'w')

  except configparser.NoOptionError as ex:
    print('Błąd konfiguracji! W sekcji', ex.args[1], 'brakuje parametru', ex.args[0])
    quit()
  except configparser.NoSectionError as ex:
    print('Błąd konfiguracji! Brakuje sekcji', ex.args[0])
    quit()

  cc.mod = 1/cc.h
  cc.roundDegree = ceil(log(cc.mod, 10))
  Chain.h = Flow.h = cc.h
  Chain.mod = Flow.mod = cc.mod
  Chain.roundDegree = Flow.roundDegree = cc.roundDegree

def prepare(cc):
  for i in range(cc.k):
    CHAINS.append(Chain())
    for j in range(cc.n):
      flow = Flow()
      flow.chains.append(CHAINS[i])
      CHAINS[i].flows.append(flow)

def updateConnectionsWindows(t):
  for chain in CHAINS:
    for flow in chain.flows:
      flow.e_dW(t)

def updateLenghtOfQueues(t):
  for chain in CHAINS:
    chain.e_dQ(t)

def saveData(t, dw, cc):
  i = 0
  for chain in CHAINS:
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
