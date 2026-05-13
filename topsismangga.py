"""
=============================================================
  PROGRAM TOPSIS - Pemilihan Bibit Unggul Buah Mangga
  Studi Kasus: Jurnal J-SAKTI Vol.5 No.1, Maret 2021
  Oleh: Didik Siswanto, Lasri Nijal, Pandu Pratama Putra
=============================================================

PENJELASAN SINGKAT TOPSIS:
  TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)
  adalah metode pengambilan keputusan multi-kriteria.
  
  Prinsip: Pilih alternatif yang PALING DEKAT dengan solusi ideal positif
           dan PALING JAUH dari solusi ideal negatif.

LANGKAH-LANGKAH:
  1. Buat matriks keputusan
  2. Normalisasi matriks
  3. Normalisasi terbobot
  4. Tentukan solusi ideal positif (A+) dan negatif (A-)
  5. Hitung jarak ke solusi ideal
  6. Hitung nilai preferensi (C+)
  7. Ranking alternatif
"""

import math

# ─────────────────────────────────────────────
#  DATA INPUT
# ─────────────────────────────────────────────

# Nama alternatif (jenis bibit mangga)
alternatif = ["Golek", "Harum Manis", "Madu", "Bengkulu", "Apel"]

# Nama kriteria
kriteria = ["Daun", "Batang", "Cabang", "Jml/Malai",
            "Warna Batang", "Rasa Buah", "Vegetatif", "Hama"]

# Bobot setiap kriteria (W)
bobot = [3, 4, 3, 2, 2, 3, 5, 4]

# Tipe kriteria: "benefit" = makin besar makin baik
#                "cost"    = makin kecil makin baik
tipe = ["benefit"] * 8  # Semua benefit di studi kasus ini

# Matriks keputusan: baris = alternatif, kolom = kriteria
# Urutan: Daun, Batang, Cabang, Jml/Malai, Warna Batang, Rasa Buah, Vegetatif, Hama
matriks = [
    [3, 3, 3, 5, 3, 5, 3, 5],  # Golek
    [3, 5, 3, 3, 3, 3, 5, 5],  # Harum Manis
    [3, 1, 3, 3, 3, 5, 5, 5],  # Madu
    [3, 3, 3, 5, 3, 3, 3, 5],  # Bengkulu
    [5, 3, 3, 3, 5, 3, 3, 3],  # Apel
]

n_alt = len(alternatif)   # jumlah alternatif
n_kri = len(kriteria)     # jumlah kriteria


# ─────────────────────────────────────────────
#  FUNGSI PEMBANTU
# ─────────────────────────────────────────────

def cetak_tabel(judul, header, baris_data, baris_label):
    """Fungsi untuk mencetak tabel terformat di terminal."""
    print(f"\n{'='*70}")
    print(f"  {judul}")
    print(f"{'='*70}")
    # Header
    lebar_label = 15
    lebar_col = 11
    print(f"{'Alternatif':<{lebar_label}}", end="")
    for h in header:
        print(f"{h:>{lebar_col}}", end="")
    print()
    print("-" * 70)
    # Isi baris
    for i, label in enumerate(baris_label):
        print(f"{label:<{lebar_label}}", end="")
        for val in baris_data[i]:
            if isinstance(val, float):
                print(f"{val:>{lebar_col}.6f}", end="")
            else:
                print(f"{val:>{lebar_col}}", end="")
        print()
    print("=" * 70)


# ─────────────────────────────────────────────
#  LANGKAH 1: TAMPILKAN MATRIKS KEPUTUSAN
# ─────────────────────────────────────────────

print("\n" + "█"*70)
print("  PROGRAM TOPSIS - PEMILIHAN BIBIT UNGGUL BUAH MANGGA")
print("█"*70)

cetak_tabel(
    "LANGKAH 1: MATRIKS KEPUTUSAN (Data Awal)",
    kriteria,
    matriks,
    alternatif
)
print("\n  ➤ Matriks ini berisi nilai setiap alternatif pada setiap kriteria.")
print("    Nilai didapat dari penilaian/scoring terhadap bibit mangga.")


# ─────────────────────────────────────────────
#  LANGKAH 2: NORMALISASI MATRIKS
# ─────────────────────────────────────────────
# Rumus: r_ij = x_ij / sqrt(Σ x_ij²)
# Tujuan: menyamakan skala semua kriteria (0 sampai 1)

print("\n\n" + "─"*70)
print("  LANGKAH 2: NORMALISASI MATRIKS")
print("─"*70)
print("""
  Rumus: r_ij = x_ij / √(Σ x_ij²)

  Caranya:
  1. Untuk tiap kolom (kriteria), hitung akar dari jumlah kuadrat semua nilai
  2. Bagi setiap nilai dengan hasil akar tadi
  
  Contoh kolom 'Batang':
    Nilai: Golek=3, HarumManis=5, Madu=1, Bengkulu=3, Apel=3
    Jumlah kuadrat: 3²+5²+1²+3²+3² = 9+25+1+9+9 = 53
    Akar: √53 ≈ 7.2801
    Normalisasi Golek: 3/7.2801 ≈ 0.4120
""")

# Hitung akar jumlah kuadrat per kolom
akar_jumlah_kuadrat = []
for j in range(n_kri):
    total = sum(matriks[i][j] ** 2 for i in range(n_alt))
    akar_jumlah_kuadrat.append(math.sqrt(total))

print("  Akar Jumlah Kuadrat per Kriteria:")
for j in range(n_kri):
    print(f"    {kriteria[j]:<15}: √{sum(matriks[i][j]**2 for i in range(n_alt))} = {akar_jumlah_kuadrat[j]:.6f}")

# Hitung matriks ternormalisasi
matriks_norm = []
for i in range(n_alt):
    baris = []
    for j in range(n_kri):
        r = matriks[i][j] / akar_jumlah_kuadrat[j]
        baris.append(r)
    matriks_norm.append(baris)

cetak_tabel(
    "Hasil Matriks Ternormalisasi (R)",
    kriteria,
    matriks_norm,
    alternatif
)


# ─────────────────────────────────────────────
#  LANGKAH 3: NORMALISASI TERBOBOT
# ─────────────────────────────────────────────
# Rumus: v_ij = w_j × r_ij
# Tujuan: kriteria yang lebih penting mendapat pengaruh lebih besar

print("\n\n" + "─"*70)
print("  LANGKAH 3: NORMALISASI TERBOBOT")
print("─"*70)
print("""
  Rumus: v_ij = w_j × r_ij
  
  Bobot mencerminkan tingkat kepentingan kriteria.
  Semakin besar bobot = semakin penting kriteria tersebut.
  
  Contoh 'Daun' Golek:
    w1 = 3, r_Golek_Daun = nilai normalisasi
    v = 3 × r_Golek_Daun
""")

print(f"  Bobot Kriteria:")
for j in range(n_kri):
    print(f"    W{j+1} {kriteria[j]:<15} = {bobot[j]}")

matriks_bobot = []
for i in range(n_alt):
    baris = []
    for j in range(n_kri):
        v = bobot[j] * matriks_norm[i][j]
        baris.append(v)
    matriks_bobot.append(baris)

cetak_tabel(
    "Hasil Matriks Ternormalisasi Terbobot (V)",
    kriteria,
    matriks_bobot,
    alternatif
)


# ─────────────────────────────────────────────
#  LANGKAH 4: SOLUSI IDEAL POSITIF & NEGATIF
# ─────────────────────────────────────────────
# A+ = nilai terbaik di setiap kolom
#   → untuk kriteria benefit: nilai MAX
#   → untuk kriteria cost: nilai MIN
# A- = nilai terburuk di setiap kolom
#   → untuk kriteria benefit: nilai MIN
#   → untuk kriteria cost: nilai MAX

print("\n\n" + "─"*70)
print("  LANGKAH 4: SOLUSI IDEAL POSITIF (A+) DAN NEGATIF (A-)")
print("─"*70)
print("""
  A+ (Ideal Positif)  = nilai TERBAIK tiap kriteria
  A- (Ideal Negatif)  = nilai TERBURUK tiap kriteria
  
  Karena semua kriteria bertipe "benefit" (makin besar makin baik):
    A+ = nilai MAKSIMUM tiap kolom
    A- = nilai MINIMUM tiap kolom
""")

A_plus  = []
A_minus = []

for j in range(n_kri):
    kolom = [matriks_bobot[i][j] for i in range(n_alt)]
    if tipe[j] == "benefit":
        A_plus.append(max(kolom))
        A_minus.append(min(kolom))
    else:  # cost
        A_plus.append(min(kolom))
        A_minus.append(max(kolom))

print("  Solusi Ideal Positif (A+):")
for j in range(n_kri):
    print(f"    {kriteria[j]:<15} A+ = {A_plus[j]:.6f}")

print("\n  Solusi Ideal Negatif (A-):")
for j in range(n_kri):
    print(f"    {kriteria[j]:<15} A- = {A_minus[j]:.6f}")


# ─────────────────────────────────────────────
#  LANGKAH 5: HITUNG JARAK KE SOLUSI IDEAL
# ─────────────────────────────────────────────
# D+_i = sqrt(Σ (v_ij - A+_j)²)  ← jarak ke ideal POSITIF
# D-_i = sqrt(Σ (v_ij - A-_j)²)  ← jarak ke ideal NEGATIF

print("\n\n" + "─"*70)
print("  LANGKAH 5: JARAK KE SOLUSI IDEAL (Separasi)")
print("─"*70)
print("""
  D+_i = √Σ(v_ij - A+_j)²   ← Jarak ke ideal POSITIF (makin kecil makin baik)
  D-_i = √Σ(v_ij - A-_j)²   ← Jarak ke ideal NEGATIF (makin besar makin baik)
""")

D_plus  = []
D_minus = []

for i in range(n_alt):
    # Hitung D+
    total_plus = sum((matriks_bobot[i][j] - A_plus[j]) ** 2 for j in range(n_kri))
    dp = math.sqrt(total_plus)
    D_plus.append(dp)

    # Hitung D-
    total_minus = sum((matriks_bobot[i][j] - A_minus[j]) ** 2 for j in range(n_kri))
    dm = math.sqrt(total_minus)
    D_minus.append(dm)

print(f"  {'Alternatif':<15} {'D+ (ke ideal+)':>18} {'D- (ke ideal-)':>18}")
print("  " + "-"*52)
for i in range(n_alt):
    print(f"  {alternatif[i]:<15} {D_plus[i]:>18.8f} {D_minus[i]:>18.8f}")


# ─────────────────────────────────────────────
#  LANGKAH 6: NILAI PREFERENSI (C+)
# ─────────────────────────────────────────────
# C+_i = D-_i / (D+_i + D-_i)
# Nilai antara 0–1. Semakin mendekati 1 = semakin baik

print("\n\n" + "─"*70)
print("  LANGKAH 6: NILAI PREFERENSI (C+)")
print("─"*70)
print("""
  Rumus: C+_i = D-_i / (D+_i + D-_i)
  
  Interpretasi:
    C+ mendekati 1 → alternatif sangat baik (dekat ideal positif)
    C+ mendekati 0 → alternatif sangat buruk (dekat ideal negatif)
""")

C_plus = []
for i in range(n_alt):
    c = D_minus[i] / (D_plus[i] + D_minus[i])
    C_plus.append(c)

print(f"  {'Alternatif':<15} {'D+':<12} {'D-':<12} {'C+ (Preferensi)':>18}")
print("  " + "-"*58)
for i in range(n_alt):
    print(f"  {alternatif[i]:<15} {D_plus[i]:<12.6f} {D_minus[i]:<12.6f} {C_plus[i]:>18.6f}")


# ─────────────────────────────────────────────
#  LANGKAH 7: RANKING
# ─────────────────────────────────────────────

print("\n\n" + "─"*70)
print("  LANGKAH 7: RANKING AKHIR (Dari Nilai C+ Terbesar ke Terkecil)")
print("─"*70)

# Buat daftar (nama, nilai C+) lalu sort descending
hasil = sorted(zip(alternatif, C_plus), key=lambda x: x[1], reverse=True)

print(f"\n  {'Rank':<6} {'Alternatif':<18} {'Nilai C+':>12}  Keterangan")
print("  " + "-"*55)
for rank, (nama, nilai) in enumerate(hasil, 1):
    ket = "← 🏆 TERBAIK!" if rank == 1 else ""
    print(f"  {rank:<6} {nama:<18} {nilai:>12.6f}  {ket}")


# ─────────────────────────────────────────────
#  KESIMPULAN
# ─────────────────────────────────────────────

print("\n\n" + "█"*70)
print("  KESIMPULAN")
print("█"*70)
bibit_terbaik = hasil[0][0]
nilai_terbaik = hasil[0][1]
print(f"""
  Berdasarkan perhitungan TOPSIS dengan 5 alternatif bibit mangga
  dan 8 kriteria penilaian, diperoleh hasil:

  ✅ Bibit terbaik adalah: {bibit_terbaik}
     Nilai C+             : {nilai_terbaik:.6f}

  Artinya bibit {bibit_terbaik} adalah yang paling mendekati
  solusi ideal positif (terbaik) dan paling jauh dari solusi
  ideal negatif (terburuk) berdasarkan kriteria yang ditetapkan.

  Hasil ini SESUAI dengan jurnal yang menyatakan:
  "Mangga Harum Manis menjadi solusi yang paling mendekati
   dengan nilai C+ = 0.67707"
""")
print("█"*70 + "\n")