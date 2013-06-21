#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Node:
  def __init__(self, number):
    self.name = 'Node' + str(number)
    self.qHist = { 0 : self.qStart }
    self.flows = []
    self.xHist = { }

  def updateParams(self, dataDict):
    if dataDict.has_key(self.name):
      for i in range(len(dataDict[self.name])):
        val = dataDict[self.name][i][0]
        if val == 'tmin':
          self.tMin = float(dataDict[self.name][i][1])
        elif val == 'tmax':
          self.tMax = float(dataDict[self.name][i][1])
        elif val == 'pmax':
          self.pMax = float(dataDict[self.name][i][1])
        elif val == 'q':
          self.qStart = float(dataDict[self.name][i][1])
        elif val == 'alfa':
          self.alfa = float(dataDict[self.name][i][1])
        elif val == 'b':
          self.b = float(dataDict[self.name][i][1])
        elif val == 'c':
          self.c = float(dataDict[self.name][i][1])
        elif val == 'qmax':
          self.qMax = float(dataDict[self.name][i][1])
        elif val == 'print':
          curData = dataDict[self.name][i][1].split(',')
          self.printVal = set()
          for data in curData:
            self.printVal.add(data.strip())

      self.qHist = { 0 : self.qStart }

  def q(self, t):
    t = round(t, self.roundDegree)
    if t < 0:
      return self.qStart
    elif self.qHist.get(t) == None:
      raise Exception('Wartosc Q dla t: ', t, ' nie istnieje')
    return self.qHist[t] 

  def e_dQ(self, t):
    def f(t):
      wirt = 0
      for flow in self.flows:
        wirt += flow.W(t) / flow.R(t)
      return -self.c + wirt

    th = round(t + self.h, self.roundDegree)
    result = self.q(t) + self.h * f(t)
    if 0 > result:
      self.qHist[th] = 0
    elif result > self.qMax:
      self.qHist[th] = self.qMax
    else :
      self.qHist[th] = result 
    return self.q(th)

  def x(self, t):
    t = round(t, self.roundDegree)
    if t < 0:
      return self.qStart
    if self.xHist.get(t) == None:
      self.xHist[t] = self.alfa * self.q(t) + (1 - self.alfa) * self.x(t - self.h)
    return self.xHist[t]

  def p(self, x):
    if 0 <= x < self.tMin:
      return 0
    elif self.tMin <= x <= self.tMax:
      return (x - self.tMin)/(self.tMax - self.tMin) * self.pMax
    elif self.tMax < x <= self.b:
      return 1
    else :
      raise Exception('Niepoprawna wartosc x:', x)

