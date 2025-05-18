# import pandas as pd
# from google.oauth2.service_account import Credentials
# from googleapiclient.discovery import build
# from sqlalchemy import create_engine

# #! untuk simpan ke csv
# def export_to_csv(df, filename="products.csv"):
#   """Simpan data ke file CSV lokal"""
#   try:
#     df.to_csv(filename, index=False)
#     print(f"✔ Data berhasil disimpan ke file CSV: {filename}")
#   except Exception as e:
#     print(f"❌ Gagal menyimpan data ke CSV: {e}")

# #! untuk export ke google sheets
# def export_to_google_sheets(df, spreadsheet_id, range_name):
#   """Unggah data ke Google Sheets"""
#   try:
#     # Autentikasi menggunakan file kredensial
#     creds = Credentials.from_service_account_file('google-sheets-api.json')
#     service = build('sheets', 'v4', credentials=creds)
#     sheet = service.spreadsheets()

#     # Konversi DataFrame menjadi list of list
#     values = [df.columns.tolist()] + df.values.tolist()
#     body = {'values': values}

#     # Update ke Google Sheets
#     sheet.values().update(
#         spreadsheetId=spreadsheet_id,
#         range=range_name,
#         valueInputOption='RAW',
#         body=body
#     ).execute()

#     print(f"✔ Data berhasil diunggah ke Google Sheets: {spreadsheet_id}")
#   except Exception as e:
#     print(f"❌ Gagal mengunggah data ke Google Sheets: {e}")


# #! untuk export ke postgresql
# def export_to_postgresql(df, table_name='products'):
#   """Simpan data ke tabel PostgreSQL Docker dengan SQLAlchemy"""
#   try:
#     # Konfigurasi koneksi database
#     db_config = {
#         'username': 'postgres',
#         'password': '1234',
#         'host': 'localhost',
#         'port': '5432',
#         'database': 'db_etl'
#     }

#     # Buat engine SQLAlchemy
#     engine = create_engine(
#         f"postgresql+psycopg2://{db_config['username']}:{db_config['password']}@"
#         f"{db_config['host']}:{db_config['port']}/{db_config['database']}"
#     )

#     # Simpan DataFrame ke database
#     df.to_sql(table_name, engine, if_exists='replace', index=False)
#     print(f"✔ Data berhasil dimuat ke tabel PostgreSQL '{table_name}'")

#   except Exception as e:
#     print(f"❌ Gagal memuat data ke PostgreSQL: {e}")

import logging
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine
import json

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def simpan_ke_csv(df, filename="products.csv"):
  try:
    df.to_csv(filename, index=False)
    logging.info(f"Data berhasil disimpan ke file CSV: {filename}")
  except Exception as e:
    logging.error(f"Gagal menyimpan data ke CSV: {e}")

def simpan_ke_google_sheets(df, spreadsheet_id, range_name):
  if not spreadsheet_id or not range_name:
    logging.error("spreadsheet_id dan range_name harus diisi")
    return
  try:
    creds = Credentials.from_service_account_file('google-sheets-api.json')
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    values = [df.columns.tolist()] + df.values.tolist()
    body = {'values': values}

    sheet.values().update(
      spreadsheetId=spreadsheet_id,
      range=range_name,
      valueInputOption='RAW',
      body=body
    ).execute()

    logging.info(f"Data berhasil diunggah ke Google Sheets: {spreadsheet_id}")
  except Exception as e:
    logging.error(f"Gagal mengunggah data ke Google Sheets: {e}")

def simpan_ke_postgresql(df, table_name='products'):
  try:
    db_config = {
      'username': 'aria_keren2727',
      'password': 'obstraawdj29hi_DBS_k2e92wj',
      'host': 'localhost',
      'port': '5432',
      'database': 'products_db'
    }
    
    # Konversi semua kolom yang berisi dict menjadi JSON string
    for col in df.columns:
      if df[col].apply(lambda x: isinstance(x, dict)).any():
        df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, dict) else x)

    engine = create_engine(
      f"postgresql+psycopg2://{db_config['username']}:{db_config['password']}@"
      f"{db_config['host']}:{db_config['port']}/{db_config['database']}"
    )

    df.to_sql(table_name, engine, if_exists='replace', index=False)
    logging.info(f"Data berhasil dimuat ke tabel PostgreSQL '{table_name}'")
  except Exception as e:
    logging.error(f"Gagal memuat data ke PostgreSQL: {e}")
