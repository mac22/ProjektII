#!/usr/bin/python
# -*- coding: UTF-8 -*-
from math import floor

class Flow:
  def __init__(self, number):
    self.name = 'Flow' + str(number)
    self.chains = []
    self.wHist = { 0 : self.wStart}

  def updateParams(self, dataDict):
    if dataDict.has_key(self.name):
      for i in range(len(dataDict[self.name])):
        val = dataDict[self.name][i][0]
        if val == 'tp':
          self.tp = float(dataDict[self.name][i][1])
        elif val == 'wstart':
          self.wStart = float(dataDict[self.name][i][1])
        elif val == 'chain':
          curData = dataDict[self.name][i][1].split(',')
          self.chainStart = []
          for data in curData:
            self.chainStart.append(data.strip().capitalize())
        elif val == 'print':
          curData = dataDict[self.name][i][1].split(',')
          self.printVal = set()
          for data in curData:
            self.printVal.add(data.strip())

      self.wHist = { 0 : self.wStart}

  def connectWithChain(self, chains):
    for chainName in self.chainStart:
      for chain in chains:
        if chain.name == chainName:
          self.chains.append(chain)
          chain.flows.append(self)
          break

  def R(self, t):
    if t < 0:
      return 0
    ci = 0
    for chain in self.chains:
      ci += chain.q(t)/chain.c
    return ci + self.tp

  def e_dW(self, t):
    def f(t, w):
      rit = self.R(t)
      trit = round((t - rit) * self.mod)/self.mod
      writ = self.W(trit)
      if writ and w:
        ci = 1
        for chain in self.chains:
          ci *= chain.p(chain.x(trit))
        if (1 - ci):
          return 1/rit - w/2. * writ/self.R(trit) * (1 - ci)
      return 1/rit 

    if t < 0:
      return 0
    wit = self.W(t)
    th = round(t + self.h, self.roundDegree)
    self.wHist[th] = wit + self.h * f(t, wit)
    return self.wHist[th]

  def W(self, t):
    if t <= 0:
      return 0
    elif self.wHist.get(t) == None:
      raise Exception('Wartosc W dla t: ', t, ' nie istnieje')
    return self.wHist[t]

