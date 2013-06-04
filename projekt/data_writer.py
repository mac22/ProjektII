#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Data_writer:
  def __init__(self):
    self.order = []
    self.dictionary = {}

  def collect(self, name, value):
    if not (name in self.order):
      self.order.append(name)
    self.dictionary[name] = value

  def resetData(self):
    self.dictionary.clear()

  def writePlotFile(self, filename = None, plot_filename = None):
    if plot_filename:
      f = open(plot_filename, 'w')
      print('plot', end=' ', file=f)
      corder = len(self.order)
      for i in range(corder):
        if corder - 1 == i:
          print('"' + filename + '" using ' + str(i+1) + ' title \'' + self.order[i] + '\' with lines', end='\n', file=f)
        else:
          print('"' + filename + '" using ' + str(i+1) + ' title \'' + self.order[i] + '\' with lines, \\', end='\n', file=f)
      f.close()
  
  def write(self, filename = None):
    if filename:
      f = open(filename, 'a')
      for i in self.order:
        print(str(self.dictionary[i]), end=' ', file=f)
      print('', file=f)
      f.close()

    else:
      for i in self.order:
        print(str(i) + ': ' + str(self.dictionary[i]))

  def reset(self, filename):
    if filename:
      f = open(filename, 'w')
      print('', end='', file=f)
      f.close()
