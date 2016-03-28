#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#
# 'utils.py'
#
# Copyright (C) 2015 Jorge Couchet <jorge.couchet at gmail.com>
#
# This file is part of 'knapsack-dp' project
# 
# The 'knapsack-dp' project is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# The 'knapsack-dp' project is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with the 'knapsack-dp' files.  If not, see <http ://www.gnu.org/licenses/>.
#

import sys
import csv
import json
import argparse

class Product(object):
   """
   The class in charge of managing the individual products.
   """
   def __init__(self, pid, price, length, width, height, weight):
      self.__pid = pid
      self.__price = price
      self.__length = length
      self.__height = height
      self.__width = width
      self.__weight = weight

   def getPid(self):
      return self.__pid

   def getPrice(self):
      return self.__price

   def getWeight(self):
      return self.__weight

   def getVolume(self):
      return self.__length*self.__height*self.__width


class Products(object):
   """
   The class in charge of managing the in-memory db with the available products.
   """
   def __init__(self, file_name, products_amount_fields, container_vol_length, container_vol_width, container_vol_heigth):
      # the file with the products detail
      self.__file_name = file_name
      # the amounts of fields that has the product 's detail in the file
      self.__products_amount_fields = products_amount_fields
      # the container volume dimensions
      self.__container_vol_length = container_vol_length
      self.__container_vol_width = container_vol_width
      self.__container_vol_heigth = container_vol_heigth
      # a dict indexing the products by i, where:
      #   -> 1 <= i <= #products
      self.__indexed_prods = {}
      # amount the products that are loaded effectively the db
      self.__amount_products = 0
      # amount the products that doesn't fit the container
      self.__amount_descarted_products = 0
      # amount of products with bad format
      self.__amount_bad_products = 0

   def loadProducts(self):
      """
      It loads the in-memory db from file.
      """
      with open(self.__file_name, 'rb') as csvf:
         csvr = csv.reader(csvf, delimiter=',')
         # counting the products with a bad format
         bad_products = 0
         # counting the number of products that are not fitting the container
         descarted_products = 0
         # used to index the objects in the order that they are appearing in the file
         product_index = 1
         # row format: product ID, price, length, width, height, weight
         for row in csvr:
            if len(row) == self.__products_amount_fields:
               # convert to integers the row elements
               try:
                  row = map(lambda x: int(x), row)
               except:
                  bad_products +=1
               else:
                  # select only the products that fit the container 's volume
                  if (row[2] <= self.__container_vol_length) and (row[3] <= self.__container_vol_width) and (row[4] <= self.__container_vol_heigth):
                     # Check that there are valid values
                     if (row[1] >=0) and (row[2] > 0) and (row[3] > 0) and (row[4] > 0) and (row[5] >= 0):
                        # create the new product object to store in the db
                        product = Product(row[0], row[1], row[2], row[3], row[4], row[5])
                        # load the product to the db
                        self.__indexed_prods[product_index] = product
                        product_index += 1
                     else:
                        bad_products +=1
                  else:
                     descarted_products += 1
            else:
               bad_products +=1

         self.__amount_descarted_products = descarted_products
         self.__amount_products = len(self.__indexed_prods)
         self.__amount_bad_products = bad_products

   def getFileName(self):
      return self.__file_name

   def getProductByIndex(self, ind):
      """
      If ind is wrong it returns None.
      """
      if ind in self.__indexed_prods:
         return self.__indexed_prods[ind]
      else:
         return None

   def getContainerVolume(self):
      return self.__container_vol_length*self.__container_vol_width*self.__container_vol_heigth

   def getAmountProducts(self):
      return self.__amount_products

   def getAmountDescartedProducts(self):
      return self.__amount_descarted_products

   def getAmountBadProducts(self):
      return self.__amount_bad_products


def openConfig(config_name):
   """
   It loads the configuration file and returns the parsed JSON file.
   """
   with open(config_name) as jfile:
      cfg = json.load(jfile)
      return cfg


def getDbObject(*argv):
   """
   It gets the name of the configuration file, and returns the object for the in-memory db.
   If something is going wrong it is returning None
   """
   if len(argv) != 0:
      cfg_file_name = argv[0]
   else:
      parser = argparse.ArgumentParser(description="Simple program to resolve the 0-1 Knapsack problem through Dynamic Programming")
      parser.add_argument('-c','--cfg', help="The path and name for the configuration file", default='')
      args = parser.parse_args()
      cfg_file_name = args.cfg

   if cfg_file_name != "":
      try:
         cfg = openConfig(cfg_file_name)
      except IOError:
         return None
      except ValueError:
         return None
      else:
         try:
            cfg['products']['amount_fields'] = int(cfg['products']['amount_fields'])
            cfg['container']['volume_length'] = int(cfg['container']['volume_length'])
            cfg['container']['volume_width'] = int(cfg['container']['volume_width'])
            cfg['container']['volume_height'] = int(cfg['container']['volume_height'])
            # check if the configuration file has valid values
            if (cfg['products']['file_path'] == '') or (cfg['products']['amount_fields'] <= 0) or (cfg['container']['volume_length'] <= 0) or (cfg['container']['volume_width'] <=0) or (cfg['container']['volume_height'] <= 0):
               return None
            else:
               # create the in-memory db for the products
               db_prods = Products(cfg['products']['file_path'], cfg['products']['amount_fields'], cfg['container']['volume_length'], cfg['container']['volume_width'], cfg['container']['volume_height'])
               return db_prods
         except:
            return None
   else:
      return None

