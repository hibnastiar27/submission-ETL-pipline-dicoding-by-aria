# import unittest
# from utils.transform import transformasi_produk

# class TestTransform(unittest.TestCase):

#   def test_transform_data(self):
#     print("\n🔍 [TEST] test_transform_data")
#     products = [
#       {'title': 'Product 1', 'price': '10000', 'rating': '4.5', 'colors': '3', 'size': 'M', 'gender': 'Men'},
#       {'title': 'Product 2', 'price': '20000', 'rating': '5.0', 'colors': '3', 'size': 'L', 'gender': 'Women'}
#     ]
#     df = transformasi_produk(products)
#     self.assertEqual(len(df), 2)
#     self.assertIn('price', df.columns)
#     self.assertIn('rating', df.columns)
#     self.assertIn('timestamp', df.columns)
#     self.assertTrue(df['price'].iloc[0] > 0)
#     self.assertTrue(df['rating'].iloc[0] > 0)

#   def test_invalid_title(self):
#     print("🔍 [TEST] test_invalid_title")
#     products = [
#       {'title': 'Unknown Product', 'price': '10000', 'rating': '4.5', 'colors': '3', 'size': 'M', 'gender': 'Men'}
#     ]
#     df = transformasi_produk(products)
#     self.assertEqual(len(df), 0)  # di drop karena price invalid
      
#   def test_invalid_price(self):
#     print("🔍 [TEST] test_invalid_price")
#     products = [
#       {'title': 'Product 1', 'price': 'invalid_price', 'rating': '4.5', 'colors': '3', 'size': 'M', 'gender': 'Men'}
#     ]
#     df = transformasi_produk(products)
#     self.assertEqual(len(df), 0)  # di drop karena price invalid

#   def test_invalid_rating(self):
#     print("🔍 [TEST] test_invalid_rating")
#     products = [
#       {'title': 'Product 1', 'price': '10000', 'rating': 'bad_rating', 'colors': '3', 'size': 'M', 'gender': 'Men'}
#     ]
#     df = transformasi_produk(products)
#     self.assertEqual(len(df), 0)  # di Drop karena rating invalid

#   def test_invalid_colors(self):
#     print("🔍 [TEST] test_invalid_colors")
#     products = [
#       {'title': 'Product 1', 'price': '10000', 'rating': '4.5', 'colors': 'no_colors', 'size': 'M', 'gender': 'Men'}
#     ]
#     df = transformasi_produk(products)
#     self.assertEqual(len(df), 0)  # di drop karena colors invalid

#   def test_mixed_invalid(self):
#     print("🔍 [TEST] test_mixed_invalid")
#     products = [
#       {'title': 'Unknown Product', 'price': '10000', 'rating': '4.5', 'colors': '3', 'size': 'M', 'gender': 'Men'},
#       {'title': 'Product 2', 'price': '10000', 'rating': '4.5', 'colors': '3', 'size': 'M', 'gender': 'Men'},
#       {'title': 'Product 3', 'price': 'bad_price', 'rating': '5.0', 'colors': '3', 'size': 'L', 'gender': 'Women'},
#       {'title': 'Product 4', 'price': '15000', 'rating': 'bad_rating', 'colors': '3', 'size': 'S', 'gender': 'Men'},
#       {'title': 'Product 5', 'price': '12000', 'rating': '4.0', 'colors': 'bad_colors', 'size': 'M', 'gender': 'Women'}
#     ]
#     df = transformasi_produk(products)
#     self.assertEqual(len(df), 1)  # Hanya product 1 yg valid

# if __name__ == '__main__':
#   unittest.main()

import pytest
from colorama import Fore, Style, init
from utils.transform import transformasi_produk

init(autoreset=True)  # Supaya warna otomatis reset setelah print
def print_test_name(name):
    print(Fore.GREEN + Style.BRIGHT + f"\n🔍 [TEST] {name}")

def test_transform_data():
    print_test_name("test_transform_data")
    products = [
        {'title': 'Product 1', 'price': '10000', 'rating': '4.5', 'colors': '3', 'size': 'M', 'gender': 'Men'},
        {'title': 'Product 2', 'price': '20000', 'rating': '5.0', 'colors': '3', 'size': 'L', 'gender': 'Women'}
    ]
    df = transformasi_produk(products)
    assert len(df) == 2
    assert 'price' in df.columns
    assert 'rating' in df.columns
    assert 'timestamp' in df.columns
    assert df['price'].iloc[0] > 0
    assert df['rating'].iloc[0] > 0

def test_invalid_title():
    print_test_name("test_invalid_title")
    products = [
        {'title': 'Unknown Product', 'price': '10000', 'rating': '4.5', 'colors': '3', 'size': 'M', 'gender': 'Men'}
    ]
    df = transformasi_produk(products)
    assert len(df) == 0

def test_invalid_price():
    print_test_name("test_invalid_price")
    products = [
        {'title': 'Product 1', 'price': 'invalid_price', 'rating': '4.5', 'colors': '3', 'size': 'M', 'gender': 'Men'}
    ]
    df = transformasi_produk(products)
    assert len(df) == 0

def test_invalid_rating():
    print_test_name("test_invalid_rating")
    products = [
        {'title': 'Product 1', 'price': '10000', 'rating': 'bad_rating', 'colors': '3', 'size': 'M', 'gender': 'Men'}
    ]
    df = transformasi_produk(products)
    assert len(df) == 0

def test_invalid_colors():
    print_test_name("test_invalid_colors")
    products = [
        {'title': 'Product 1', 'price': '10000', 'rating': '4.5', 'colors': 'no_colors', 'size': 'M', 'gender': 'Men'}
    ]
    df = transformasi_produk(products)
    assert len(df) == 0

def test_mixed_invalid():
    print_test_name("test_mixed_invalid")
    products = [
        {'title': 'Unknown Product', 'price': '10000', 'rating': '4.5', 'colors': '3', 'size': 'M', 'gender': 'Men'},
        {'title': 'Product 2', 'price': '10000', 'rating': '4.5', 'colors': '3', 'size': 'M', 'gender': 'Men'},
        {'title': 'Product 3', 'price': 'bad_price', 'rating': '5.0', 'colors': '3', 'size': 'L', 'gender': 'Women'},
        {'title': 'Product 4', 'price': '15000', 'rating': 'bad_rating', 'colors': '3', 'size': 'S', 'gender': 'Men'},
        {'title': 'Product 5', 'price': '12000', 'rating': '4.0', 'colors': 'bad_colors', 'size': 'M', 'gender': 'Women'}
    ]
    df = transformasi_produk(products)
    assert len(df) == 1

