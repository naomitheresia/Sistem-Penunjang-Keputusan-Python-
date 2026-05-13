"""
====================================================================
  PROGRAM AHP (Analytic Hierarchy Process)
  Penentuan Nilai Akhir Mahasiswa
  Berdasarkan Jurnal: "Penerapan Metode AHP dalam Penentuan
  Nilai Akhir Mahasiswa"
====================================================================
"""

import numpy as np

# ─────────────────────────────────────────────────────────────────
# KONSTANTA & DATA
# ─────────────────────────────────────────────────────────────────

# Nama kriteria
KRITERIA = ["Tugas", "UTS", "UAS", "Quiz", "Proyek Akhir"]

RI_TABLE = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90,
            5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}

# Matriks Perbandingan Berpasangan 
# Baris/Kolom: [Tugas, UTS, UAS, Quiz, Proyek Akhir]
MATRIKS_PERBANDINGAN = np.array([
    [1,     1/3,   1/5,   3,     7    ],   # Tugas
    [3,     1,     1/3,   5,     9    ],   # UTS
    [5,     3,     1,     7,     9    ],   # UAS
    [1/3,   1/5,   1/7,   1,     5    ],   # Quiz
    [1/7,   1/9,   1/9,   1/5,   1    ],   # Proyek Akhir
])

# Data nilai mahasiswa (dummy)
DATA_MAHASISWA = [
    {"nama": "Mahasiswa 1", "Tugas": 80, "UTS": 70, "UAS": 90, "Quiz": 85, "Proyek Akhir": 95},
    {"nama": "Mahasiswa 2", "Tugas": 75, "UTS": 80, "UAS": 85, "Quiz": 70, "Proyek Akhir": 88},
    {"nama": "Mahasiswa 3", "Tugas": 90, "UTS": 65, "UAS": 78, "Quiz": 92, "Proyek Akhir": 72},
    {"nama": "Mahasiswa 4", "Tugas": 85, "UTS": 88, "UAS": 92, "Quiz": 78, "Proyek Akhir": 80},
    {"nama": "Mahasiswa 5", "Tugas": 70, "UTS": 75, "UAS": 80, "Quiz": 65, "Proyek Akhir": 68},
]


# ─────────────────────────────────────────────────────────────────
# FUNGSI-FUNGSI AHP
# ─────────────────────────────────────────────────────────────────

def cetak_matriks(matriks, label_baris, label_kolom, judul, lebar_kolom=12):
    """Cetak matriks dengan format rapi"""
    n = len(label_baris)
    lebar_baris = max(len(l) for l in label_baris) + 2
    print(f"\n  {judul}")
    print("  " + "─" * (lebar_baris + lebar_kolom * n + 2))
    # Header kolom
    header = f"  {'Kriteria':<{lebar_baris}}"
    for k in label_kolom:
        header += f"{k:>{lebar_kolom}}"
    print(header)
    print("  " + "─" * (lebar_baris + lebar_kolom * n + 2))
    # Isi baris
    for i, baris_label in enumerate(label_baris):
        baris = f"  {baris_label:<{lebar_baris}}"
        for j in range(n):
            nilai = matriks[i][j]
            # Tampilkan pecahan jika < 1
            if nilai < 1 and nilai != 0:
                # Cari penyebut yang cocok (1/x)
                penyebut = round(1 / nilai)
                baris += f"{'1/'+str(penyebut):>{lebar_kolom}}"
            else:
                baris += f"{nilai:>{lebar_kolom}.4f}"
        print(baris)
    print("  " + "─" * (lebar_baris + lebar_kolom * n + 2))


def langkah1_tampilkan_matriks(matriks):
    """LANGKAH 1: Tampilkan matriks perbandingan berpasangan"""
    print("\n" + "━"*70)
    print("  LANGKAH 1 : MATRIKS PERBANDINGAN BERPASANGAN")
    print("━"*70)
    print("""
  Penjelasan:
  • Setiap kriteria dibandingkan satu sama lain menggunakan skala 1–9
  • Diagonal utama selalu = 1 (kriteria dibanding dirinya sendiri)
  • Bersifat RESIPROKAL: jika A vs B = 5, maka B vs A = 1/5
  • Skala: 1=sama penting, 3=sedikit lebih penting, 5=lebih penting,
           7=sangat penting, 9=mutlak sangat penting""")

    cetak_matriks(matriks, KRITERIA, KRITERIA,
                  "Matriks Perbandingan (nilai asli):", lebar_kolom=14)

    # Jumlah kolom
    jumlah_kolom = matriks.sum(axis=0)
    print(f"\n  Jumlah per kolom:")
    for i, k in enumerate(KRITERIA):
        print(f"    {k:<15} : {jumlah_kolom[i]:.4f}")

    return jumlah_kolom


def langkah2_normalisasi(matriks, jumlah_kolom):
    """LANGKAH 2: Normalisasi matriks"""
    print("\n" + "━"*70)
    print("  LANGKAH 2 : NORMALISASI MATRIKS")
    print("━"*70)
    print("""
  Cara: Setiap elemen dibagi dengan jumlah kolomnya
  Rumus: nilai_normalisasi[i][j] = matriks[i][j] / jumlah_kolom[j]
  Tujuan: Agar setiap kolom berjumlah = 1 (proporsional)""")

    n = len(KRITERIA)
    matriks_normal = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            matriks_normal[i][j] = matriks[i][j] / jumlah_kolom[j]

    cetak_matriks(matriks_normal, KRITERIA, KRITERIA,
                  "Matriks Ternormalisasi:", lebar_kolom=12)

    # Verifikasi: jumlah kolom harus = 1
    jumlah_kolom_normal = matriks_normal.sum(axis=0)
    print(f"\n  ✔ Verifikasi jumlah kolom (harus = 1.0):")
    for i, k in enumerate(KRITERIA):
        print(f"    {k:<15} : {jumlah_kolom_normal[i]:.4f}")

    return matriks_normal


def langkah3_vektor_prioritas(matriks_normal):
    """LANGKAH 3: Hitung vektor prioritas (bobot)"""
    print("\n" + "━"*70)
    print("  LANGKAH 3 : VEKTOR PRIORITAS (BOBOT KRITERIA)")
    print("━"*70)
    print("""
  Cara: Rata-rata setiap baris dari matriks ternormalisasi
  Rumus: bobot[i] = jumlah_baris[i] / jumlah_kriteria
  Ini adalah BOBOT kepentingan setiap kriteria""")

    n = len(KRITERIA)
    bobot = matriks_normal.mean(axis=1)

    print(f"\n  {'Kriteria':<20} {'Jumlah Baris':>14} {'÷ n='+str(n):>6} {'Bobot Prioritas':>17}")
    print(f"  {'─'*60}")
    for i, k in enumerate(KRITERIA):
        jumlah_baris = matriks_normal[i].sum()
        print(f"  {k:<20} {jumlah_baris:>14.4f} {' ':>6} {bobot[i]:>17.5f}")
    print(f"  {'─'*60}")
    print(f"  {'TOTAL':>42} {bobot.sum():>17.5f}  (harus = 1.0)")

    print(f"\n  📊 Interpretasi Bobot:")
    bobot_sorted = sorted(zip(KRITERIA, bobot), key=lambda x: x[1], reverse=True)
    for rank, (k, b) in enumerate(bobot_sorted, 1):
        bar = "█" * int(b * 50)
        print(f"  {rank}. {k:<16} {b:.5f}  {bar}")

    return bobot


def langkah4_uji_konsistensi(matriks, bobot):
    """LANGKAH 4: Uji konsistensi"""
    print("\n" + "━"*70)
    print("  LANGKAH 4 : UJI KONSISTENSI")
    print("━"*70)
    print("""
  Tujuan: Memastikan perbandingan kita logis dan tidak kontradiksi
  Langkah:
    1. Hitung Weighted Sum Vector = matriks × bobot
    2. Hitung Consistency Vector = weighted_sum / bobot
    3. Hitung λmax (lambda max) = rata-rata consistency vector
    4. Hitung CI = (λmax - n) / (n - 1)
    5. Hitung CR = CI / RI
    6. Jika CR ≤ 0.1 → KONSISTEN ✔""")

    n = len(KRITERIA)

    # Step 1: Weighted Sum Vector (Ax = matriks @ bobot)
    weighted_sum = matriks @ bobot
    print(f"\n  Step 1 - Weighted Sum Vector (matriks × bobot):")
    print(f"  {'Kriteria':<18} {'W. Sum':>10} {'÷ Bobot':>10} {'= C. Vector':>12}")
    print(f"  {'─'*52}")

    # Step 2: Consistency Vector
    consistency_vector = weighted_sum / bobot
    for i, k in enumerate(KRITERIA):
        print(f"  {k:<18} {weighted_sum[i]:>10.4f} {bobot[i]:>10.5f} {consistency_vector[i]:>12.4f}")

    # Step 3: λmax
    lambda_max = consistency_vector.mean()
    print(f"\n  Step 2 - λmax (rata-rata Consistency Vector):")
    print(f"    λmax = ({' + '.join([f'{v:.4f}' for v in consistency_vector])}) / {n}")
    print(f"    λmax = {consistency_vector.sum():.4f} / {n} = {lambda_max:.4f}")

    # Step 4: CI
    CI = (lambda_max - n) / (n - 1)
    print(f"\n  Step 3 - Consistency Index (CI):")
    print(f"    CI = (λmax - n) / (n - 1)")
    print(f"    CI = ({lambda_max:.4f} - {n}) / ({n} - 1)")
    print(f"    CI = {lambda_max - n:.4f} / {n-1} = {CI:.4f}")

    # Step 5: CR
    RI = RI_TABLE.get(n, 1.12)
    CR = CI / RI
    print(f"\n  Step 4 - Consistency Ratio (CR):")
    print(f"    RI untuk n={n} = {RI}")
    print(f"    CR = CI / RI = {CI:.4f} / {RI} = {CR:.4f}")

    # Step 6: Kesimpulan
    print(f"\n  {'═'*45}")
    if CR <= 0.1:
        print(f"  ✅ CR = {CR:.4f} ≤ 0.10  →  MATRIKS KONSISTEN")
        print(f"     Bobot kriteria dapat digunakan untuk perhitungan nilai akhir.")
    else:
        print(f"  ❌ CR = {CR:.4f} > 0.10  →  MATRIKS TIDAK KONSISTEN")
        print(f"     Perlu revisi matriks perbandingan berpasangan!")
    print(f"  {'═'*45}")

    return lambda_max, CI, CR


def langkah5_nilai_akhir(bobot):
    """LANGKAH 5: Hitung nilai akhir mahasiswa"""
    print("\n" + "━"*70)
    print("  LANGKAH 5 : PERHITUNGAN NILAI AKHIR MAHASISWA")
    print("━"*70)
    print(f"""
  Rumus:
  Nilai Akhir = (Tugas × {bobot[0]:.5f}) + (UTS × {bobot[1]:.5f}) +
                (UAS × {bobot[2]:.5f}) + (Quiz × {bobot[3]:.5f}) +
                (Proyek Akhir × {bobot[4]:.5f})""")

    hasil = []
    for mhs in DATA_MAHASISWA:
        print(f"\n  {'─'*65}")
        print(f"  🎓 {mhs['nama']}")
        print(f"  {'─'*65}")
        print(f"  {'Kriteria':<18} {'Nilai':>8} {'× Bobot':>10} {'= Kontribusi':>14}")
        print(f"  {'─'*52}")

        total = 0
        detail = []
        for i, k in enumerate(KRITERIA):
            nilai = mhs[k]
            kontribusi = nilai * bobot[i]
            total += kontribusi
            detail.append(kontribusi)
            print(f"  {k:<18} {nilai:>8.1f} × {bobot[i]:>8.5f} = {kontribusi:>12.4f}")

        # Normalisasi ke skala 0-100
        nilai_akhir_norm = (total / 100) * 100  # sudah dalam skala 100

        print(f"  {'─'*52}")
        print(f"  {'NILAI AKHIR':>42} = {total:>10.4f}")
        print(f"  {'(Normalisasi 0-100)':>42} = {total:.4f}")

        hasil.append({
            "nama": mhs["nama"],
            "nilai_akhir": total,
            "detail": {k: mhs[k] for k in KRITERIA}
        })

    return hasil


def langkah6_ranking(hasil):
    """LANGKAH 6: Ranking mahasiswa"""
    print("\n" + "━"*70)
    print("  LANGKAH 6 : RANKING MAHASISWA")
    print("━"*70)

    hasil_sorted = sorted(hasil, key=lambda x: x["nilai_akhir"], reverse=True)

    print(f"\n  {'Rank':<6} {'Nama Mahasiswa':<20} {'Tugas':>7} {'UTS':>7} {'UAS':>7} "
          f"{'Quiz':>7} {'Proyek':>8} {'Nilai Akhir':>13}")
    print(f"  {'─'*78}")

    grade_map = [(85, "A"), (75, "B"), (65, "C"), (55, "D"), (0, "E")]

    for rank, h in enumerate(hasil_sorted, 1):
        d = h["detail"]
        na = h["nilai_akhir"]
        grade = next(g for thr, g in grade_map if na >= thr)
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, "  ")
        print(f"  {str(rank)+'.':<4} {medal} {h['nama']:<17} "
              f"{d['Tugas']:>7.1f} {d['UTS']:>7.1f} {d['UAS']:>7.1f} "
              f"{d['Quiz']:>7.1f} {d['Proyek Akhir']:>8.1f} "
              f"  {na:>8.4f}  [{grade}]")

    print(f"  {'─'*78}")

    # Statistik
    nilai_list = [h["nilai_akhir"] for h in hasil]
    print(f"\n  📈 Statistik Kelas:")
    print(f"    Nilai Tertinggi : {max(nilai_list):.4f}  ({hasil_sorted[0]['nama']})")
    print(f"    Nilai Terendah  : {min(nilai_list):.4f}  ({hasil_sorted[-1]['nama']})")
    print(f"    Rata-rata Kelas : {sum(nilai_list)/len(nilai_list):.4f}")

    return hasil_sorted


# ─────────────────────────────────────────────────────────────────
# MAIN PROGRAM
# ─────────────────────────────────────────────────────────────────
def main():
    print("\n" + "╔" + "═"*68 + "╗")
    print("║" + " SISTEM PENDUKUNG KEPUTUSAN - METODE AHP".center(68) + "║")
    print("║" + " Penentuan Nilai Akhir Mahasiswa".center(68) + "║")
    print("╚" + "═"*68 + "╝")

    print("""
  Kriteria Penilaian yang digunakan:
    1. Tugas         → Pekerjaan rumah / latihan harian
    2. UTS           → Ujian Tengah Semester
    3. UAS           → Ujian Akhir Semester
    4. Quiz          → Kuis singkat
    5. Proyek Akhir  → Proyek/tugas besar akhir semester

  Skala Perbandingan AHP:
    1 = Sama penting          5 = Lebih penting
    3 = Sedikit lebih penting 7 = Sangat penting
    9 = Mutlak sangat penting (2,4,6,8 = nilai antara)
    """)

    # Jalankan semua langkah
    jumlah_kolom       = langkah1_tampilkan_matriks(MATRIKS_PERBANDINGAN)
    matriks_normal     = langkah2_normalisasi(MATRIKS_PERBANDINGAN, jumlah_kolom)
    bobot              = langkah3_vektor_prioritas(matriks_normal)
    lambda_max, CI, CR = langkah4_uji_konsistensi(MATRIKS_PERBANDINGAN, bobot)
    hasil              = langkah5_nilai_akhir(bobot)
    hasil_sorted       = langkah6_ranking(hasil)

    # Ringkasan akhir
    print("\n" + "╔" + "═"*68 + "╗")
    print("║" + " RINGKASAN HASIL AHP".center(68) + "║")
    print("╚" + "═"*68 + "╝")
    print(f"""
  Bobot Prioritas Kriteria (dari terpenting):
    1. UAS           : {bobot[2]:.5f}  ({bobot[2]*100:.2f}%)
    2. UTS           : {bobot[1]:.5f}  ({bobot[1]*100:.2f}%)
    3. Proyek Akhir  : {bobot[4]:.5f}  ({bobot[4]*100:.2f}%)
    4. Tugas         : {bobot[0]:.5f}  ({bobot[0]*100:.2f}%)
    5. Quiz          : {bobot[3]:.5f}  ({bobot[3]*100:.2f}%)

  Uji Konsistensi:
    λmax = {lambda_max:.4f}
    CI   = {CI:.4f}
    CR   = {CR:.4f}  {'✅ KONSISTEN (CR ≤ 0.10)' if CR <= 0.1 else '❌ TIDAK KONSISTEN'}

  Peringkat Akhir:""")

    for rank, h in enumerate(hasil_sorted, 1):
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"{rank}.")
        print(f"    {medal} {h['nama']:<20} → Nilai Akhir = {h['nilai_akhir']:.4f}")

    print("\n" + "="*70)
    print("  Program selesai.")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
