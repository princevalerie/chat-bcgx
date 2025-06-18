import streamlit as st
import os
import tempfile
from pathlib import Path
import io
from datetime import datetime
import pandas as pd
import json

# LangChain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import GoogleGenerativeAIEmbeddings
from langchain.llms import GoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document
from langchain.prompts import PromptTemplate

# Docling imports
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions, 
    TableFormerMode,
    AcceleratorOptions
)
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.utils.export import generate_multimodal_pages

# Page configuration
st.set_page_config(
    page_title="Financial Analyst AI Chatbot",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #2a5298;
    }
    .user-message {
        background-color: #f0f2f6;
        border-left-color: #ff6b6b;
    }
    .bot-message {
        background-color: #e8f4fd;
        border-left-color: #2a5298;
    }
    .sidebar-content {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

class FinancialAnalystBot:
    def __init__(self):
        self.gemini_api_key = None
        self.llm = None
        self.embeddings = None
        self.vectorstore = None
        self.conversation_chain = None
        self.doc_converter = self.initialize_converter()
        
    def initialize_converter(self):
        """Initialize the Docling document converter"""
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE
        pipeline_options.table_structure_options.do_cell_matching = True
        pipeline_options.accelerator_options = AcceleratorOptions(num_threads=4)
        pipeline_options.images_scale = 2.0
        pipeline_options.generate_page_images = True

        return DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options,
                    backend=PyPdfiumDocumentBackend
                )
            }
        )
    
    def setup_gemini(self, api_key):
        """Setup Gemini AI with API key"""
        try:
            self.gemini_api_key = api_key
            os.environ["GOOGLE_API_KEY"] = api_key
            
            self.llm = GoogleGenerativeAI(
                model="gemini-2.0-flash",
                temperature=0.1
            )
            
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001"
            )
            
            return True
        except Exception as e:
            st.error(f"Error setting up Gemini: {str(e)}")
            return False
    
    def extract_pdf_content(self, uploaded_file):
        """Extract content from PDF using Docling"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        try:
            # Convert the PDF - remove limitations
            conversion_result = self.doc_converter.convert(tmp_path)
            
            # Get markdown content
            markdown_content = conversion_result.document.export_to_markdown()
            
            # Extract tables and financial data
            financial_data = self.extract_financial_data(conversion_result)
            
            return markdown_content, financial_data
            
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
            return None, None
        finally:
            os.unlink(tmp_path)
    
    def extract_financial_data(self, conversion_result):
        """Extract specific financial data from the document"""
        financial_data = {
            "tables": [],
            "text_segments": []
        }
        
        try:
            for (content_text, content_md, content_dt, page_cells, page_segments, page) in generate_multimodal_pages(conversion_result):
                # Extract tables (financial statements, ratios, etc.)
                if page_cells:
                    financial_data["tables"].extend(page_cells)
                
                # Extract all text segments for comprehensive analysis
                for segment in page_segments:
                    financial_data["text_segments"].append({
                        "page": page.page_no,
                        "content": str(segment),
                        "type": "financial_data"
                    })
        
        except Exception as e:
            st.warning(f"Error extracting financial data: {str(e)}")
        
        return financial_data
    
    def create_vectorstore(self, documents):
        """Create vector store from documents"""
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=2000,
                chunk_overlap=400,
                length_function=len,
            )
            
            chunks = text_splitter.split_documents(documents)
            
            self.vectorstore = FAISS.from_documents(
                documents=chunks,
                embedding=self.embeddings
            )
            
            return True
        except Exception as e:
            st.error(f"Error creating vector store: {str(e)}")
            return False
    
    def setup_conversation_chain(self):
        """Setup the conversational retrieval chain"""
        try:
            # Custom prompt for financial analysis
            financial_prompt = PromptTemplate(
                input_variables=["context", "question", "chat_history"],
                template="""
                Anda adalah seorang Financial Analyst AI yang ahli dalam menganalisis dokumen keuangan perusahaan.
                
                Gunakan konteks berikut untuk menjawab pertanyaan tentang analisis keuangan:
                {context}
                
                Riwayat percakapan:
                {chat_history}
                
                Pertanyaan: {question}
                
                Berikan analisis yang mendalam dan profesional dengan:
                1. Analisis data keuangan yang relevan
                2. Interpretasi rasio dan metrik keuangan
                3. Insight tentang kinerja perusahaan
                4. Rekomendasi berdasarkan data
                5. Perbandingan dengan standar industri jika memungkinkan
                
                Jawaban harus dalam bahasa Indonesia dan gunakan format yang mudah dipahami.
                Jika data tidak cukup, jelaskan keterbatasan analisis.
                
                Jawaban:
                """
            )
            
            memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="answer"
            )
            
            self.conversation_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),
                memory=memory,
                return_source_documents=True,
                combine_docs_chain_kwargs={"prompt": financial_prompt}
            )
            
            return True
        except Exception as e:
            st.error(f"Error setting up conversation chain: {str(e)}")
            return False
    
    def get_response(self, question):
        """Get response from the chatbot"""
        try:
            response = self.conversation_chain({"question": question})
            return response["answer"], response.get("source_documents", [])
        except Exception as e:
            return f"Error: {str(e)}", []

def main():
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "bot" not in st.session_state:
        st.session_state.bot = FinancialAnalystBot()
    if "documents_processed" not in st.session_state:
        st.session_state.documents_processed = False
    if "financial_data" not in st.session_state:
        st.session_state.financial_data = None

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>💼 Financial Analyst AI Chatbot</h1>
        <p>Analisis Dokumen Keuangan Perusahaan dengan AI</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Pengaturan")
        
        # API Key input
        api_key = st.text_input(
            "Google Gemini API Key",
            type="password",
            help="Masukkan API Key Google Gemini Anda"
        )
        
        if api_key:
            if st.session_state.bot.setup_gemini(api_key):
                st.success("✅ Gemini AI siap digunakan!")
            
        st.markdown("---")
        
        # File upload
        st.markdown("## 📄 Upload Dokumen")
        uploaded_file = st.file_uploader(
            "Upload dokumen keuangan (PDF)",
            type=['pdf'],
            help="Upload laporan keuangan, annual report, atau dokumen keuangan lainnya"
        )
        
        if uploaded_file and api_key:
            if st.button("🔄 Proses Dokumen", type="primary"):
                with st.spinner("Memproses dokumen..."):
                    content, financial_data = st.session_state.bot.extract_pdf_content(uploaded_file)
                    
                    if content:
                        # Create documents for vector store
                        documents = [Document(page_content=content, metadata={"source": uploaded_file.name})]
                        
                        # Add financial data segments
                        if financial_data and financial_data["text_segments"]:
                            for segment in financial_data["text_segments"]:
                                documents.append(Document(
                                    page_content=segment["content"],
                                    metadata={
                                        "source": uploaded_file.name,
                                        "page": segment["page"],
                                        "type": segment["type"]
                                    }
                                ))
                        
                        if st.session_state.bot.create_vectorstore(documents):
                            if st.session_state.bot.setup_conversation_chain():
                                st.session_state.documents_processed = True
                                st.session_state.financial_data = financial_data
                                st.success("✅ Dokumen berhasil diproses!")
                                st.rerun()
        
        # Document info
        if st.session_state.documents_processed:
            st.markdown("---")
            st.markdown("## 📊 Info Dokumen")
            
            with st.container():
                st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
                st.write("✅ **Status:** Dokumen siap untuk analisis")
                
                if st.session_state.financial_data:
                    data = st.session_state.financial_data
                    st.write(f"📈 **Tabel:** {len(data.get('tables', []))}")
                    st.write(f"📝 **Segmen Keuangan:** {len(data.get('text_segments', []))}")
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Sample questions
        st.markdown("## 💡 Contoh Pertanyaan")
        sample_questions = [
            "Bagaimana kinerja keuangan perusahaan tahun ini?",
            "Berapa tingkat profitabilitas perusahaan?",
            "Analisis rasio likuiditas perusahaan",
            "Apa rekomendasi investasi berdasarkan laporan ini?",
            "Bandingkan kinerja dengan tahun sebelumnya"
        ]
        
        for i, question in enumerate(sample_questions):
            if st.button(f"❓ {question}", key=f"sample_{i}"):
                if st.session_state.documents_processed:
                    st.session_state.messages.append({"role": "user", "content": question})
                    st.rerun()

    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Chat messages
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>👤 Anda:</strong><br>
                        {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message bot-message">
                        <strong>🤖 Financial Analyst AI:</strong><br>
                        {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Chat input
        if st.session_state.documents_processed:
            user_question = st.chat_input("Tanyakan tentang analisis keuangan...")
            
            if user_question:
                # Add user message
                st.session_state.messages.append({"role": "user", "content": user_question})
                
                # Get bot response
                with st.spinner("Menganalisis..."):
                    response, sources = st.session_state.bot.get_response(user_question)
                
                # Add bot response
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                st.rerun()
        else:
            st.info("📤 Upload dan proses dokumen keuangan terlebih dahulu untuk memulai chat")
    
    with col2:
        if st.session_state.documents_processed and st.session_state.financial_data:
            st.markdown("## 📊 Quick Stats")
            
            data = st.session_state.financial_data
            
            # Metrics cards
            st.markdown(f"""
            <div class="metric-card">
                <h4>📈 Tabel Terdeteksi</h4>
                <h2>{len(data.get('tables', []))}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>📝 Segmen Keuangan</h4>
                <h2>{len(data.get('text_segments', []))}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Clear chat button
            if st.button("🗑️ Clear Chat", type="secondary"):
                st.session_state.messages = []
                st.rerun()

if __name__ == "__main__":
    main()
