"""
Script untuk menjalankan Financial Analyst AI Chatbot
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Setup environment untuk aplikasi"""
    # Buat folder yang diperlukan
    folders = ['temp', 'uploads', 'logs']
    for folder in folders:
        Path(folder).mkdir(exist_ok=True)
        print(f"✅ Folder '{folder}' siap")
    
    # Load environment variables
    if Path('.env').exists():
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded")
    else:
        print("⚠️  File .env tidak ditemukan. Silakan copy dari .env.example")
        return False
    
    # Check API key
    if not os.getenv('GOOGLE_API_KEY'):
        print("❌ GOOGLE_API_KEY tidak ditemukan di .env")
        print("Silakan masukkan API key Google Gemini di file .env")
        return False
    
    print("✅ Google Gemini API Key terdeteksi")
    return True

def main():
    """Fungsi utama untuk menjalankan aplikasi"""
    print("🚀 Memulai Financial Analyst AI Chatbot...")
    print("=" * 50)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    print("=" * 50)
    print("✅ Setup selesai! Menjalankan aplikasi Streamlit...")
    print("🌐 Aplikasi akan terbuka di browser Anda")
    print("📱 Jika tidak terbuka otomatis, buka: http://localhost:8501")
    print("=" * 50)
    
    # Jalankan streamlit
    os.system("streamlit run app.py")

if __name__ == "__main__":
    main()