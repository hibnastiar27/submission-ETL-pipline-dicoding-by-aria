import sys
import os

# Tambahkan path root agar modul utils bisa diimpor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from utils.extract import ambil_data_produk, ambil_elemen_teks, banyak_produk
from bs4 import BeautifulSoup

class TestProductScraping(unittest.TestCase):

  @patch('utils.extract.requests.get')
  def test_fetch_product_data_success(self, mock_requests_get):
    """Test saat fetch data berhasil (status 200)"""
    sample_url = "https://fashion-studio.dicoding.dev/"
    
    # Simulasi respons HTML dari web
    mock_html = """
    <html>
      <body>
        <div class="collection-card">
          <h3 class="product-title">Sample Product</h3>
          <div class="price-container">$15</div>
          <p>Rating: 4.5 stars</p>
          <p>Colors: Red, Green</p>
          <p>Size: S, M</p>
          <p>Gender: Female</p>
        </div>
      </body>
    </html>
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = mock_html
    mock_requests_get.return_value = mock_response

    # Jalankan fungsi
    products = ambil_data_produk(sample_url)

    # Validasi hasil
    self.assertIsInstance(products, list)
    self.assertGreater(len(products), 0)
    self.assertEqual(products[0]['title'], 'Sample Product')

  @patch('utils.extract.requests.get')
  def test_fetch_product_data_failure(self, mock_requests_get):
    """Test saat fetch data gagal (status error 404)"""
    error_url = "https://fashion-studio.dicoding.dev/"
    
    # Simulasi error HTTP
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = Exception("404 Client Error")
    mock_requests_get.return_value = mock_response

    # Validasi exception dilempar
    with self.assertRaises(Exception) as error:
      ambil_data_produk(error_url)
    
    self.assertEqual(str(error.exception), "404 Client Error")



class TestAmbilElemenTeks(unittest.TestCase):
  def test_elemen_dengan_class(self):
    html = '<div><h3 class="product-title">Produk A</h3></div>'
    soup = BeautifulSoup(html, 'html.parser')
    card = soup.find('div')
    hasil = ambil_elemen_teks(card, 'h3', class_name='product-title')
    self.assertEqual(hasil, 'Produk A')

  def test_elemen_dengan_contains_text(self):
    html = '<div><p>Rating: 4.5</p></div>'
    soup = BeautifulSoup(html, 'html.parser')
    card = soup.find('div')
    hasil = ambil_elemen_teks(card, 'p', contains_text='Rating')
    self.assertEqual(hasil, 'Rating: 4.5')

  def test_elemen_default_tidak_ditemukan(self):
    html = '<div></div>'
    soup = BeautifulSoup(html, 'html.parser')
    card = soup.find('div')
    hasil = ambil_elemen_teks(card, 'span', default='Tidak Ada')
    self.assertEqual(hasil, 'Tidak Ada')


class TestBanyakProduk(unittest.TestCase):
  @patch('utils.extract.ambil_data_produk')
  def test_banyak_produk_terbatas(self, mock_ambil_data):
    dummy_produk = [{
      'title': 'Dummy',
      'price': 'Rp0',
      'rating': 'Rating: 0',
      'colors': 'Colors: None',
      'size': 'Size: None',
      'gender': 'Gender: None',
      'timestamp': '2025-05-18 00:00:00'
    }]
    mock_ambil_data.return_value = dummy_produk

    hasil = banyak_produk(max_produk=3)
    self.assertEqual(len(hasil), 3)
    self.assertEqual(hasil[0]['title'], 'Dummy')

  @patch('utils.extract.ambil_data_produk')
  def test_banyak_produk_berhenti_saat_kosong(self, mock_ambil_data):
    mock_ambil_data.side_effect = [
      [{'title': 'A', 'price': 'Rp1', 'rating': '', 'colors': '', 'size': '', 'gender': '', 'timestamp': ''}],
      [],  # halaman 2 kosong
    ]
    hasil = banyak_produk(max_produk=10)
    self.assertEqual(len(hasil), 1)


if __name__ == '__main__':
  import unittest
  unittest.main()
