from api_groq import api_call
import streamlit as st
import json
import sqlite3
import base64
from datetime import datetime
from pathlib import Path
import time
import os
import pandas as pd
import io


# ==================== CONFIGURAZIONE ====================
st.set_page_config(
    page_title="Consta AI - Query Interface",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================== COSTANTI ====================
class Config:
    VIDEO_DURATION = 13
    DB_PATH = 'data/db.sqlite'
    VIDEO_PATH = r'objects\Query.mp4'
    OUTPUT_JSON = 'output.json'
    RESULTS_JSON = 'results.json'
    SQL_MODIFICATION_COMMANDS = frozenset(["DROP", "REPLACE", "UPDATE", "INSERT", "DELETE"])

    # Emoji e messaggi
    EMOJI_ERROR = "🛑"
    EMOJI_WARNING = "🙂‍↕️"
    EMOJI_SUCCESS = "💥"
    EMOJI_EMPTY = "🫤"


# ==================== CSS OTTIMIZZATO ====================
def load_custom_css():
    st.markdown("""
<style>
    /* === BASE === */
    .stApp { background: linear-gradient(135deg, #1a2332 0%, #0f1419 100%); }
    .main .block-container { background-color: transparent; }
    .main { color: #e8eaed; }
    hr { border-color: rgba(255, 255, 255, 0.2) !important; }
    p, div, span { font-size: 1.2rem !important; }
    .main p { font-size: 1.25rem !important; line-height: 1.6 !important; }

    /* === SIDEBAR === */
    section[data-testid="stSidebar"] {
        font-size: 1.25rem !important;
        background: linear-gradient(180deg, #1e2936 0%, #151b24 100%);
    }
    section[data-testid="stSidebar"] * { font-size: 1.25rem !important; color: #e8eaed !important; }
    section[data-testid="stSidebar"] h1 { font-size: 2rem !important; font-weight: 700 !important; color: #fff !important; }
    section[data-testid="stSidebar"] h2 { font-size: 1.7rem !important; font-weight: 600 !important; color: #fff !important; }
    section[data-testid="stSidebar"] h3 { font-size: 1.4rem !important; font-weight: 600 !important; color: #fff !important; }
    section[data-testid="stSidebar"] a {
        font-size: 1.3rem !important;
        padding: 0.75rem 1rem !important;
        color: #e8eaed !important;
    }
    section[data-testid="stSidebar"] a:hover {
        background-color: rgba(102, 126, 234, 0.2) !important;
        border-left: 3px solid #667eea !important;
    }

    /* === TITOLI === */
    h1 { font-size: 2.5rem !important; font-weight: 700 !important; color: #fff !important; }
    h2 { font-size: 2rem !important; font-weight: 600 !important; color: #fff !important; }
    h3 { font-size: 1.5rem !important; font-weight: 600 !important; color: #fff !important; }

    /* === TEXT AREA === */
    .stTextArea textarea {
        background-color: #2a3544 !important;
        color: #e8eaed !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 10px !important;
        font-size: 1.2rem !important;
        padding: 1rem !important;
    }
    .stTextArea textarea::placeholder { font-size: 1.1rem !important; color: rgba(232, 234, 237, 0.5) !important; }
    .stTextArea textarea:focus {
        border-color: rgba(102, 126, 234, 0.6) !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    .stTextArea label { color: #fff !important; font-size: 1.4rem !important; font-weight: 600 !important; }

/* === BOTTONI === */
    .stButton>button, 
    .stDownloadButton>button,
    button[data-testid="baseButton-secondary"],
    div[data-testid="stPopover"] button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0.85rem 2.2rem !important;
        border-radius: 8px !important;
        font-size: 1.3rem !important;
        transition: transform 0.3s, box-shadow 0.3s !important;
        width: 100% !important;
        height: auto !important;
    }
    .stButton>button:hover, 
    .stDownloadButton>button:hover,
    button[data-testid="baseButton-secondary"]:hover,
    div[data-testid="stPopover"] button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
    }

    /* === MESSAGGI === */
    .stSuccess, .stWarning, .stError, .stInfo {
        background-color: rgba(42, 53, 68, 0.9) !important;
        color: #e8eaed !important;
        border-radius: 8px !important;
        font-size: 1.3rem !important;
        padding: 1.5rem !important;
    }
    .stSuccess { border-left: 4px solid #4caf50 !important; }
    .stWarning { border-left: 4px solid #ff9800 !important; }
    .stError { border-left: 4px solid #f44336 !important; }
    .stInfo { border-left: 4px solid #2196f3 !important; }

    /* === CODE === */
    .stCodeBlock, pre, code {
        background-color: #1e2936 !important;
        color: #e8eaed !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 8px !important;
        font-size: 1.25rem !important;
        padding: 1.5rem !important;
        line-height: 1.6 !important;
    }

    /* === DATAFRAME === */
    .stDataFrame, [data-testid="stDataFrame"] { font-size: 1.3rem !important; }
    .stDataFrame td, .stDataFrame th { font-size: 1.3rem !important; padding: 1rem 1.2rem !important; }
    .stDataFrame thead th { font-size: 1.4rem !important; font-weight: 700 !important; padding: 1.2rem !important; }

    /* === MEDIA === */
    .stVideo, video {
        border-radius: 10px !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
        border: 2px solid rgba(102, 126, 234, 0.3);
    }
    img { border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }

    /* === PROGRESS & SPINNER === */
    .stProgress > div > div { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; }
    .stSpinner > div, .stSpinner p { font-size: 1.3rem !important; color: #fff !important; }
</style>
""", unsafe_allow_html=True)


# ==================== GESTIONE STATO ====================
class SessionState:
    @staticmethod
    def init():
        """Inizializza tutte le variabili di stato"""
        defaults = {
            'video_visto': False,
            'video_start': None,
            'sandbox_db': None,
            'query_in_elaborazione': False
        }
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    @staticmethod
    def reset_sandbox():
        """Reset del database sandbox"""
        if st.session_state.sandbox_db:
            st.session_state.sandbox_db.close()
        st.session_state.sandbox_db = DatabaseManager.create_sandbox(Config.DB_PATH)


# ==================== DATABASE MANAGER ====================
class DatabaseManager:
    @staticmethod
    def create_sandbox(db_path):
        """Crea un database sandbox in memoria"""
        if not Path(db_path).exists():
            raise FileNotFoundError(f"Database non trovato: {db_path}")

        source = sqlite3.connect(db_path)
        sandbox = sqlite3.connect(':memory:', check_same_thread=False)
        source.backup(sandbox)
        source.close()
        return sandbox

    @staticmethod
    def execute_query(query, db_connection):
        """Esegue una query SQL e restituisce i risultati"""
        if "Warning" in query:
            return Config.EMOJI_WARNING

        try:
            cursor = db_connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            db_connection.commit()

            # Gestione risultati per comandi di modifica
            if not result:
                if any(cmd in query for cmd in Config.SQL_MODIFICATION_COMMANDS):
                    return f"{Config.EMOJI_SUCCESS} La query è stata eseguita!"
                return f"{Config.EMOJI_EMPTY} Nada!"

            # ✨ Estrai i nomi delle colonne
            column_names = [description[0] for description in cursor.description]

            # Restituisci un dizionario con colonne e dati
            return {
                'columns': column_names,
                'data': result
            }

        except sqlite3.Error as e:
            print(f"Errore SQL: {e}")
            return f"{Config.EMOJI_ERROR} Error: {e} {Config.EMOJI_ERROR}"


# ==================== FILE MANAGER ====================
class FileManager:
    @staticmethod
    def load_json(filepath):
        """Carica un file JSON"""
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def save_json(filepath, data):
        """Salva dati in un file JSON"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def convert_to_csv(data):
        """Converte i risultati in formato CSV"""
        if isinstance(data, str):
            return None

        # Se i dati sono un dizionario con 'columns' e 'data'
        if isinstance(data, dict) and 'columns' in data and 'data' in data:
            df = pd.DataFrame(data['data'], columns=data['columns'])
        else:
            df = pd.DataFrame(data)

        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8')
        return csv_buffer.getvalue()


# ==================== QUERY PROCESSOR ====================
class QueryProcessor:
    @staticmethod
    def process_api_response():
        """Processa la risposta dell'API ed esegue la query"""
        completion = FileManager.load_json(Config.OUTPUT_JSON)
        query = completion["query"]
        disamina = completion["disamina"]

        print(f"Query: {query}")
        print(f"Disamina: {disamina}")

        query_result = DatabaseManager.execute_query(query, st.session_state.sandbox_db)
        FileManager.save_json(Config.RESULTS_JSON, [disamina, query, query_result])


# ==================== UI COMPONENTS ====================
class UIComponents:
    @staticmethod
    def show_centered_image(image_path):
        """Mostra un'immagine centrata"""
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image_path)

    @staticmethod
    def render_string_result(query_result, sql_query):
        """Renderizza risultati stringa con stili appropriati"""
        if Config.EMOJI_ERROR in query_result:
            st.error(query_result)
            UIComponents.show_centered_image(r"objects\hasbu.avif")
        elif "Warning" in sql_query or Config.EMOJI_WARNING in query_result:
            st.warning(query_result)
            UIComponents.show_centered_image(r"objects\meme.jpg")
        elif Config.EMOJI_SUCCESS in query_result or Config.EMOJI_EMPTY in query_result:
            st.success(query_result)
        else:
            st.write(query_result)

    @staticmethod
    def render_results():
        """Renderizza i risultati della query"""
        disamina, sql_query, query_result = FileManager.load_json(Config.RESULTS_JSON)

        st.markdown("---")

        # Ragionamento
        st.markdown("### 🧠 Ragionamento dell'AI")
        st.info(disamina)

        # Query SQL
        st.markdown("### 💻 Query SQL Generata")
        st.code(sql_query, language="sql")

        # Risultato
        st.markdown("### 📊 Risultato")

        if isinstance(query_result, str):
            UIComponents.render_string_result(query_result, sql_query)
        elif isinstance(query_result, dict) and 'columns' in query_result:
            # ✨ Crea DataFrame con nomi di colonna
            df = pd.DataFrame(query_result['data'], columns=query_result['columns'])
            st.dataframe(df, use_container_width=True)

            # Bottone download CSV
            csv_data = FileManager.convert_to_csv(query_result)
            if csv_data:
                st.download_button(
                    label="📥 Scarica Risultati (CSV)",
                    data=csv_data,
                    file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=False
                )
        else:
            # Fallback per formato vecchio
            st.dataframe(query_result, use_container_width=True)

        # Video per operazioni pericolose
        if Config.EMOJI_ERROR not in str(query_result) and any(cmd in sql_query for cmd in ["DELETE", "DROP"]):
            st.video(r"objects\non_farlo.mp4")

    @staticmethod
    def show_video_intro():
        """Gestisce il video introduttivo"""
        if st.session_state.video_start is None:
            st.session_state.video_start = datetime.now()

        try:
            with open(Config.VIDEO_PATH, "rb") as video_file:
                video_base64 = base64.b64encode(video_file.read()).decode()

            st.markdown(f"""
            <div style="display:flex; justify-content:center; margin:20px 0;">
                <video autoplay controls style="max-width:1200px; width:100%;">
                    <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                </video>
            </div>
            """, unsafe_allow_html=True)

            elapsed = (datetime.now() - st.session_state.video_start).total_seconds()

            if elapsed < Config.VIDEO_DURATION:
                progress = min(elapsed / Config.VIDEO_DURATION, 1.0)
                st.progress(progress)
                st.write(f"⏱️ Il video termina tra {int(Config.VIDEO_DURATION - elapsed)} secondi...")

                # Bottone skip
                col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
                with col3:
                    if st.button("⏭️ Salta", use_container_width=True):
                        st.session_state.video_visto = True
                        st.rerun()

                time.sleep(1)
                st.rerun()
            else:
                st.session_state.video_visto = True
                st.rerun()

        except FileNotFoundError:
            st.warning("⚠️ Video non trovato. Passo direttamente alla sezione principale.")
            st.session_state.video_visto = True
            st.rerun()

    @staticmethod
    def render_main_interface():
        """Renderizza l'interfaccia principale"""
        st.title("🔎 Interroga il database...")
        st.write("")
        st.write("")

        # Input query
        query = st.text_area(
            "💬 Inserisci la tua query:",
            height=200,
            placeholder="Esempio: Le canzoni rock che durano più di 10 minuti...",
        )

        # Bottoni
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            esegui = st.button("🔍 Esegui Query", use_container_width=True)

        with col2:
            with st.popover("ℹ️ Info Database", use_container_width=True):
                st.markdown("### 🗃️ IL DATABASE")
                st.write(
                    "Database dello store musicale Chinook: artisti musicali, album, canzoni, playlist, "
                    "generi musicali, clienti, fatture, dipendenti, etc. È composto da 11 tabelle e oltre 15000 record!"
                )
                st.image(r"objects\db_scheme.png", width=625)

        with col3:
            reset = st.button("🔄 Reset Database", use_container_width=True)

        # Gestione azioni
        if reset:
            SessionState.reset_sandbox()
            st.success("✅ Database ripristinato!")

        if esegui and query:
            UIComponents.execute_query_workflow(query)

        # Mostra risultati
        if query and not st.session_state.query_in_elaborazione:
            UIComponents.show_results_if_available()

    @staticmethod
    def execute_query_workflow(query):
        """Esegue il workflow completo della query"""
        st.session_state.query_in_elaborazione = True

        # Cancella risultati precedenti
        if os.path.exists(Config.RESULTS_JSON):
            os.remove(Config.RESULTS_JSON)

        with st.spinner("🗿​ Sto elaborando la tua richiesta..."):
            # Progress bar animata
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)

            try:
                api_call(query)
                QueryProcessor.process_api_response()
                st.session_state.query_in_elaborazione = False
                st.success("✅ Query elaborata con successo!")
            except Exception as e:
                st.session_state.query_in_elaborazione = False
                st.error(f"❌ Errore durante l'elaborazione: {e}")

    @staticmethod
    def show_results_if_available():
        """Mostra i risultati se disponibili"""
        try:
            UIComponents.render_results()
        except FileNotFoundError:
            st.info("💡 Inserisci una query e clicca su 'Esegui Query' per iniziare!")
        except Exception as e:
            st.error(f"❌ Errore: {e}")


# ==================== MAIN APP ====================
def main():
    """Funzione principale dell'applicazione"""
    # Inizializzazione
    SessionState.init()
    load_custom_css()

    # Gestione video introduttivo
    if not st.session_state.video_visto:
        UIComponents.show_video_intro()
    else:
        # Inizializza database se necessario
        if st.session_state.sandbox_db is None:
            st.session_state.sandbox_db = DatabaseManager.create_sandbox(Config.DB_PATH)

        # Renderizza interfaccia principale
        UIComponents.render_main_interface()


if __name__ == "__main__":
    main()