#!/usr/bin/python
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
      f.write('plot ')
      corder = len(self.order)
      for i in range(corder):
        if not ( 0 == i ):
          if corder - 1 == i:
            f.write('"' + filename + '" using 1:' + str(i+1) + ' title \'' + self.order[i] + '\' with lines\n')
          else :
            f.write('"' + filename + '" using 1:' + str(i+1) + ' title \'' + self.order[i] + '\' with lines, \\\n')
      f.close()
  
  def write(self, filename = None):
    if filename:
      f = open(filename, 'a')
      for i in self.order:
        f.write(str(self.dictionary[i]) + ' ')
      f.write('\n')
      f.close()

    else :
      for i in self.order:
        print str(i) + ': ' + str(self.dictionary[i])

  def reset(self, filename):
    if filename:
      f = open(filename, 'w')
      f.close()
