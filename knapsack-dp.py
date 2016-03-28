#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#
# 'knapsack-dp.py'
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

import logging
from time import gmtime, strftime
# custom baseline functions
import utils

def fillTable(db_prods):
   """
   It fills the table for solving the 0-1 knapsack problem:
      according to the recurrence we don't need to hold the whole table in memory:
         it is only needed to have a structure for the current table' row (i.e. row_i) being filled and the previous
         row to it (ie.row_i-1)
   """
   # Initializing the solved row in the table:
   # each position in the table is a tuple with the following format:
   #    (price, weight, solution)
   table_previous_row = [(0, 0, [])] * (db_prods.getContainerVolume() + 1)
   # iterate from bottom up through the products index
   for i in xrange(1, db_prods.getAmountProducts() + 1):
      # Initializing the current row to solve in the table:
      table_current_row = [0] * (db_prods.getContainerVolume() + 1) 
      # Get the product associated to the current index
      current_product = db_prods.getProductByIndex(i)
      current_pvol = current_product.getVolume()
      current_pprice = current_product.getPrice()
      current_pweight = current_product.getWeight()
      current_pid = current_product.getPid()
      # iterate from bottom up through the the container volume range:
      #    it solves the following recurrence:
      #       [DV(i,v), c] =
      #          1. [DV(i-1, v), c]  if current_pvol > v
      #          2. max_{[DV[(i-1, v), c] , [DV(i-1, v' = v - current_pvol) + current_pprice,  c = c + current_product]}:
      #                if DV(i-1, v)  = DV(i-1, v' = v - current_pvol):
      #                   if total_weight(c) <= total_weight(c + current_product): 
      #                      [DV[(i-1, v), c]
      #                   else:
      #                      [DV(i-1, v' = v - current_pvol) + current_pprice,  c = c + current_product]
      for v in xrange(db_prods.getContainerVolume() + 1):
         if (current_pvol > v):
            # for v current_product is not part of the solution
      	    table_current_row[v] = table_previous_row[v]
         else:
            if (table_previous_row[v-current_pvol][0] + current_pprice) > table_previous_row[v][0]:
               table_current_row[v] = (table_previous_row[v-current_pvol][0] + current_pprice, table_previous_row[v-current_pvol][1] + current_pweight, table_previous_row[v-current_pvol][2]+ [current_pid])
            else:
               if (table_previous_row[v-current_pvol][0] + current_pprice) == table_previous_row[v][0]:
                  if table_previous_row[v-current_pvol][1] < table_previous_row[v][1]:
                     table_current_row[v] = (table_previous_row[v-current_pvol][0] + current_pprice, table_previous_row[v-current_pvol][1] + current_pweight, table_previous_row[v-current_pvol][2]+ [current_pid])
                  else:
                     table_current_row[v] = table_previous_row[v]
               else:
                  table_current_row[v] = table_previous_row[v]   
      table_previous_row = table_current_row
   return table_previous_row[db_prods.getContainerVolume()]


def getSumIds(sol):
   """
   It returns the sum of the product's IDs from the final solution
   """
   return reduce(lambda x,y: x+y, sol[2])
         
            
def main():
   """
   The script entry point.
   """
   # using a default log file
   logging.basicConfig(filename='knapsack-dp.log',level=logging.DEBUG)

   print "The program is starting ..."   

   db_prods = utils.getDbObject()

   # load the products from file
   if db_prods != None:
      try:
         logging.info('************* ###### *************')
         logging.info('************* ###### *************')
         logging.info('It starts to load the products file at: %s', strftime("%Y-%m-%d %H:%M:%S", gmtime()))
         db_prods.loadProducts()
         logging.info('It ends to load the products file at: %s', strftime("%Y-%m-%d %H:%M:%S", gmtime()))
         logging.info('Amount of products loaded: %s', db_prods.getAmountProducts())
         logging.info('Amount of products descarted: %s', db_prods.getAmountDescartedProducts())
         logging.info('Amount of bad products: %s', db_prods.getAmountBadProducts())
      except IOError:
         logging.error('There was not possible to load the products file! The file name is: %s', db_prods.getFileName())
      else:
         # solve the 0-1 knapsack problem for the products in db_prods
         logging.info('It starts to solve at: %s', strftime("%Y-%m-%d %H:%M:%S", gmtime()))
         sol = fillTable(db_prods)
         logging.info('It gets the solution at: %s', strftime("%Y-%m-%d %H:%M:%S", gmtime()))
         logging.info('The solution is: %s', (sol[2], getSumIds(sol)))
         print "The final solution is: {}".format(getSumIds(sol))
   else:
      logging.error('There was not possible to load the configuration file')


if __name__ == "__main__":
    main()
