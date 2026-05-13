"""
====================================================================
 "Penerapan Metode Profile Matching Dalam
  Pemilihan Program Keahlian Di Sekolah Menengah Kejuruan"
====================================================================
"""

# ─────────────────────────────────────────────
# 1. DATA SISWA (raw nilai rapor)
# ─────────────────────────────────────────────
data_siswa_raw = [
    {"id": 1,  "nama": "Adinda Shafira",              "MAT": 84,    "BIN": 89,    "ING": 85,    "SBD": 90,    "INF": 94,    "sikap": "SB", "minat": "MM"},
    {"id": 2,  "nama": "Hani Heryusi",                "MAT": 82,    "BIN": 89,    "ING": 84,    "SBD": 84,    "INF": 80,    "sikap": "B",  "minat": "MM"},
    {"id": 3,  "nama": "Muhammad Irsyad Syauki",      "MAT": 55,    "BIN": 72,    "ING": 83,    "SBD": 70,    "INF": 86,    "sikap": "B",  "minat": "TKJ"},
    {"id": 4,  "nama": "Nelza Avantin Yusuf",         "MAT": 88.72, "BIN": 86,    "ING": 88,    "SBD": 92,    "INF": 91,    "sikap": "SB", "minat": "MM"},
    {"id": 5,  "nama": "Raysha Nursyafa",             "MAT": 92,    "BIN": 91,    "ING": 97,    "SBD": 88,    "INF": 88,    "sikap": "SB", "minat": "MM"},
    {"id": 6,  "nama": "Yogas Saputra",               "MAT": 80,    "BIN": 87,    "ING": 80,    "SBD": 82,    "INF": 85,    "sikap": "B",  "minat": "TKJ"},
    {"id": 7,  "nama": "Bayu Ramadan",                "MAT": 89.6,  "BIN": 88.4,  "ING": 85.4,  "SBD": 87.2,  "INF": 85.4,  "sikap": "SB", "minat": "TKJ"},
    {"id": 8,  "nama": "Wildan Fadhillah",            "MAT": 85,    "BIN": 87,    "ING": 86,    "SBD": 86,    "INF": 84,    "sikap": "B",  "minat": "MM"},
    {"id": 9,  "nama": "Zia Zahira Garnetta",         "MAT": 78,    "BIN": 88,    "ING": 81,    "SBD": 76,    "INF": 83,    "sikap": "B",  "minat": "MM"},
    {"id": 10, "nama": "Sri Mulyani Dewi",            "MAT": 81,    "BIN": 90,    "ING": 85,    "SBD": 84,    "INF": 81,    "sikap": "B",  "minat": "MM"},
]

# ─────────────────────────────────────────────
# 2. TABEL KONVERSI NILAI
# ─────────────────────────────────────────────
def konversi_nilai(nilai):
    """Konversi nilai angka ke skala 1-4"""
    if nilai > 85:   return 4
    elif nilai >= 80: return 3
    elif nilai >= 76: return 2
    else:             return 1

def konversi_sikap(sikap):
    """Konversi nilai sikap ke skala 1-4"""
    tabel = {"SB": 4, "B": 3, "C": 2, "D": 1}
    return tabel.get(sikap, 1)

def konversi_minat(minat):
    """Konversi minat: MM=1, TKJ=2"""
    return 1 if minat == "MM" else 2

# ─────────────────────────────────────────────
# 3. TABEL PEMBOBOTAN GAP
# ─────────────────────────────────────────────
tabel_bobot = {
    0:  5.0,
    1:  4.5,
   -1:  4.0,
    2:  3.5,
   -2:  3.0,
    3:  2.5,
   -3:  2.0,
    4:  1.5,
   -4:  1.0,
}

def get_bobot(gap):
    """Ambil bobot dari tabel GAP. Jika tidak ada, nilai minimal."""
    return tabel_bobot.get(gap, 1.0)

# ─────────────────────────────────────────────
# 4. PROFIL MINIMAL (TARGET IDEAL)
# ─────────────────────────────────────────────
profil_minimal_MM  = {"MAT": 3, "BIN": 2, "ING": 4, "SBD": 4, "INF": 3, "sikap": 4, "minat": 1}
profil_minimal_TKJ = {"MAT": 4, "BIN": 3, "ING": 4, "SBD": 2, "INF": 4, "sikap": 4, "minat": 2}

# ─────────────────────────────────────────────
# 5. KRITERIA CF DAN SF PER PROGRAM
# ─────────────────────────────────────────────
cf_MM  = ["MAT", "ING", "SBD", "INF"]          # Core Factor MM
sf_MM  = ["BIN", "sikap", "minat"]             # Secondary Factor MM

cf_TKJ = ["MAT", "BIN", "ING", "INF"]          # Core Factor TKJ
sf_TKJ = ["SBD", "sikap", "minat"]             # Secondary Factor TKJ

# ─────────────────────────────────────────────
# 6. FUNGSI UTAMA PROFILE MATCHING
# ─────────────────────────────────────────────
def profile_matching(siswa_konversi, profil_minimal, cf_list, sf_list, nama_program):
    """
    Menghitung nilai total profile matching untuk satu program keahlian.
    
    Returns: dict berisi detail perhitungan
    """
    atribut = ["MAT", "BIN", "ING", "SBD", "INF", "sikap", "minat"]
    
    # Hitung GAP
    gap = {}
    for attr in atribut:
        gap[attr] = profil_minimal[attr] - siswa_konversi[attr]
    
    # Konversi GAP ke Bobot
    bobot = {}
    for attr in atribut:
        bobot[attr] = get_bobot(gap[attr])
    
    # Hitung NCF (rata-rata Core Factor)
    ncf = sum(bobot[attr] for attr in cf_list) / len(cf_list)
    
    # Hitung NSF (rata-rata Secondary Factor)
    nsf = sum(bobot[attr] for attr in sf_list) / len(sf_list)
    
    # Nilai Total = 60% NCF + 40% NSF
    total = round(0.6 * ncf + 0.4 * nsf, 2)
    
    return {
        "program": nama_program,
        "gap": gap,
        "bobot": bobot,
        "ncf": round(ncf, 2),
        "nsf": round(nsf, 2),
        "total": total
    }

# ─────────────────────────────────────────────
# 7. PROSES SEMUA SISWA
# ─────────────────────────────────────────────
def proses_semua_siswa(data_siswa_raw):
    hasil_akhir = []

    for s in data_siswa_raw:
        # Konversi nilai
        sk = {
            "MAT":   konversi_nilai(s["MAT"]),
            "BIN":   konversi_nilai(s["BIN"]),
            "ING":   konversi_nilai(s["ING"]),
            "SBD":   konversi_nilai(s["SBD"]),
            "INF":   konversi_nilai(s["INF"]),
            "sikap": konversi_sikap(s["sikap"]),
            "minat": konversi_minat(s["minat"]),
        }

        # Hitung untuk MM dan TKJ
        hasil_mm  = profile_matching(sk, profil_minimal_MM,  cf_MM,  sf_MM,  "Multimedia (MM)")
        hasil_tkj = profile_matching(sk, profil_minimal_TKJ, cf_TKJ, sf_TKJ, "Teknik Komputer Jaringan (TKJ)")

        # Rekomendasi
        rekomendasi = "Multimedia (MM)" if hasil_mm["total"] >= hasil_tkj["total"] else "Teknik Komputer Jaringan (TKJ)"

        hasil_akhir.append({
            "id": s["id"],
            "nama": s["nama"],
            "konversi": sk,
            "mm": hasil_mm,
            "tkj": hasil_tkj,
            "rekomendasi": rekomendasi,
        })

    return hasil_akhir

# ─────────────────────────────────────────────
# 8. TAMPILAN OUTPUT
# ─────────────────────────────────────────────
def cetak_detail_satu_siswa(hasil, nomor=1, total=1):
    """Cetak detail perhitungan satu siswa"""
    s = hasil
    sk = s["konversi"]
    mm = s["mm"]
    tkj = s["tkj"]

    print("=" * 70)
    print(f"  SISWA #{s['id']} : {s['nama']}")
    print("=" * 70)

    # Konversi nilai
    print("\n📋 LANGKAH 1 - KONVERSI NILAI")
    print(f"  {'Atribut':<12} {'Konversi':>10}")
    print(f"  {'-'*25}")
    label = {"MAT":"Matematika","BIN":"Bhs. Indonesia","ING":"Bhs. Inggris",
             "SBD":"Seni Budaya","INF":"Informatika","sikap":"Sikap","minat":"Minat"}
    for attr in ["MAT","BIN","ING","SBD","INF","sikap","minat"]:
        print(f"  {label[attr]:<18} {sk[attr]:>4}")

    # GAP dan Bobot MM
    print("\n📐 LANGKAH 2 & 3 - GAP & BOBOT (Program MM)")
    print(f"  {'Atribut':<14} {'Profil Min':>10} {'Nilai Siswa':>12} {'GAP':>6} {'Bobot':>7} {'CF/SF':>6}")
    print(f"  {'-'*57}")
    cf_sf_mm = {attr: "CF" for attr in cf_MM}
    cf_sf_mm.update({attr: "SF" for attr in sf_MM})
    for attr in ["MAT","BIN","ING","SBD","INF","sikap","minat"]:
        print(f"  {label[attr]:<14} {profil_minimal_MM[attr]:>10} {sk[attr]:>12} {mm['gap'][attr]:>6} {mm['bobot'][attr]:>7.1f} {cf_sf_mm[attr]:>6}")

    print(f"\n  ➤ NCF (Core Factor MM)      = ({' + '.join([str(mm['bobot'][a]) for a in cf_MM])}) / {len(cf_MM)} = {mm['ncf']}")
    print(f"  ➤ NSF (Secondary Factor MM) = ({' + '.join([str(mm['bobot'][a]) for a in sf_MM])}) / {len(sf_MM)} = {mm['nsf']}")
    print(f"  ➤ Total MM = 60% × {mm['ncf']} + 40% × {mm['nsf']} = \033[1m{mm['total']}\033[0m")

    # GAP dan Bobot TKJ
    print("\n📐 LANGKAH 2 & 3 - GAP & BOBOT (Program TKJ)")
    print(f"  {'Atribut':<14} {'Profil Min':>10} {'Nilai Siswa':>12} {'GAP':>6} {'Bobot':>7} {'CF/SF':>6}")
    print(f"  {'-'*57}")
    cf_sf_tkj = {attr: "CF" for attr in cf_TKJ}
    cf_sf_tkj.update({attr: "SF" for attr in sf_TKJ})
    for attr in ["MAT","BIN","ING","SBD","INF","sikap","minat"]:
        print(f"  {label[attr]:<14} {profil_minimal_TKJ[attr]:>10} {sk[attr]:>12} {tkj['gap'][attr]:>6} {tkj['bobot'][attr]:>7.1f} {cf_sf_tkj[attr]:>6}")

    print(f"\n  ➤ NCF (Core Factor TKJ)      = ({' + '.join([str(tkj['bobot'][a]) for a in cf_TKJ])}) / {len(cf_TKJ)} = {tkj['ncf']}")
    print(f"  ➤ NSF (Secondary Factor TKJ) = ({' + '.join([str(tkj['bobot'][a]) for a in sf_TKJ])}) / {len(sf_TKJ)} = {tkj['nsf']}")
    print(f"  ➤ Total TKJ = 60% × {tkj['ncf']} + 40% × {tkj['nsf']} = \033[1m{tkj['total']}\033[0m")

    # Keputusan
    print(f"\n🏆 REKOMENDASI")
    print(f"  Total MM  : {mm['total']}  {'◀ LEBIH TINGGI' if mm['total'] >= tkj['total'] else ''}")
    print(f"  Total TKJ : {tkj['total']}  {'◀ LEBIH TINGGI' if tkj['total'] > mm['total'] else ''}")
    rek_bersih = s['rekomendasi'].replace('\033[1m','').replace('\033[0m','')
    print(f"\n  ✅ Rekomendasi : \033[1;32m{rek_bersih}\033[0m")


def cetak_ringkasan(semua_hasil):
    """Cetak tabel ringkasan semua siswa"""
    print("\n" + "=" * 75)
    print("  TABEL RINGKASAN HASIL REKOMENDASI SEMUA SISWA")
    print("=" * 75)
    print(f"  {'No':<4} {'Nama Siswa':<30} {'Total MM':>9} {'Total TKJ':>10} {'Rekomendasi':<28}")
    print(f"  {'-'*73}")
    for h in semua_hasil:
        rek = h['rekomendasi'].replace('Teknik Komputer Jaringan (TKJ)', 'TKJ').replace('Multimedia (MM)', 'Multimedia (MM)')
        print(f"  {h['id']:<4} {h['nama']:<30} {h['mm']['total']:>9.1f} {h['tkj']['total']:>10.1f}   {rek}")

    # Statistik
    mm_count  = sum(1 for h in semua_hasil if "MM" in h["rekomendasi"] and "TKJ" not in h["rekomendasi"])
    tkj_count = len(semua_hasil) - mm_count
    print(f"\n  📊 Total Siswa    : {len(semua_hasil)}")
    print(f"  🎨 Rekomen MM     : {mm_count} siswa")
    print(f"  💻 Rekomen TKJ    : {tkj_count} siswa")


# ─────────────────────────────────────────────
# 9. MAIN - JALANKAN PROGRAM
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "╔" + "═"*68 + "╗")
    print("║" + " SISTEM PENDUKUNG KEPUTUSAN - PROFILE MATCHING".center(68) + "║")
    print("║" + " Rekomendasi Program Keahlian SMK".center(68) + "║")
    print("╚" + "═"*68 + "╝")

    print("\n📌 REFERENSI PROFIL MINIMAL")
    print(f"  MM  → MAT:{profil_minimal_MM['MAT']} BIN:{profil_minimal_MM['BIN']} ING:{profil_minimal_MM['ING']} SBD:{profil_minimal_MM['SBD']} INF:{profil_minimal_MM['INF']} Sikap:{profil_minimal_MM['sikap']} Minat:{profil_minimal_MM['minat']}")
    print(f"  TKJ → MAT:{profil_minimal_TKJ['MAT']} BIN:{profil_minimal_TKJ['BIN']} ING:{profil_minimal_TKJ['ING']} SBD:{profil_minimal_TKJ['SBD']} INF:{profil_minimal_TKJ['INF']} Sikap:{profil_minimal_TKJ['sikap']} Minat:{profil_minimal_TKJ['minat']}")

    print("\n📌 TABEL BOBOT GAP")
    print(f"  {'GAP':<8} {'Bobot':<8} {'Keterangan'}")
    print(f"  {'-'*55}")
    keterangan_gap = {
        0:  "Nilai sama persis dengan yang dibutuhkan",
        1:  "Siswa melebihi 1 tingkat dari yang dibutuhkan",
       -1:  "Siswa kurang 1 tingkat dari yang dibutuhkan",
        2:  "Siswa melebihi 2 tingkat",
       -2:  "Siswa kurang 2 tingkat",
        3:  "Siswa melebihi 3 tingkat",
       -3:  "Siswa kurang 3 tingkat",
    }
    for gap, bobot in sorted(tabel_bobot.items()):
        ket = keterangan_gap.get(gap, "")
        print(f"  {gap:<8} {bobot:<8} {ket}")

    # Proses
    semua_hasil = proses_semua_siswa(data_siswa_raw)

    # Detail hanya 3 siswa pertama sebagai contoh
    print("\n\n" + "━"*70)
    print("  DETAIL PERHITUNGAN (3 Siswa Pertama sebagai Contoh)")
    print("━"*70)
    for h in semua_hasil[:3]:
        cetak_detail_satu_siswa(h)
        print()

    # Ringkasan semua
    cetak_ringkasan(semua_hasil)
    print("\n" + "=" * 75)
    print("  Program selesai.")
    print("=" * 75 + "\n")
