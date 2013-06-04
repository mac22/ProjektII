#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from math import floor

class Flow:
  def __init__(self):
    self.chains = []
    self.wHist = { 0 : self.wStart}

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
      #print(t, writ)
      if writ and w:
        ci = 0
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

