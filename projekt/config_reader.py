#!/usr/bin/python
# -*- coding: UTF-8 -*-
from config_container import Config_container
import configparser
from chain import Chain
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
      self.cc.k = self.cp.getint('General', 'chains')
      self.cc.simT = self.cp.getint('General', 'simulation_time')
      self.cc.h = self.cp.getfloat('General', 'step')
      self.cc.filename = self.cp.get('General', 'data_filename')
      self.cc.plotFilename = self.cp.get('General', 'plot_filename')
      self.cc.graphFilename = self.cp.get('General', 'graph_filename')

      Chain.tMin = self.cp.getfloat('Chains', 'tMin')
      Chain.tMax = self.cp.getfloat('Chains', 'tMax')
      Chain.pMax = self.cp.getfloat('Chains', 'pMax')
      Chain.qStart = self.cp.getfloat('Chains', 'q')
      Chain.alfa = self.cp.getfloat('Chains', 'alfa')
      Chain.b = self.cp.getfloat('Chains', 'b')
      Chain.c = self.cp.getfloat('Chains', 'c')
      Chain.qMax = self.cp.getfloat('Chains', 'qMax')

      Flow.tp = self.cp.getfloat('Flows', 'tp')
      Flow.wStart = self.cp.getfloat('Flows', 'w')

    except configparser.NoOptionError as ex:
      print('Błąd konfiguracji! W sekcji', ex.args[1], 'brakuje parametru', ex.args[0])
      quit()
    except configparser.NoSectionError as ex:
      print('Błąd konfiguracji! Brakuje sekcji', ex.args[0])
      quit()

    self.readOtherSections()

    self.cc.mod = 1/self.cc.h
    self.cc.roundDegree = int(ceil(log(self.cc.mod, 10)))
    Chain.h = Flow.h = self.cc.h
    Chain.mod = Flow.mod = self.cc.mod
    Chain.roundDegree = Flow.roundDegree = self.cc.roundDegree
    return self.cc

  def readOtherSections(self):
    for i in range(self.cc.k):
      name = 'Chain' + str(i)
      if self.cp.has_section(name):
        self.cc.data[name] = self.cp.items(name)

    for i in range(self.cc.n):
      name = 'Flow' + str(i)
      if self.cp.has_section(name):
        self.cc.data[name] = self.cp.items(name)

