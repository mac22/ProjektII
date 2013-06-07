#!/usr/bin/python
# -*- coding: UTF-8 -*-
from config_container import Config_container
import configparser
from node import Node
from flow import Flow
from math import ceil, log

class Config_reader:
  def read(self):
    self.cc = Config_container()
    self.cc.data = {}
    self.cp = configparser.ConfigParser()
    self.cp.readfp(open('config.ini'))
    try :
      self.cc.n = self.cp.getint('General', 'flows')
      self.cc.k = self.cp.getint('General', 'nodes')
      self.cc.simT = self.cp.getint('General', 'simulation_time')
      self.cc.h = self.cp.getfloat('General', 'step')
      self.cc.filename = self.cp.get('General', 'data_filename')
      self.cc.plotFilename = self.cp.get('General', 'plot_filename')
      self.cc.graphFilename = self.cp.get('General', 'graph_filename')

      Node.tMin = self.cp.getfloat('Nodes', 'tMin')
      Node.tMax = self.cp.getfloat('Nodes', 'tMax')
      Node.pMax = self.cp.getfloat('Nodes', 'pMax')
      Node.qStart = self.cp.getfloat('Nodes', 'q')
      Node.alfa = self.cp.getfloat('Nodes', 'alfa')
      Node.b = self.cp.getfloat('Nodes', 'b')
      Node.c = self.cp.getfloat('Nodes', 'c')
      Node.qMax = self.cp.getfloat('Nodes', 'qMax')

      curData = self.cp.get('Nodes', 'print')
      curData = curData.split(',')
      Node.printVal = set()
      for data in curData:
        Node.printVal.add(data.strip())

      Flow.tp = self.cp.getfloat('Flows', 'tp')
      Flow.wStart = self.cp.getfloat('Flows', 'w')

      curData = self.cp.get('Flows', 'node')
      curData = curData.split(',')
      Flow.nodeStart = []
      for data in curData:
        Flow.nodeStart.append(data.strip().capitalize())

      curData = self.cp.get('Flows', 'print')
      curData = curData.split(',')
      Flow.printVal = set()
      for data in curData:
        Flow.printVal.add(data.strip())

    except configparser.NoOptionError as ex:
      print('Błąd konfiguracji! W sekcji', ex.args[1], 'brakuje parametru', ex.args[0])
      quit()
    except configparser.NoSectionError as ex:
      print('Błąd konfiguracji! Brakuje sekcji', ex.args[0])
      quit()

    self.readOtherSections()

    self.cc.mod = 1/self.cc.h
    self.cc.roundDegree = int(ceil(log(self.cc.mod, 10)))
    Node.h = Flow.h = self.cc.h
    Node.mod = Flow.mod = self.cc.mod
    Node.roundDegree = Flow.roundDegree = self.cc.roundDegree
    return self.cc

  def readOtherSections(self):
    for i in range(self.cc.k):
      name = 'Node' + str(i)
      if self.cp.has_section(name):
        self.cc.data[name] = self.cp.items(name)

    for i in range(self.cc.n):
      name = 'Flow' + str(i)
      if self.cp.has_section(name):
        self.cc.data[name] = self.cp.items(name)

