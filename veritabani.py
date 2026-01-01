import sqlite3

# Veritabanı dosyasının adı
DB_NAME = "kisisel_gelisim.db"

def baslat():
    """Tabloyu oluşturur."""
    con = sqlite3.connect(DB_NAME)
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS gorevler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kategori TEXT,
            baslik TEXT,
            durum INTEGER DEFAULT 0
        )""")


    # ders_id: Hangi derse ait olduğunu tutar
    cursor.execute("""CREATE TABLE IF NOT EXISTS konular (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ders_id INTEGER,
            konu_basligi TEXT,
            aciklama TEXT,
            durum INTEGER DEFAULT 0,
            FOREIGN KEY(ders_id) REFERENCES gorevler(id)
        )""")

    con.commit()
    con.close()

def ders_ekle(kategori, baslik):
    """Yeni görev ekler."""
    con = sqlite3.connect(DB_NAME)
    cursor = con.cursor()
    cursor.execute("INSERT INTO gorevler (kategori, baslik) VALUES (?, ?)", (kategori, baslik))
    con.commit()
    con.close()

def dersleri_getir():
    """Tüm görevleri liste olarak geri döndürür."""
    con = sqlite3.connect(DB_NAME)
    con.row_factory = dict_factory
    cursor = con.cursor()
    cursor.execute("SELECT kategori, baslik, durum FROM gorevler")
    veriler = cursor.fetchall()
    con.close()
    return veriler

def konu_ekle(ders_id, konu_basligi, aciklama):
    con = sqlite3.connect(DB_NAME)
    cursor = con.cursor()
    cursor.execute("INSERT INTO konular (ders_id, konu_basligi, aciklama) VALUES (?, ?, ?)", (ders_id, konu_basligi, aciklama))
    con.commit()
    con.close()

def konulari_getir(ders_id):
    con = sqlite3.connect(DB_NAME)
    con.row_factory = dict_factory
    cursor = con.cursor()
    cursor.execute("SELECT konu_basligi, aciklama, durum FROM konular where ders_id = ?", (ders_id,))
    veriler = cursor.fetchall()
    con.close()
    return veriler

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
