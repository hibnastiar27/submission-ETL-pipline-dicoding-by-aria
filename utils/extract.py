import requests
from bs4 import BeautifulSoup
from datetime import datetime

def ambil_elemen_teks(card, tag, class_name=None, contains_text=None, default=''):
  # mencari eleme HTML yang sesuai dengan kriteria
  if contains_text:
    elemen = card.find(tag, string=lambda t: t and contains_text in t)
  elif class_name:
    elemen = card.find(tag, class_=class_name)
  else:
    elemen = card.find(tag)
    
  # mengembalikan teks elemen
  return elemen.text.strip() if elemen else default

# untuk mengambil data produk
def ambil_data_produk(url):
  try:
    respon = requests.get(url, timeout=5)
    respon.raise_for_status()
  except requests.exceptions.RequestException as e:
    raise Exception(f"❌ Error akses URL {url}: {e}")

  try:
    soup = BeautifulSoup(respon.text, 'html.parser')
    produk_list = []

    for card in soup.find_all('div', class_='collection-card'):
      produk = {
        'title': ambil_elemen_teks(card, 'h3', class_name='product-title', default='Judul produk Tidak Diketahui'),
        'price': ambil_elemen_teks(card, 'div', class_name='price-container', default='Harga Tidak Tersedia'),
        'rating': ambil_elemen_teks(card, 'p', contains_text='Rating', default='Rating Tidak Ada'),
        'colors': ambil_elemen_teks(card, 'p', contains_text='Colors', default='Warna Tidak Ada'),
        'size': ambil_elemen_teks(card, 'p', contains_text='Size', default='Ukuran Tidak Ada'),
        'gender': ambil_elemen_teks(card, 'p', contains_text='Gender', default='Gender Tidak Ada'),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      }
      produk_list.append(produk)

    print(f"\n✅ Selamat kamu berhasil mengambil {len(produk_list)} produk dari {url}")
    return produk_list

  except Exception as e:
    raise Exception(f"Gagal parsing HTML {url}: {e}")

def banyak_produk(base_url="https://fashion-studio.dicoding.dev", max_produk=1000):
  produk_list = []
  halaman = 1

  while len(produk_list) < max_produk:
    # Format URL: halaman 1 = base_url, sisanya = /page2, /page3, dst
    url = base_url if halaman == 1 else f"{base_url}/page{halaman}"
    print(f"🔄 Mengambil halaman {halaman}: {url}")
    
    try:
      produk = ambil_data_produk(url)
      if not produk:
        print("🚫 Tidak ada produk ditemukan. Pengambilan dihentikan.")
        break

      produk_list.extend(produk)
    except Exception as e:
      print(f"❌ Gagal mengambil data dari halaman {halaman}: {e}")
      break

    halaman += 1

  produk_list = produk_list[:max_produk]
  print(f"\n✅ Total produk terkumpul: {len(produk_list)}")
  return produk_list
