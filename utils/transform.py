import pandas as pd
import numpy as np
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
pd.set_option('future.no_silent_downcasting', True)

def transformasi_produk(data_produk):
  # """Transformasi dan normalisasi data produk mentah menjadi data siap pakai."""
  """
  Transformasi dan pembersihan data produk mentah menjadi DataFrame siap pakai.

  Args:
    data_produk (list of dict): Data produk hasil ekstraksi web.

  Returns:
    pd.DataFrame: Data produk yang sudah bersih dan terformat.
  """

  print(f"📝 Jumlah data awal: {len(data_produk)}")

  df = pd.DataFrame(data_produk)
  
  # Pastikan kolom yang dibutuhkan ada
  expected_cols = ['title', 'price', 'rating', 'colors', 'size', 'gender']
  for col in expected_cols:
    if col not in df.columns:
      df[col] = np.nan

  # Filter produk dengan judul tidak valid (mengandung 'unknown')
  df = df[~df['title'].str.lower().str.contains('unknown', na=False)]

  # Konversi harga: hapus karakter non-digit, ubah ke float, konversi ke Rupiah
  df['price'] = (
      df['price']
      .str.replace(r'[^\d.]', '', regex=True)
      .replace('', np.nan)
  )
  df['price'] = pd.to_numeric(df['price'], errors='coerce') * 16000

  # Ekstrak angka dari rating dan konversi ke float
  df['rating'] = (
    df['rating']
    .str.extract(r'([\d.]+)', expand=False)
  )
  df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

  # Ekstrak angka dari colors, konversi ke integer nullable
  df['colors'] = (
    df['colors']
    .str.extract(r'(\d+)', expand=False)
  )
  df['colors'] = pd.to_numeric(df['colors'], errors='coerce').astype('Int64')

  # Bersihkan label size dan gender
  df['size'] = df['size'].str.replace(r'^Size:\s*', '', regex=True)
  df['gender'] = df['gender'].str.replace(r'^Gender:\s*', '', regex=True)

  # Buang baris dengan nilai penting yang kosong dan yang duplikat
  df.dropna(subset=['price', 'rating', 'colors'], inplace=True)
  df.drop_duplicates(inplace=True)

  # Tambahkan kolom timestamp
  df['timestamp'] = pd.Timestamp.now().isoformat()

  print(f"📝✅ Jumlah data setelah transformasi: {len(df)}\n")
  return df
