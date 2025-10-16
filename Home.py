import streamlit as st
from pathlib import Path

# Configurazione pagina
st.set_page_config(
    page_title="Consta AI",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS per styling
st.markdown("""
<style>
    /* Stili Sidebar - Font MOLTO più grandi - Selettori Universali */
    section[data-testid="stSidebar"],
    .css-1d391kg,
    [data-testid="stSidebar"] {
        font-size: 1.25rem !important;
    }

    /* Tutti gli elementi di testo nella sidebar */
    section[data-testid="stSidebar"] *,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] a,
    [data-testid="stSidebar"] * {
        font-size: 1.25rem !important;
        color: #e8eaed !important;
    }

    /* Titoli nella sidebar */
    section[data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h1 {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h2 {
        font-size: 1.7rem !important;
        font-weight: 600 !important;
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h3 {
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        color: #ffffff !important;
    }

    /* Link di navigazione nella sidebar */
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a,
    section[data-testid="stSidebar"] nav a,
    [data-testid="stSidebar"] a {
        font-size: 1.3rem !important;
        padding: 0.75rem 1rem !important;
        color: #e8eaed !important;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover,
    section[data-testid="stSidebar"] nav a:hover {
        background-color: rgba(102, 126, 234, 0.2) !important;
        border-left: 3px solid #667eea !important;
    }

    /* Radio buttons e checkbox */
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] .stCheckbox label,
    [data-testid="stSidebar"] label {
        font-size: 1.25rem !important;
    }

    /* Select box */
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] select,
    [data-testid="stSidebar"] select {
        font-size: 1.25rem !important;
    }

    /* Text input */
    section[data-testid="stSidebar"] input,
    [data-testid="stSidebar"] input {
        font-size: 1.2rem !important;
    }

    /* Buttons nella sidebar */
    section[data-testid="stSidebar"] button,
    [data-testid="stSidebar"] button {
        font-size: 1.2rem !important;
    }

    /* Sfondo Blu Scuro per la Pagina */
    .stApp {
        background: linear-gradient(135deg, #1a2332 0%, #0f1419 100%);
    }

    .main .block-container {
        background-color: transparent;
    }

    /* Sfondo anche per la sidebar - tonalità coordinata */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e2936 0%, #151b24 100%);
    }

    /* Colore testo principale per leggibilità su sfondo scuro */
    .main {
        color: #e8eaed;
    }

    /* Divisori più visibili su sfondo scuro */
    hr {
        border-color: rgba(255, 255, 255, 0.2) !important;
    }

    /* Stili Main Page */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }

    .subtitle {
        font-size: 1.2rem;
        color: #b8bdc4;
        text-align: center;
        margin-bottom: 2rem;
    }

.feature-card {
    background: linear-gradient(135deg, #2a3544 0%, #1e2936 100%);
    padding: 1.5rem;
    border-radius: 10px;
    margin: 1rem 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    transition: transform 0.2s;
    border: 1px solid rgba(102, 126, 234, 0.2);
    
    min-height: 180px;  /* Altezza minima fissa */
    height: 100%;       /* Occupa tutta l'altezza disponibile */
    display: flex;
    flex-direction: column;
}

    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.3);
        border-color: rgba(102, 126, 234, 0.4);
    }

    .feature-card h3 {
        margin-top: 0;
        color: #ffffff;
    }

    .feature-card p {
        color: #b8bdc4;
    }

    .section-title {
        font-size: 2rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1.5rem;
        margin-top: 2rem;
    }

    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-size: 1.1rem;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }

    /* Miglioramento video container su sfondo scuro */
    .stVideo {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
        border: 2px solid rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

st.title("🫡 Consta, la tua assistente AI")

# Sezione video di presentazione con controllo esistenza file
video_path = Path("Consta.mp4")

if video_path.exists():
    st.video(str(video_path))
else:
    st.warning(
        "⚠️ Video di presentazione non disponibile. Verifica che 'onsta.mp4' sia presente nella directory del progetto.")

# Divider
st.markdown("---")

# Sezione caratteristiche principali
st.markdown('<h2 class="section-title">✨ Caratteristiche Principali</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🌍 Multilingua</h3>
        <p>Interroga il database in italiano o inglese, l'AI comprende il linguaggio naturale e lo traduce in SQL perfetto.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>🛡️ Sicuro per Design</h3>
        <p>Database isolato in memoria, validazione a 2 livelli e protezione contro query pericolose. I tuoi dati sono al sicuro.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🪄 Auto-Correzione</h3>
        <p> Correzione automatica degli errori e ottimizzazione della query in tempo reale\n.</p>
    </div>
    """, unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="feature-card">
        <h3>👩🏻‍🏫 Spiegazioni Chiare</h3>
        <p>Ogni query viene spiegata in linguaggio semplice, così puoi imparare l'SQL mentre lavori.\n</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="feature-card">
        <h3>⚡ Prestazioni Incredibili</h3>
        <p>Risposte rapide anche per query complesse.\n\n</p>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="feature-card">
        <h3>💯 Massima Precisione</h3>
        <p>Impossibile ottenere query inesatte.\n\n</p>
    </div>
    """, unsafe_allow_html=True)

# Divider
st.markdown("---")

# Sezione come iniziare
st.markdown('<h2 class="section-title">🚀 Come Iniziare</h2>', unsafe_allow_html=True)

steps_col1, steps_col2 = st.columns(2)

with steps_col1:
    st.markdown("""
    ### 💬 Fai la tua richiesta
    Scrivi in linguaggio naturale ciò che vuoi sapere dal database:
    - *"Questo mese dobbiamo festeggiare l'anniversario dell'assunzione di qualche dipendente?"*
    - *"Sushi o sashimi?"*                
    - *"Titoli delle canzoni Rock dalla durata superiore ai 5 minuti presenti in almeno due compilation*
    - *"Cancella la tabella dipendenti"*
    - *"Dove vivono i nostri clienti? Indicami i 3 paesi più rappresentativi"*
    - *"Meglio Messi o Ronaldo?"*
    - *"Aggiungi un nuovo cliente di nome Mark Pittau e i relativi valori (usa dati sintetici)"*
    - *"Abbiamo Paolo Conte tra gli artisti?"*
    - *"Analogie tra la sorella del mio collega e Unieuro"*
    - *"Rimuovi tutte le tabelle*
    """)

with steps_col2:
    st.markdown("""

    ### 🧠 Analizza la query
    L'AI genera la query e ti mostra il suo ragionamento così puoi verificare che abbia interpretato correttamente la tua richiesta.
    Scarica il risultato in formato csv con un semplice click per iniziare subito le tue analisi.

    ### 🤓 Impara e migliora
    Leggi la spiegazione educativa dell'AI per capire come funziona la query e migliorare le tue competenze SQL.
    """)

# Call to action
st.markdown("<br>", unsafe_allow_html=True)
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    st.markdown("""
    <div style='text-align: center;'>
        <p style='font-size: 1.5rem; margin: 1rem 0; color: #ffffff;'>
            Pronto per iniziare? Vai alla pagina <strong>Query Interface</strong> dalla sidebar! 👈
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #b8bdc4; padding: 2rem 0;'>
    <p><strong style='color: #ffffff;'>Consta AI v1.0</strong> - Powered by Giuseppe Curridori</p>
    <p>Stack: Python 3.12 | Streamlit | Groq API | OpenAI | SQLite | & more</p>
</div>
""", unsafe_allow_html=True)