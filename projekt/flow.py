#!/usr/bin/python
# -*- coding: UTF-8 -*-
from math import floor

class Flow:
  def __init__(self, number):
    self.name = 'Flow' + str(number)
    self.nodes = []
    self.wHist = { 0 : self.wStart}

  def updateParams(self, dataDict):
    if dataDict.has_key(self.name):
      for i in range(len(dataDict[self.name])):
        val = dataDict[self.name][i][0]
        if val == 'tp':
          self.tp = float(dataDict[self.name][i][1])
        elif val == 'w':
          self.wStart = float(dataDict[self.name][i][1])
        elif val == 'node':
          curData = dataDict[self.name][i][1].split(',')
          self.nodeStart = []
          for data in curData:
            self.nodeStart.append(data.strip().capitalize())
        elif val == 'print':
          curData = dataDict[self.name][i][1].split(',')
          self.printVal = set()
          for data in curData:
            self.printVal.add(data.strip())

      self.wHist = { 0 : self.wStart}

  def connectWithNode(self, nodes):
    for nodeName in self.nodeStart:
      for node in nodes:
        if node.name == nodeName:
          self.nodes.append(node)
          node.flows.append(self)

  def R(self, t):
    if t < 0:
      return 0
    ci = 0
    for node in self.nodes:
      ci += node.q(t)/node.c
    return ci + self.tp

  def e_dW(self, t):
    def f(t, w):
      rit = self.R(t)
      trit = round((t - rit) * self.mod)/self.mod
      writ = self.W(trit)
      if writ and w:
        ci = 1
        for node in self.nodes:
          ci *= 1 - node.p(node.x(trit))
        if ci:
          return 1/rit - w/2. * writ/self.R(trit) * (1 - ci)
      return 1/rit 

    if t < 0:
      return 0
    wit = self.W(t)
    th = round(t + self.h, self.roundDegree)
    self.wHist[th] = wit + self.h * f(t, wit)
    return self.wHist[th]

  def W(self, t):
    if t < 0:
      return 0
    elif self.wHist.get(t) == None:
      raise Exception('Wartosc W dla t: ', t, ' nie istnieje')
    return self.wHist[t]

