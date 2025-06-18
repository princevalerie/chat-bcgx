# 💼 Financial Analyst AI Chatbot

Aplikasi Streamlit dengan UI chatbot untuk analisis dokumen keuangan perusahaan menggunakan AI. Chatbot ini dapat mengekstrak dan menganalisis isi dokumen keuangan seperti laporan tahunan, laporan keuangan, dan dokumen finansial lainnya.

## 🚀 Fitur Utama

- **📄 Ekstraksi PDF Cerdas**: Menggunakan Docling untuk mengekstrak teks, tabel, dan gambar dari dokumen PDF
- **🤖 AI Financial Analyst**: Chatbot berbasis Gemini AI yang dapat menganalisis data keuangan
- **📊 Analisis Komprehensif**: Menganalisis semua aspek dokumen keuangan tanpa batasan
- **💬 Conversational AI**: Interface chat yang natural untuk bertanya tentang dokumen keuangan
- **📈 Ekstraksi Data Lengkap**: Mengekstrak semua halaman dokumen tanpa batasan
- **🔍 Retrieval Augmented Generation (RAG)**: Menggunakan LangChain untuk analisis kontekstual
- **🌐 Multi-bahasa**: Mendukung analisis dalam bahasa Indonesia dan Inggris

## 🛠️ Teknologi yang Digunakan

- **Streamlit**: Framework web app
- **Docling**: Ekstraksi dan pemrosesan dokumen PDF
- **LangChain**: Framework untuk aplikasi AI dan RAG
- **Google Gemini AI**: Model AI untuk analisis dan percakapan
- **FAISS**: Vector database untuk pencarian semantik
- **PyPdfium2**: Backend pemrosesan PDF

## 📋 Persyaratan Sistem

- Python 3.8+
- RAM minimal 4GB (8GB direkomendasikan)
- Google Gemini API Key

## 🚀 Instalasi

1. **Clone repository atau buat direktori project**
```bash
mkdir financial-chatbot
cd financial-chatbot
```

2. **Buat virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
```

Edit file `.env` dan masukkan Google Gemini API Key Anda:
```
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

5. **Jalankan aplikasi**
```bash
streamlit run app.py
```

## 🔑 Mendapatkan Google Gemini API Key

1. Kunjungi [Google AI Studio](https://makersuite.google.com/app/prompts/new_chat)
2. Login dengan akun Google Anda
3. Klik "Get API Key" dan buat API key baru
4. Copy API key dan masukkan ke file `.env`

## 📖 Cara Penggunaan

1. **Jalankan aplikasi** dengan `streamlit run app.py`
2. **Masukkan API Key** Google Gemini di sidebar
3. **Upload dokumen PDF** keuangan (laporan tahunan, laporan keuangan, dll.)
4. **Tunggu proses ekstraksi** dokumen selesai
5. **Mulai bertanya** tentang analisis keuangan melalui chat interface

## 💡 Contoh Pertanyaan

- "Bagaimana kinerja keuangan perusahaan tahun ini?"
- "Berapa tingkat profitabilitas perusahaan?"
- "Analisis rasio likuiditas perusahaan"
- "Apa rekomendasi investasi berdasarkan laporan ini?"
- "Bandingkan kinerja dengan tahun sebelumnya"
- "Berapa tingkat leverage keuangan perusahaan?"
- "Analisis efisiensi operasional perusahaan"
- "Bagaimana posisi kas perusahaan?"

## 📁 Struktur Project

```
financial-chatbot/
│
├── app.py                 # Aplikasi Streamlit utama
├── requirements.txt       # Dependencies
├── .env.example          # Template environment variables
├── .env                  # Environment variables (buat sendiri)
├── README.md             # Dokumentasi
│
├── temp/                 # Folder temporary (otomatis dibuat)
├── uploads/              # Folder upload (otomatis dibuat)
└── logs/                 # Folder logs (otomatis dibuat)
```

## 🔧 Konfigurasi

Aplikasi ini menggunakan konfigurasi default yang optimal:

- **Chunk size**: 2000 karakter untuk analisis yang lebih komprehensif
- **Temperature**: 0.1 untuk respons yang lebih konsisten
- **Retrieval documents**: 5 dokumen untuk konteks yang lebih luas
- **Tanpa batasan halaman**: Mengekstrak semua halaman dokumen
- **Tanpa batasan output**: Gemini AI dapat memberikan respons lengkap

## 🚨 Troubleshooting

### Error "Module not found"
```bash
pip install -r requirements.txt
```

### Error "API Key not found"
Pastikan file `.env` sudah dibuat dan berisi API key yang valid:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

### Error "PDF processing failed"
- Pastikan file PDF tidak corrupt
- Coba dengan file PDF yang lebih kecil terlebih dahulu
- Pastikan file PDF berisi teks (bukan hanya gambar)

### Performance lambat
- Gunakan file PDF dengan ukuran < 50MB
- Pastikan RAM cukup (minimal 4GB)
- Tutup aplikasi lain yang tidak perlu

## 📝 Catatan Penting

- **API Usage**: Aplikasi ini menggunakan Google Gemini API yang berbayar setelah quota gratis habis
- **Privacy**: Dokumen diproses secara lokal, tetapi konten dikirim ke API Gemini untuk analisis
- **Akurasi**: Hasil analisis bergantung pada kualitas dokumen PDF dan kemampuan AI
- **Bahasa**: Aplikasi mendukung dokumen dalam bahasa Indonesia dan Inggris

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:
1. Fork repository
2. Buat branch feature (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Buat Pull Request

## 📄 Lisensi

Project ini menggunakan lisensi MIT. Lihat file `LICENSE` untuk detail.

## 📧 Support

Jika mengalami masalah atau memiliki pertanyaan, silakan buat issue di repository atau hubungi developer.

---

**Dibuat dengan ❤️ menggunakan Streamlit, LangChain, dan Google Gemini AI**