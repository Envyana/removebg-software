# AI Background Remover GUI

Aplikasi GUI sederhana untuk menghapus background gambar menggunakan berbagai model AI. Dibangun dengan PyQt5 dan library rembg.

![Screenshot Aplikasi](screenshot.jpg)

## Fitur Utama
- Antarmuka minimalis dan mudah digunakan
- Support 15+ model AI berbeda
- Drag & drop gambar
- Auto-download model saat pertama kali digunakan
- Menyimpan hasil dalam format PNG
- Penskalaan gambar otomatis
- Pilihan model sesuai kebutuhan (umum, anime, pakaian, dll)

## Prasyarat
- Python 3.10 atau lebih baru
- RAM 4GB+ (rekomendasi 8GB untuk model besar)
- Ruang disk 500MB+ untuk penyimpanan model
- Sistem Operasi Windows/Linux/macOS

## Instalasi
1. Download atau clone repository ini
2. Jalankan `run.bat` (untuk Windows) dengan:
   - Klik 2x file `run.bat` atau
   - Buka CMD/Powershell dan ketik:
     ```bash
     run.bat
     ```

Isi `run.bat`:
```batch
@echo off
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python app.py
pause
