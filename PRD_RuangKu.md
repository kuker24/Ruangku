# PRD — RuangKu: Website Sistem Reservasi Ruang Kampus Digital

**Versi:** 1.0  
**Tanggal:** 7 April 2026  
**Status:** Draft

---

## 1. Ringkasan Produk

RuangKu adalah sistem reservasi ruang kampus berbasis web yang menggantikan proses manual (datang ke BAK, isi formulir kertas, tunggu konfirmasi verbal) menjadi proses digital yang bisa dilakukan dari HP dalam 3 menit. Website ini berfungsi sebagai **landing page penjelasan sistem sekaligus portal akses** bagi mahasiswa, pengurus UKM/BEM, dan staf BAK.

**Tagline:** *"Pinjam ruang kampus dalam 3 menit dari HP, tanpa antre di BAK, tanpa formulir kertas."*

---

## 2. Latar Belakang & Masalah

| Aspek | Detail |
|---|---|
| **Siapa** | Mahasiswa aktif, pengurus UKM/BEM, staf administrasi BAK |
| **Masalah** | Peminjaman ruang non-kelas (GSG, GOR, Lab, Kelas) masih manual — formulir fisik, konfirmasi verbal/WA pribadi, tidak ada data terpusat |
| **Dampak** | 30–60 menit waktu terbuang per pengajuan, bentrok jadwal ruang, kegiatan batal mendadak, staf BAK kewalahan menjawab pertanyaan berulang |
| **Urgensi** | Volume kegiatan mahasiswa meningkat, kapasitas staf BAK tidak bertambah |

---

## 3. Tujuan Website

1. **Menjelaskan cara kerja RuangKu** secara visual dan mudah dipahami oleh semua stakeholder (mahasiswa, UKM, staf BAK).
2. **Menjadi pintu masuk digital** — pengguna bisa langsung mengakses form reservasi dari website.
3. **Menampilkan status ketersediaan ruang** (integrasi dengan Google Sheets sebagai database).
4. **Membangun kepercayaan** terhadap sistem baru dengan menampilkan alur yang transparan.

---

## 4. Target Pengguna & Kebutuhan

### 4.1 Mahasiswa / Pengurus UKM
- Melihat ketersediaan ruang secara real-time
- Mengajukan reservasi tanpa datang ke BAK
- Mendapat konfirmasi status (Disetujui/Ditolak/Konflik)
- Proses cepat (< 3 menit)

### 4.2 Staf BAK (Admin)
- Dashboard untuk melihat semua pengajuan masuk
- Kemampuan update status booking (Disetujui/Ditolak/Konflik)
- Melihat kalender jadwal ruang harian/mingguan
- Mengurangi pertanyaan berulang via WA

---

## 5. Arsitektur Sistem

```
[Pengguna] 
    │
    ▼
[Website RuangKu] ─── Landing Page (penjelasan sistem)
    │                    ├── Hero: Tagline + CTA "Ajukan Reservasi"
    │                    ├── Cara Kerja (6 langkah visual)
    │                    ├── Ruang Tersedia (daftar ruang kampus)
    │                    ├── FAQ
    │                    └── Footer (kontak BAK)
    │
    ▼
[Google Form] ─── Input: Nama, NIM, UKM, Ruang, Tanggal, Jam, Keperluan, No. WA
    │
    ▼
[Google Sheets] ─── Database terpusat
    │                 ├── Tab "Antrian" (pengajuan baru)
    │                 ├── Tab "Jadwal" (yang sudah disetujui)
    │                 └── Kolom STATUS: Menunggu → Disetujui / Ditolak / Konflik
    │
    ▼
[Staf BAK] ─── Review di Sheets → Update status
    │
    ▼
[Notifikasi WA] ─── Manual atau via Apps Script auto-email
    │
    ▼
[Pengguna] ─── Datang sesuai jadwal yang dikonfirmasi
```

---

## 6. Fitur Website (Scope MVP)

### 6.1 Halaman Utama (Landing Page)

| Section | Konten | Prioritas |
|---|---|---|
| **Hero** | Tagline, deskripsi singkat masalah, tombol CTA "Ajukan Reservasi Sekarang" | P0 |
| **Masalah** | 3 pain point utama dengan ikon/ilustrasi | P0 |
| **Cara Kerja** | 6 langkah alur sistem (Scan QR → Isi Form → Sheets → Review → Notif → Gunakan Ruang) dengan visual step-by-step | P0 |
| **Daftar Ruang** | Kartu ruang yang tersedia (GSG, GOR, Lab, Kelas) dengan kapasitas & fasilitas | P1 |
| **Keuntungan** | Perbandingan sebelum vs sesudah RuangKu | P1 |
| **FAQ** | 5–7 pertanyaan umum | P1 |
| **Footer** | Kontak BAK, jam operasional, link sosmed kampus | P2 |

### 6.2 Fitur Interaktif

| Fitur | Deskripsi | Prioritas |
|---|---|---|
| **Tombol CTA → Google Form** | Redirect ke Google Form reservasi | P0 |
| **QR Code Display** | Menampilkan QR code yang bisa di-scan langsung | P1 |
| **Status Tracker** | Input NIM/nama → cek status pengajuan (embed dari Sheets) | P2 |
| **Kalender Ketersediaan** | View-only kalender ruang dari Google Sheets | P2 |

---

## 7. Alur Pengguna (User Flow)

### Flow Utama: Reservasi Ruang

```
1. Pengguna buka website / scan QR code
2. Lihat halaman utama → pahami cara kerja
3. Klik "Ajukan Reservasi Sekarang"
4. Redirect ke Google Form
5. Isi form (Nama, NIM, UKM, Ruang, Tanggal, Jam, Keperluan, No. WA)
6. Submit → Data masuk Google Sheets tab "Antrian"
7. Staf BAK review → update STATUS
8. Pengguna terima notifikasi via WA
9. Pengguna gunakan ruang sesuai jadwal
```

### Flow Admin: Review Reservasi

```
1. Staf BAK buka Google Sheets
2. Lihat tab "Antrian" — filter status "Menunggu"
3. Cek bentrok dengan tab "Jadwal"
4. Update kolom STATUS: Disetujui / Ditolak / Konflik
5. Kirim notif WA ke pengguna (manual atau Apps Script)
```

---

## 8. Komponen Teknologi

| Komponen | Teknologi | Biaya |
|---|---|---|
| Website Landing Page | HTML/CSS/JS (static site) atau React | Rp 0 (hosting gratis di GitHub Pages / Vercel) |
| Form Reservasi | Google Forms | Rp 0 |
| Database | Google Sheets | Rp 0 |
| QR Code | qr-code-generator.com | Rp 0 |
| Notifikasi | WhatsApp manual / Google Apps Script (auto-email) | Rp 0 |
| Domain (opsional) | .my.id atau subdomain kampus | Rp 0 – Rp 15.000/tahun |

**Total biaya operasional: Rp 0 (atau maks Rp 15.000/tahun jika pakai domain custom)**

---

## 9. Desain & Branding

| Elemen | Spesifikasi |
|---|---|
| **Nama** | RuangKu |
| **Warna Primer** | Biru kampus (#1E3A5F) — kepercayaan & profesional |
| **Warna Aksen** | Kuning/amber (#F59E0B) — energi & aksi |
| **Font** | Display: bold sans-serif · Body: clean readable sans |
| **Tone** | Friendly, langsung, efisien — bahasa mahasiswa |
| **Responsif** | Mobile-first (mayoritas akses dari HP) |

---

## 10. Metrik Keberhasilan

| Metrik | Target (3 bulan pertama) |
|---|---|
| Jumlah reservasi via sistem | ≥ 50 reservasi/bulan |
| Waktu rata-rata proses (submit → konfirmasi) | < 4 jam |
| Pengurangan antrian fisik di BAK | ≥ 70% |
| Insiden bentrok jadwal | Turun ≥ 50% |
| Skor kepuasan pengguna | ≥ 4.0 / 5.0 |

---

## 11. Risiko & Mitigasi

| Risiko | Mitigasi |
|---|---|
| Staf BAK enggan beralih ke digital | Demo langsung + SOP visual 1 halaman + pelatihan 15 menit |
| Mahasiswa tidak tahu sistem ada | QR code di mading & pintu ruang, sosialisasi via grup WA UKM |
| Double booking saat internet mati | Kolom cadangan manual di Sheets + SOP fallback kertas |
| Data palsu / penyalahgunaan | Validasi NIM di form + kolom verifikasi |
| Google Forms/Sheets down | Jarang terjadi; SOP fallback manual disiapkan |

---

## 12. Flywheel Effect

```
Lebih banyak mahasiswa submit via Form
        ↓
Data jadwal di Sheets makin lengkap & akurat
        ↓
Konflik jadwal makin jarang → kepercayaan naik
        ↓
BAK makin cepat konfirmasi
        ↓
Mahasiswa baru langsung pakai sistem ini
        ↓
(kembali ke atas — loop positif)
```

---

## 13. Timeline Pengembangan

| Minggu | Deliverable |
|---|---|
| **Minggu 1** | Desain UI website (Figma/langsung code) + Setup Google Form & Sheets |
| **Minggu 2** | Development website landing page + integrasi link Form |
| **Minggu 3** | Testing dengan 3–5 responden + iterasi berdasarkan feedback |
| **Minggu 4** | Deploy + cetak QR code + sosialisasi ke UKM & BAK |

---

## 14. Scope Masa Depan (Post-MVP)

- Dashboard admin berbasis web (bukan hanya Sheets)
- Notifikasi otomatis via WhatsApp API / Telegram Bot
- Kalender interaktif ketersediaan ruang real-time
- Sistem rating & review ruang oleh pengguna
- Integrasi dengan sistem akademik kampus (SIAKAD)
- Multi-kampus support

---

*Dokumen ini berstatus Draft Hipotesis — validasi lapangan wajib dilakukan sebelum finalisasi.*
