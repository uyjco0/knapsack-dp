#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#
# 'tests_run.py'
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
# The 'knapsack-dp' is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with the 'knapsack-dp' files.  If not, see <http ://www.gnu.org/licenses/>.
#

import unittest
import imp
# import from another folder
dp = imp.load_source('utils', '../utils.py')
kp = imp.load_source('knapsack-dp', '../knapsack-dp.py')

class LoadProducts(unittest.TestCase):

   def test_cfg_name_fail(self):
      """
      Failing when there is not a configuration file name.
      """
      db_prods = dp.getDbObject()
      self.assertIsNone(db_prods)

   def test_cfg_name_fail1(self):
      """
      Failing when the configuration file has an empty file name.
      """
      db_prods = dp.getDbObject('config-err1.json')
      self.assertIsNone(db_prods)

   def test_cfg_name_fail2(self):
      """
      Failing when the configuration file has an invalid value (i.e. 0 in the amount of fields).
      """
      db_prods = dp.getDbObject('config-err2.json')
      self.assertIsNone(db_prods)

   def test_cfg_name_fail3(self):
      """
      Failing when the configuration file has an invalid value (i.e. 0 in volume length).
      """
      db_prods = dp.getDbObject('config-err3.json')
      self.assertIsNone(db_prods)

   def test_cfg_name_fail4(self):
      """
      Failing when the configuration file has an invalid value (i.e. -1 in volume width).
      """
      db_prods = dp.getDbObject('config-err4.json')
      self.assertIsNone(db_prods)

   def test_cfg_name_fail5(self):
      """
      Failing when the configuration file has an empty value (i.e. no value in volume width).
      """
      db_prods = dp.getDbObject('config-err5.json')
      self.assertIsNone(db_prods)

   def test_cfg_name_fail6(self):
      """
      Failing when the configuration file has an empty value (i.e. a in volume width).
      """
      db_prods = dp.getDbObject('config-err6.json')
      self.assertIsNone(db_prods)

   def test_cfg_name_success(self):
      """
      Success when there is a configuration file name.
      """
      db_prods = dp.getDbObject('config-val-err.json')
      self.assertIsNotNone(db_prods)

   def test_load_file_fail(self):
      """
      Failing when there is a wrong product file name.
      """
      db_prods = dp.getDbObject('config-val-err.json')
      # working with exceptions:
      #    self.assertRaises(name_expected_exception, function, function_arg1, function_arg2, ..)
      self.assertRaises(IOError, db_prods.loadProducts)

   def test_load_file_success(self):
      """
      Success loading the products file.
      The file has the following rows with problems:
         -> 1,556,24,14,15,1557,12 -> bad amount of fields (bad_product)
         -> a,712,33,20,19,944 -> the product ide (first field) is not an integer (bad_product)
         -> 6,-1947,29,26,21,984 -> the price (second field) is negative (bad_product)
         -> 7,939,33,18,36,2587 -> the height (fifth field) > 35 (descarted)
         -> 9,570,0,11,25,1996 -> the length (third field) = 0 (bad_product)
         -> 10,843,46,36,23,1769 -> the length (third field) > 45 (descarted)
         -> 29,1856,46,24,31,2231 -> the length (third field) > 45 (descarted)
         -> 30,1488,46,36,28,2608 -> the length (third field) > 45 (descarted)
      """
      db_prods = dp.getDbObject('config-val.json')
      db_prods.loadProducts()
      self.assertEqual(db_prods.getContainerVolume(), 45*30*35)
      self.assertEqual(db_prods.getAmountProducts(), 10)
      self.assertEqual(db_prods.getAmountDescartedProducts(), 4)
      self.assertEqual(db_prods.getAmountBadProducts(), 4)

   def test_access_individual_product_fail1(self):
      """
      Fail accessing individual product because wrong index:
         -> 1 <= index <= 6
      """
      db_prods = dp.getDbObject('config-val2.json')
      db_prods.loadProducts()
      self.assertIsNone(db_prods.getProductByIndex(-1))

   def test_access_individual_product_fail2(self):
      """
      Fail accessing individual product because wrong key.
         -> 1 <= index <= 6
      """
      db_prods = dp.getDbObject('config-val2.json')
      db_prods.loadProducts()
      self.assertIsNone(db_prods.getProductByIndex(8))

   def test_access_individual_product_succes1(self):
      """
      Success accessing individual product by the right key:
         -> 1 <= index <= 6
      """
      db_prods = dp.getDbObject('config-val2.json')
      db_prods.loadProducts()
      product = db_prods.getProductByIndex(1)
      self.assertEqual(product.getPid(), 9)
      self.assertEqual(product.getPrice(), 2)
      self.assertEqual(product.getVolume(), 1)
      self.assertEqual(product.getWeight(), 1)

   def test_access_individual_product_succes2(self):
      """
      Success accessing individual product by the right key:
         -> 1 <= index <= 6
      """
      db_prods = dp.getDbObject('config-val2.json')
      db_prods.loadProducts()
      product = db_prods.getProductByIndex(5)
      self.assertEqual(product.getPid(), 15)
      self.assertEqual(product.getPrice(), 10)
      self.assertEqual(product.getVolume(), 5)
      self.assertEqual(product.getWeight(), 1)

class SolveKnapsack(unittest.TestCase):

   def test_solve1(self):
      """
      Success finding the best solution:
         -> best: (price: 16, products: [11, 17], weight: 4)
         -> second best: (price: 16, products: [7, 30], weight: 6) 
      """
      db_prods = dp.getDbObject('config-val2.json')
      db_prods.loadProducts()
      sol = kp.fillTable(db_prods)
      self.assertListEqual(sol[2], [11, 17])
      self.assertEqual(kp.getSumIds(sol), 28)

   def test_solve3(self):
      """
      Success finding the best solution:
         -> best: (price: 16, products: [7, 30], weight: 6)
         -> second best: (price: 16, products: [11, 17], weight: 7)
      """
      db_prods = dp.getDbObject('config-val3.json')
      db_prods.loadProducts()
      sol = kp.fillTable(db_prods)
      sol2 = kp.getSumIds(sol)
      self.assertListEqual(sol[2], [7, 30])
      self.assertEqual(kp.getSumIds(sol), 37)

if __name__ == "__main__":
   unittest.main()
