````md
# SPK-Python

Repository ini berisi implementasi beberapa metode **Sistem Pendukung Keputusan (SPK)** menggunakan bahasa Python.

Project ini dibuat sebagai tugas implementasi metode SPK pada berbagai studi kasus nyata menggunakan metode pengambilan keputusan multikriteria, yaitu:

* TOPSIS
* Profile Matching
* AHP (Analytical Hierarchy Process)

---

# Daftar Metode

## 1. TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)

Studi kasus:

* Pemilihan bibit unggul buah mangga

Fitur:

* Matriks keputusan
* Normalisasi matriks
* Normalisasi terbobot
* Solusi ideal positif dan negatif
* Perhitungan jarak solusi ideal
* Nilai preferensi (C+)
* Ranking alternatif

File:

```text
TOPSIS/mangga.py
````

Output:

* Ranking bibit mangga terbaik berdasarkan kriteria yang telah ditentukan.

---

## 2. Profile Matching

Studi kasus:

* Rekomendasi program keahlian SMK (Multimedia dan TKJ)

Fitur:

* Konversi nilai
* Perhitungan GAP
* Pembobotan GAP
* Core Factor (CF)
* Secondary Factor (SF)
* Perhitungan nilai total
* Rekomendasi jurusan

File:

```text
Profile-Matching/profile_matching.py
```

Output:

* Rekomendasi program keahlian terbaik untuk setiap siswa.

---

## 3. AHP (Analytical Hierarchy Process)

Studi kasus:

* Penentuan nilai akhir mahasiswa

Fitur:

* Matriks perbandingan berpasangan
* Normalisasi matriks
* Perhitungan bobot prioritas
* Uji konsistensi (CI dan CR)
* Perhitungan nilai akhir mahasiswa
* Ranking mahasiswa

File:

```text
AHP/ahp_nilai_mahasiswa.py
```

Output:

* Ranking nilai akhir mahasiswa berdasarkan bobot kriteria AHP.

---

# Struktur Repository

```text
SPK-Python/
│
├── TOPSIS/
│   └── mangga.py
│
├── Profile-Matching/
│   └── profile_matching.py
│
├── AHP/
│   └── ahp_nilai_mahasiswa.py
│
└── README.md
```

---

# Tools dan Library

Project ini menggunakan:

* Python 3
* math
* numpy

Install library yang diperlukan:

```bash
pip install numpy
```

---

# Cara Menjalankan

## TOPSIS

```bash
cd TOPSIS
python mangga.py
```

## Profile Matching

```bash
cd Profile-Matching
python profile_matching.py
```

## AHP

```bash
cd AHP
python ahp_nilai_mahasiswa.py
```

---

# Penjelasan Singkat Metode

## TOPSIS

TOPSIS adalah metode pengambilan keputusan yang memilih alternatif terbaik berdasarkan jarak terhadap solusi ideal positif dan solusi ideal negatif.

---

## Profile Matching

Profile Matching digunakan untuk mencocokkan profil individu dengan profil ideal berdasarkan nilai GAP dan bobot tertentu.

---

## AHP

AHP digunakan untuk menentukan prioritas keputusan dengan membandingkan setiap kriteria secara berpasangan dan menghitung bobot prioritasnya.

---

# Tujuan Repository

Repository ini dibuat untuk:

* mempelajari implementasi metode SPK menggunakan Python,
* memahami konsep pengambilan keputusan multikriteria,
* menerapkan algoritma SPK pada studi kasus nyata,
* serta menjadi bahan pembelajaran dan presentasi mata kuliah.

---

# Author

Nama : Naomi Theresia. S
NPM : 2315061091
Mata Kuliah : Sistem Penunjang Keputusan

```
```
