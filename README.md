# Submission ETL Dicoding by Nur Aria Hibnastiar

merupakan tugas akhir dari kelas **Belajar Fundamental Pemrosesan Data** yang membahas tentang ETL (Extract Transform dan Load)


Berikut page yang saya lakukan proses ETL
[Webstie Scraping](https://fashion-studio.dicoding.dev/)

Data yang saya ambil 1000 dan setelah tahap transform menjadi 867

# Struktur Folder

```
  root/
  ├── env/ # virtual environtment 
  ├── tests/ # folder untuk testing terhadap file di folder utils
      └── test_extract.py
      └── test_transform.py
      └── test_load.py
  ├── utils/ # folder utama ETL nya
      └── extract.py
      └── transform.py
      └── load.py
  ├── main.py # folder untuk penggabungan ETL pada folder utils
  ├── requirements.txt
  ├── google-sheets-api.json # sensitif key jadi saya private

```


# Cara Running

## 1. masuk ke env (Pakek Bash / Poweshel)
```bash
source env/Script/activate
```
## 2. install depedensi yang ada di requirements.txt jalankan perintah ini
```bash
pip install -r requirements.txt
```
## 3. Jalankan perintah ini jika menggunakan postgre docker
```bash
# ini untuk merunning server postgree
docker compose up -d

# check apakah container sudah active dengan
docker ps
```
## 4. Lalu jalankan perintah ini
```
python main.py
```

# Hasil Testing

```
Name                      Stmts   Miss  Cover
---------------------------------------------
tests\test_extract.py        65      2    97%
tests\test_load.py           37      0   100%
tests\test_transform.py      41      0   100%
utils\extract.py             45      6    87%
utils\load.py                37      9    76%
utils\transform.py           26      1    96%
---------------------------------------------
TOTAL                       251     18    93%
```

Dengan hasil testing **coverage 93%** maka masuk terdalam kriteria **Advanced**

