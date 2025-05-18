import pandas as pd
from utils.extract import banyak_produk
from utils.transform import transformasi_produk
from utils.load import (
  simpan_ke_csv,
  simpan_ke_google_sheets,
  simpan_ke_postgresql
)

def try_step(step_name, func, *args, **kwargs):
  print(f"\n⏳ Mulai {step_name}...")
  try:
    result = func(*args, **kwargs)
    print(f"✅ {step_name} berhasil!")
    return result
  except Exception as e:
    print(f"❌ Gagal {step_name}: {e}")
    return None

def main():
  base_url = "https://fashion-studio.dicoding.dev/"

  # Step 1: Extract
  products = try_step("ekstraksi data produk", banyak_produk, base_url, 1000)
  if not products:
    print("⚠️ Tidak ada data produk yang berhasil diambil.")
    return

  # Step 2: Transform
  df = pd.DataFrame(products)
  df_clean = try_step("transformasi data produk", transformasi_produk, df)
  if df_clean is None or df_clean.empty:
    print("⚠️ Data produk setelah transformasi kosong.")
    return

  # Step 3: Load
  try_step("menyimpan ke file CSV", simpan_ke_csv, df_clean, "products.csv")

  try_step(
    "mengunggah ke Google Sheets",
    simpan_ke_google_sheets,
    df_clean,
    spreadsheet_id="1uyi9CDbI9_XxXMxzvaRDMsZqiuwVPcr2dIMj-2hK7XQ",
    range_name="Sheet1!A1"
  )

  try_step(
    "menyimpan ke PostgreSQL",
    simpan_ke_postgresql,
    df_clean,
    table_name='products'
  )

if __name__ == "__main__":
    main()
