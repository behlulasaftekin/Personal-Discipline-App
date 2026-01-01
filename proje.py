import customtkinter as ctk
import veritabani

class DersKarti(ctk.CTkFrame):
        def __init__(self, parent, ders_id, baslik, renk):
                super().__init__(parent, fg_color="transparent")
                self.pack(fill="x", pady=5)
                self.ders_id = ders_id
                self.acik_mi = False

                self.btn_ders = ctk.CTkButton(self, text=baslik, fg_color=renk, height=40, anchor="w", font=("Arial", 16, "bold"),command=self.ac_kapa)
                self.btn_ders.pack(fill="x")

                self.konu_frame = ctk.CTkFrame(self, fg_color="gray30")

                self.konulari_yukle()
        def konulari_yukle(self):
                for widget in self.konu_frame.winfo_children():
                       widget.destroy()
                konular = veritabani.konulari_getir(self.ders_id)

                if not konular:
                        lbl = ctk.CTkLabel(self.konu_frame, text="Henüz konu eklenmedi.", text_color="gray")
                        lbl.pack(pady=5)
                for konu in konular:
                        baslik = konu[0]
                        aciklama = konu[1]

                        satir = ctk.CTkLabel(self.konu_frame, text=f"•{baslik}: {aciklama}", anchor="w", justify="left")
                        satir.pack(fill="x", padx=20, pady=2)

        def ac_kapa(self):
                if self.acik_mi:
                        self.konu_frame.pack_forget()
                        self.acik_mi = False
                else:
                        self.konu_frame.pack(fill="x", padx=10, pady=5)
                        self.konulari_yukle()
                        self.acik_mi = True

def liste_guncelle():
        # 1. Eski kutucukları temizle
        for widget in scroll_dersler.winfo_children():
                widget.destroy()
        for widget in scroll_antrenman.winfo_children():
                widget.destroy()

        # 2. Verileri al
        kayitlar = veritabani.dersleri_getir()

        # 3. Verileri döngüye sok
        for kayit in kayitlar:
                # Veritabanından gelen veri sırası: (kategori, baslik, durum)

                d_id = kayit['kategori']
                d_kategori = kayit['baslik']
                d_baslik = kayit['durum']


                if d_kategori == "Ders":
                        DersKarti(scroll_dersler, d_id, d_baslik,"#2E8B57")
                elif d_kategori == "Antrenman":
                        DersKarti(scroll_antrenman, d_id, d_baslik,"#A52A2A")


def konu_ekle_kaydet():
        secilen_ders_str = ders_secim_menu.get()
        baslik = konu_baslik_girisi.get()
        aciklama = konu_aciklama_girisi.get()

        if baslik == "" or secilen_ders_str == "":
                return

        tum_dersler = veritabani.dersleri_getir()
        secilen_id = None
        for ders in tum_dersler:
                if ders[2] == secilen_ders_str:
                        secilen_id = ders[0]
                        break
        if secilen_id:
                veritabani.konu_ekle(secilen_id, baslik, aciklama)
                liste_guncelle()
                konu_pencere.destroy()


def konu_ekle_pencere_ac():
        global konu_pencere, ders_secim_menu, konu_baslik_girisi, konu_aciklama_girisi

        konu_pencere = ctk.CTkToplevel(app)
        konu_pencere.title("Derse Konu Ekle")
        konu_pencere.geometry("400x400")
        konu_pencere.attributes("-topmost", True)

        # 1. Mevcut Dersleri Listele
        dersler_data = veritabani.dersleri_getir()
        ders_isimleri = [d[2] for d in dersler_data]
        if not ders_isimleri:
                ctk.CTkLabel(konu_pencere, text="Önce Ana Ekranda Ders Oluşturmalısın!").pack(pady=20)
                return

        ctk.CTkLabel(konu_pencere, text="Hangi Derse Eklenecek?").pack(pady=5)
        ders_secim_menu = ctk.CTkOptionMenu(konu_pencere, values=ders_isimleri)
        ders_secim_menu.pack(pady=5)

        ctk.CTkLabel(konu_pencere, text="Konu Başlığı:").pack(pady=5)
        konu_baslik_girisi = ctk.CTkEntry(konu_pencere)
        konu_baslik_girisi.pack(pady=5)

        ctk.CTkLabel(konu_pencere, text="Açıklama / Not:").pack(pady=5)
        konu_aciklama_girisi = ctk.CTkTextbox(konu_pencere, height=100)
        konu_aciklama_girisi.pack(pady=5, padx=10)

        ctk.CTkButton(konu_pencere, text="Konuyu Kaydet", command=konu_ekle_kaydet).pack(pady=20)


# --- YENİ DERS EKLEME ---
def ders_ekle_kaydet():
        try:
                tur = tur_secimi.get()
                ad = ad_girisi.get()

                if ad:
                        veritabani.ders_ekle(tur, ad)
                        liste_guncelle()
                        ders_pencere.destroy()
        except Exception as e:
                print(f"Bir hata oluştu: {e}")


def ders_ekle_pencere_ac():

        global ders_pencere, tur_secimi, ad_girisi

        ders_pencere = ctk.CTkToplevel(app)
        ders_pencere.title("Yeni Ders/Spor Ekle")
        ders_pencere.geometry("300x250")
        ders_pencere.attributes("-topmost", True)

        ctk.CTkLabel(ders_pencere, text="Tür:").pack(pady=5)
        tur_secimi = ctk.CTkOptionMenu(ders_pencere, values=["Ders", "Antrenman"])
        tur_secimi.pack(pady=5)

        ctk.CTkLabel(ders_pencere, text="Adı:").pack(pady=5)
        ad_girisi = ctk.CTkEntry(ders_pencere)
        ad_girisi.pack(pady=5)

        ctk.CTkButton(ders_pencere, text="Kaydet", command=ders_ekle_kaydet).pack(pady=20)
#---ANA UYGULAMA---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

veritabani.baslat()

app = ctk.CTk()
app.title("Haftalık takip - Disipline")
app.geometry("1000x600")

app.grid_columnconfigure(0, weight=3)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

    #---SOL PANEL---
sol_panel = ctk.CTkFrame(app, corner_radius=15)
sol_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

baslik_frame = ctk.CTkFrame(sol_panel, fg_color="transparent")
baslik_frame.pack(padx=10, pady=10, fill="x")

baslik_lbl = ctk.CTkLabel(baslik_frame, text="Haftalık Görevler", font=("Arial", 20, "bold"))
baslik_lbl.pack(side="left", padx=10)

    #---EKLE BUTONU---
btn_ders_ekle = ctk.CTkButton(baslik_frame, text="Ders/Spor Ekle", width=120, command=ders_ekle_pencere_ac)
btn_ders_ekle.pack(side="right", padx=5)

btn_konu_ekle = ctk.CTkButton(baslik_frame, text="Konu ekle", width=120, command=konu_ekle_pencere_ac)
btn_konu_ekle.pack(side="right", padx=5)

    #---SEKMELER---
sekmeler = ctk.CTkTabview(sol_panel)
sekmeler.pack(fill="both", expand=True, padx=10, pady=10)

sekmeler.add("Dersler")
sekmeler.add("Antrenman")

    #---KAYDIRILABİLİR ALANLAR
scroll_dersler = ctk.CTkScrollableFrame(sekmeler.tab("Dersler"), fg_color="transparent")
scroll_dersler.pack(fill="both", expand=True)

scroll_antrenman = ctk.CTkScrollableFrame(sekmeler.tab("Antrenman"), fg_color="transparent")
scroll_antrenman.pack(fill="both", expand=True)

    #---SAĞ PANEL---
sag_panel = ctk.CTkFrame(app, corner_radius=15, fg_color="#2b2b2b")
sag_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

sag_baslik = ctk.CTkLabel(sag_panel, text="İstatistikler", font=("Arial", 16, "bold"))
sag_baslik.pack(pady=20)

liste_guncelle()

app.mainloop()

