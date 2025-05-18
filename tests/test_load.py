import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import simpan_ke_csv, simpan_ke_google_sheets, simpan_ke_postgresql

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

data = {
  'title': ['Produk A', 'Produk B'],
  'price': [10000, 20000]
}
df = pd.DataFrame(data)

def test_export_to_csv(tmp_path):
  filename = tmp_path / "test_products.csv" # Buat file sementara
  simpan_ke_csv(df, filename=str(filename)) # Simpan DataFrame ke CSV
  assert filename.exists() # Pastikan file CSV berhasil dibuat
  
  df_loaded = pd.read_csv(filename) # Baca kembali file CSV
  assert list(df_loaded.columns) == list(df.columns) # Pastikan kolom sama
  
  # Cek satu nilai agar yakin isinya sesuai
  assert df_loaded.loc[0, 'title'] == 'Produk A'
  assert df_loaded.loc[1, 'price'] == 20000
  print("\n✅ test_export_to_csv sukses, file CSV dibuat dan validasi data OK")
  
@patch('utils.load.build')  # patch function build dari googleapiclient.discovery
@patch('utils.load.Credentials.from_service_account_file')
def test_export_to_google_sheets(mock_creds, mock_build):
  mock_creds.return_value = MagicMock()
  mock_service = MagicMock()
  mock_build.return_value = mock_service
  mock_spreadsheets = mock_service.spreadsheets.return_value
  mock_spreadsheets.values.return_value.update.return_value.execute.return_value = None

  # panggil fungsi untuk mengunggah ke Google Sheets
  simpan_ke_google_sheets(df, spreadsheet_id="fake_id", range_name="Sheet1!A1")

  # Pastikan fungsi dipanggil dengan benar
  mock_creds.assert_called_once()
  mock_build.assert_called_once_with('sheets', 'v4', credentials=mock_creds.return_value)
  mock_spreadsheets.values.return_value.update.assert_called_once()
  print("✅ test_export_to_google_sheets sukses, Google Sheets API terpanggil dengan benar")
  
@patch('utils.load.create_engine')
def test_export_to_postgresql(mock_create_engine):
  mock_engine = MagicMock()
  mock_create_engine.return_value = mock_engine
  simpan_ke_postgresql(df, table_name='test_table')
  
  mock_create_engine.assert_called_once()
  mock_engine.connect.assert_not_called()  # to_sql handle koneksi sendiri
  print("✅ test_export_to_postgresql sukses, database mock engine terpanggil")