#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Chain:
  def __init__(self):
    self.qHist = { 0 : self.qStart }
    self.flows = []
    self.xHist = { }

  def q(self, t):
    if t < 0:
      return self.q
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
    elif result > self.qmax:
      self.qHist[th] = self.qmax
    else:
      self.qHist[th] = result 
    return self.qHist[th]

  def x(self, t):
    t = round(t, self.roundDegree)
    if t < 0:
      return 1
    if self.xHist.get(t) == None:
      self.xHist[t] = self.alfa * self.q(t) + (1 - self.alfa) * self.x(t-1)
    return self.xHist[t]

  def p(self, x):
    if 0 <= x < self.tMin:
      return 0
    elif self.tMin <= x <= self.tMax:
      return (x - self.tMin)/(self.tMax - self.tMin) * self.pMax
    elif self.tMax < x <= self.b:
      return 1
    else:
      raise Exception('Niepoprawna wartosc x:', x)

