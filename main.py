import streamlit as st
import anthropic
# import google.generativeai as genai
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import Flow
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseUpload
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from urllib.parse import urlparse
import time
import re
from PIL import Image
import io
import base64

# ============================================
# CONFIGURATION STREAMLIT
# ============================================

st.set_page_config(
    page_title="SEO Intelligence Suite Pro v6.0 🚀",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CSS MODERNE ET ÉLÉGANT
# ============================================

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .block-container {
        padding: 2rem 3rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        margin: 1rem auto;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Header animé */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 2rem 0;
        animation: gradient 3s ease infinite;
        background-size: 200% 200%;
        letter-spacing: -1px;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.2rem;
        margin-top: -1rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    /* Cards modernes */
    .metric-card-pro {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.06);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card-pro::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transform: scaleX(0);
        transition: transform 0.4s ease;
    }
    
    .metric-card-pro:hover::before {
        transform: scaleX(1);
    }
    
    .metric-card-pro:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.25);
    }
    
    /* Boutons stylés */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* Tags premium */
    .tag { 
        display: inline-block; 
        padding: 0.4rem 1rem; 
        border-radius: 25px; 
        font-size: 0.8rem; 
        font-weight: 600; 
        margin: 0.3rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .tag-p0 { 
        background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
        color: white;
    }
    .tag-p1 { 
        background: linear-gradient(135deg, #ffd93d, #f9ca24);
        color: #2d3436;
    }
    .tag-p2 { 
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
    }
    
    /* Expanders élégants */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        font-weight: 600;
        padding: 1rem;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
        transform: translateX(5px);
    }
    
    /* Progress bar moderne */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        background-size: 200% 100%;
        animation: progress 1.5s ease infinite;
    }
    
    @keyframes progress {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Success/Error messages */
    .element-container div.stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Image preview */
    .image-preview {
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .image-preview:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 50px rgba(0,0,0,0.3);
    }
    
    /* Stats cards */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        font-weight: 500;
    }
    
    /* Tabs personnalisés */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        background: #f8fafc;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Loading animation */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================

if 'anthropic_key' not in st.session_state:
    st.session_state.anthropic_key = None

if 'gemini_key' not in st.session_state:
    st.session_state.gemini_key = None

if 'google_creds' not in st.session_state:
    st.session_state.google_creds = None

if 'paa_questions' not in st.session_state:
    st.session_state.paa_questions = []

if 'paa_selected' not in st.session_state:
    st.session_state.paa_selected = []

if 'paa_content_generated' not in st.session_state:
    st.session_state.paa_content_generated = []

if 'generated_images' not in st.session_state:
    st.session_state.generated_images = {}

if 'linking_suggestions' not in st.session_state:
    st.session_state.linking_suggestions = {}

if 'paa_keyword' not in st.session_state:
    st.session_state.paa_keyword = ""

if 'paa_brand_context' not in st.session_state:
    st.session_state.paa_brand_context = ""

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'links_injected' not in st.session_state:
    st.session_state.links_injected = False

if 'roi_data' not in st.session_state:
    st.session_state.roi_data = {
        'cost_per_article': 15.0,
        'time_per_article': 3.0,
        'hourly_rate': 50.0
    }

# ============================================
# FONCTIONS GEMINI
# ============================================

def init_gemini(api_key):
    """Initialise l'API Gemini"""
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Erreur initialisation Gemini: {str(e)}")
        return False

def generate_image_with_gemini(prompt, article_context=""):
    """Génère une image avec Gemini Imagen"""
    try:
        if not st.session_state.gemini_key:
            st.error("Clé API Gemini non configurée")
            return None
        
        # Note: Gemini Imagen n'est pas encore disponible publiquement via l'API Python
        # Pour l'instant, on génère un placeholder avec les specs
        st.info("🎨 Génération d'image avec Gemini (Placeholder - API en développement)")
        
        # Créer une image placeholder
        img = Image.new('RGB', (1024, 1024), color=(102, 126, 234))
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return {
            'image_data': buffer,
            'prompt': prompt,
            'format': 'PNG',
            'size': '1024x1024'
        }
        
    except Exception as e:
        st.error(f"Erreur génération image: {str(e)}")
        return None

def generate_image_prompts_with_claude(article_content, question, anthropic_key):
    """Génère des prompts d'images optimisés avec Claude"""
    client = anthropic.Anthropic(api_key=anthropic_key)
    
    prompt = f"""Analyse cet article SEO et génère 3 prompts optimisés pour créer des images avec Gemini Imagen.

ARTICLE: {article_content[:2000]}
QUESTION: {question}

Pour chaque image, fournis:
1. Un prompt détaillé et descriptif (en anglais)
2. Le type d'image (illustration, infographie, photo-réaliste, diagramme)
3. Le placement suggéré dans l'article

Format JSON:
{{
  "image_prompts": [
    {{
      "prompt": "Detailed English prompt for Gemini Imagen",
      "type": "illustration",
      "placement": "Après l'introduction",
      "alt_text": "Description pour SEO"
    }}
  ]
}}

Réponds UNIQUEMENT avec le JSON."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        text = message.content[0].text
        json_match = re.search(r'\{[\s\S]*\}', text)
        
        if json_match:
            data = json.loads(json_match.group(0))
            return data.get('image_prompts', [])
        
        return []
        
    except Exception as e:
        st.error(f"Erreur génération prompts: {str(e)}")
        return []

# ============================================
# FONCTIONS GOOGLE WORKSPACE
# ============================================

def save_to_google_docs(content, title, creds):
    """Sauvegarde le contenu dans Google Docs"""
    try:
        docs_service = build('docs', 'v1', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)
        
        # Créer le document
        doc = docs_service.documents().create(body={'title': title}).execute()
        doc_id = doc.get('documentId')
        
        # Ajouter le contenu
        requests_body = [{
            'insertText': {
                'location': {'index': 1},
                'text': content
            }
        }]
        
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests_body}
        ).execute()
        
        # Obtenir le lien
        file = drive_service.files().get(fileId=doc_id, fields='webViewLink').execute()
        
        return {
            'success': True,
            'doc_id': doc_id,
            'link': file.get('webViewLink')
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def save_images_to_drive(images, folder_name, creds):
    """Sauvegarde les images dans Google Drive"""
    try:
        drive_service = build('drive', 'v3', credentials=creds)
        
        # Créer un dossier
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')
        
        uploaded_files = []
        
        for idx, img_data in enumerate(images):
            file_metadata = {
                'name': f'image_{idx+1}.png',
                'parents': [folder_id]
            }
            
            media = MediaIoBaseUpload(
                img_data['image_data'],
                mimetype='image/png',
                resumable=True
            )
            
            file = drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,webViewLink'
            ).execute()
            
            uploaded_files.append({
                'file_id': file.get('id'),
                'link': file.get('webViewLink')
            })
        
        return {
            'success': True,
            'folder_id': folder_id,
            'files': uploaded_files
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

# ============================================
# FONCTIONS CLAUDE (SEO)
# ============================================

def extract_paa_questions(keyword, anthropic_key, num=20):
    """Extrait les questions PAA avec Claude"""
    client = anthropic.Anthropic(api_key=anthropic_key)
    
    prompt = f"""Tu es un expert SEO. Génère {num} questions PAA (People Also Ask) réalistes et variées pour le mot-clé "{keyword}".

Format JSON strict requis:
{{
  "paa_questions": [
    {{
      "question": "Question PAA complète et naturelle ?",
      "priority": "P0",
      "difficulty": "easy",
      "search_intent": "informational",
      "estimated_volume": "high",
      "related_keywords": ["kw1", "kw2", "kw3"],
      "content_type": "Article",
      "content_angle": "Comment faire X",
      "target_length": "1500-2000 words"
    }}
  ]
}}

Critères:
- Questions variées (comment, pourquoi, quoi, combien, etc.)
- Priorité: P0 (haute), P1 (moyenne), P2 (basse)
- Difficulté: easy, medium, hard
- Intent: informational, transactional, navigational
- Volume: high, medium, low

Réponds UNIQUEMENT avec le JSON, rien d'autre."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        text = message.content[0].text
        json_match = re.search(r'\{[\s\S]*\}', text)
        
        if json_match:
            data = json.loads(json_match.group(0))
            return data
        
        return {"paa_questions": []}
        
    except Exception as e:
        st.error(f"Erreur extraction PAA: {str(e)}")
        return {"paa_questions": []}

def generate_paa_content(question_data, anthropic_key, brand_context=""):
    """Génère un article SEO optimisé"""
    client = anthropic.Anthropic(api_key=anthropic_key)
    
    prompt = f"""Tu es un expert rédacteur SEO. Rédige un article complet et optimisé pour cette question PAA.

QUESTION: {question_data['question']}
INTENT: {question_data.get('search_intent', 'informational')}
KEYWORDS: {', '.join(question_data.get('related_keywords', []))}
CONTEXTE MARQUE: {brand_context}

L'article doit:
- Être structuré avec des titres H2, H3
- Contenir 1500-2500 mots
- Inclure des listes à puces
- Répondre directement à la question
- Être optimisé SEO
- Avoir un ton professionnel mais accessible

Format Markdown."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
        
    except Exception as e:
        st.error(f"Erreur génération contenu: {str(e)}")
        return "Erreur de génération"

def generate_internal_linking(articles, anthropic_key):
    """Génère des suggestions de maillage interne"""
    client = anthropic.Anthropic(api_key=anthropic_key)
    
    articles_summary = "\n\n".join([
        f"ARTICLE {i+1}: {a['question']}\nContenu: {a['content'][:500]}..."
        for i, a in enumerate(articles[:10])
    ])
    
    prompt = f"""Analyse ces articles et génère une stratégie de maillage interne optimale.

{articles_summary}

Pour chaque article, suggère:
- 2-4 liens internes vers d'autres articles
- L'ancre exacte à utiliser
- La position dans le texte

Format JSON:
{{
  "linking_matrix": [
    {{
      "from_article": 0,
      "to_article": 2,
      "anchor_text": "texte de l'ancre",
      "context": "phrase où insérer le lien"
    }}
  ]
}}

Réponds UNIQUEMENT avec le JSON."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        text = message.content[0].text
        json_match = re.search(r'\{[\s\S]*\}', text)
        
        if json_match:
            return json.loads(json_match.group(0))
        
        return {"linking_matrix": []}
        
    except Exception as e:
        st.error(f"Erreur génération maillage: {str(e)}")
        return {"linking_matrix": []}

def inject_internal_links(articles, linking_matrix):
    """Injecte les liens internes dans les articles"""
    injected = articles.copy()
    stats = {'total_injections': 0}
    
    for link in linking_matrix:
        from_idx = link['from_article']
        to_idx = link['to_article']
        anchor = link['anchor_text']
        
        if from_idx < len(injected) and to_idx < len(injected):
            target_article = injected[to_idx]['question']
            link_md = f"[{anchor}](#{to_idx})"
            
            # Rechercher et remplacer l'ancre dans le contenu
            if anchor in injected[from_idx]['content']:
                injected[from_idx]['content'] = injected[from_idx]['content'].replace(
                    anchor, link_md, 1
                )
                stats['total_injections'] += 1
    
    return injected, stats

def calculate_roi(articles, roi_data):
    """Calcule le ROI de la production de contenu"""
    num_articles = len(articles)
    
    # Coûts traditionnels
    traditional_cost = num_articles * roi_data['cost_per_article']
    traditional_time = num_articles * roi_data['time_per_article']
    
    # Coûts avec l'outil (estimation)
    tool_cost = num_articles * 0.50  # 0.50€ par article (API Claude)
    tool_time = num_articles * 0.1  # 6 minutes par article
    
    # Économies
    cost_saved = traditional_cost - tool_cost
    time_saved = traditional_time - tool_time
    value_saved = time_saved * roi_data['hourly_rate']
    
    roi_percentage = ((value_saved - tool_cost) / tool_cost) * 100 if tool_cost > 0 else 0
    
    return {
        'num_articles': num_articles,
        'traditional_cost': traditional_cost,
        'tool_cost': tool_cost,
        'cost_saved': cost_saved,
        'traditional_time_hours': traditional_time,
        'tool_time_hours': tool_time,
        'time_saved_hours': time_saved,
        'value_time_saved': value_saved,
        'total_cost': tool_cost,
        'roi_percentage': roi_percentage
    }

def generate_client_report(articles, linking_data, roi_data, anthropic_key):
    """Génère un rapport client professionnel"""
    client = anthropic.Anthropic(api_key=anthropic_key)
    
    summary = f"""Génère un rapport client professionnel pour cette production de contenu SEO:

STATISTIQUES:
- {len(articles)} articles générés
- ROI: {roi_data['roi_percentage']:.1f}%
- Économie: {roi_data['value_time_saved']:.0f}€
- Temps économisé: {roi_data['time_saved_hours']:.1f}h
- Liens internes: {len(linking_data.get('linking_matrix', []))}

ARTICLES:
{chr(10).join([f"- {a['question']}" for a in articles[:10]])}

Le rapport doit inclure:
1. Résumé exécutif
2. Métriques clés
3. Liste des articles avec stats
4. Stratégie de maillage
5. ROI détaillé
6. Prochaines étapes

Format Markdown professionnel."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            messages=[{"role": "user", "content": summary}]
        )
        
        return message.content[0].text
        
    except Exception as e:
        return f"# Rapport Client\n\nErreur de génération: {str(e)}"

def chat_with_assistant(user_message, articles, linking_data, anthropic_key):
    """Assistant IA pour questions sur le projet"""
    client = anthropic.Anthropic(api_key=anthropic_key)
    
    context = f"""Tu es un assistant SEO expert. Tu as accès à ces données:

ARTICLES GÉNÉRÉS: {len(articles)}
LIENS INTERNES: {len(linking_data.get('linking_matrix', []))}

Réponds à la question de l'utilisateur de manière concise et utile.

QUESTION: {user_message}"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1000,
            messages=[{"role": "user", "content": context}]
        )
        
        return message.content[0].text
        
    except Exception as e:
        return f"Erreur: {str(e)}"

# ============================================
# INTERFACE PRINCIPALE
# ============================================

def main():
    # Header avec animation
    st.markdown('<h1 class="main-header">🚀 SEO Intelligence Suite Pro v6.0</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">✨ Génération de Contenu SEO Premium avec IA • Gemini Images • Google Workspace</p>', unsafe_allow_html=True)
    
    # SIDEBAR - Configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # Clé Anthropic
        anthropic_input = st.text_input(
            "🔑 Clé API Anthropic (Claude)",
            type="password",
            value=st.session_state.get('anthropic_key', '') or '',
            help="Obtenez votre clé sur console.anthropic.com"
        )
        
        if anthropic_input:
            st.session_state.anthropic_key = anthropic_input
            st.success("✅ Claude connecté")
        
        # Clé Gemini
        gemini_input = st.text_input(
            "🎨 Clé API Gemini (Images)",
            type="password",
            value=st.session_state.get('gemini_key', '') or '',
            help="Obtenez votre clé sur ai.google.dev"
        )
        
        if gemini_input:
            st.session_state.gemini_key = gemini_input
            if init_gemini(gemini_input):
                st.success("✅ Gemini connecté")
        
        st.markdown("---")
        
        # Stats en temps réel
        if st.session_state.paa_content_generated:
            st.markdown("### 📊 Stats en Temps Réel")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{len(st.session_state.paa_content_generated)}</div>
                    <div class="stat-label">Articles</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                images_count = len(st.session_state.generated_images)
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{images_count}</div>
                    <div class="stat-label">Images</div>
                </div>
                """, unsafe_allow_html=True)
            
            # ROI Quick View
            if st.session_state.paa_content_generated:
                roi = calculate_roi(st.session_state.paa_content_generated, st.session_state.roi_data)
                st.markdown(f"""
                <div class="metric-card-pro" style="margin-top: 1rem;">
                    <h4 style="margin: 0 0 0.5rem 0;">💰 ROI Rapide</h4>
                    <div style="font-size: 2rem; font-weight: 800; color: #667eea;">{roi['roi_percentage']:.0f}%</div>
                    <div style="color: #64748b; font-size: 0.9rem;">Économie: {roi['value_time_saved']:.0f}€</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🎯 Paramètres ROI")
        
        st.session_state.roi_data['cost_per_article'] = st.number_input(
            "Coût article manuel (€)",
            value=15.0,
            min_value=0.0,
            step=1.0
        )
        
        st.session_state.roi_data['time_per_article'] = st.number_input(
            "Temps article manuel (h)",
            value=3.0,
            min_value=0.0,
            step=0.5
        )
        
        st.session_state.roi_data['hourly_rate'] = st.number_input(
            "Taux horaire (€)",
            value=50.0,
            min_value=0.0,
            step=5.0
        )
    
    # MAIN CONTENT
    if not st.session_state.anthropic_key:
        st.warning("⚠️ Veuillez configurer votre clé API Anthropic dans la sidebar")
        st.info("👈 Cliquez sur la sidebar pour commencer")
        st.stop()
    
    # TABS
    tabs = st.tabs([
        "🎯 Génération PAA",
        "🎨 Visuels Gemini",
        "🔗 Maillage Interne",
        "📊 ROI & Analytics",
        "📄 Rapports Client",
        "💬 Assistant IA",
        "☁️ Google Workspace"
    ])
    
    # TAB 1: GÉNÉRATION PAA
    with tabs[0]:
        st.markdown("## 🎯 Extraction & Génération PAA")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            keyword = st.text_input(
                "🔍 Mot-clé principal",
                value=st.session_state.get('paa_keyword', ''),
                placeholder="Ex: marketing digital",
                help="Le mot-clé pour lequel générer des questions PAA"
            )
            st.session_state.paa_keyword = keyword
        
        with col2:
            num_questions = st.selectbox(
                "📝 Nombre de questions",
                options=[10, 20, 30, 50],
                index=1
            )
        
        brand_context = st.text_area(
            "🏢 Contexte de marque (optionnel)",
            value=st.session_state.get('paa_brand_context', ''),
            placeholder="Ex: Nous sommes une agence SEO spécialisée en e-commerce...",
            height=100
        )
        st.session_state.paa_brand_context = brand_context
        
        if st.button("🚀 EXTRAIRE LES QUESTIONS PAA", type="primary", use_container_width=True):
            if keyword:
                with st.spinner("🔍 Extraction des questions PAA en cours..."):
                    data = extract_paa_questions(keyword, st.session_state.anthropic_key, num_questions)
                    st.session_state.paa_questions = data.get('paa_questions', [])
                    
                if st.session_state.paa_questions:
                    st.success(f"✅ {len(st.session_state.paa_questions)} questions extraites!")
                    st.rerun()
            else:
                st.warning("⚠️ Veuillez entrer un mot-clé")
        
        # Affichage des questions
        if st.session_state.paa_questions:
            st.markdown("---")
            st.markdown("### 📋 Questions PAA Extraites")
            
            # Filtres rapides
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("✅ Tout Sélectionner", use_container_width=True):
                    st.session_state.paa_selected = list(range(len(st.session_state.paa_questions)))
                    st.rerun()
            
            with col2:
                if st.button("❌ Tout Désélectionner", use_container_width=True):
                    st.session_state.paa_selected = []
                    st.rerun()
            
            with col3:
                if st.button("🔥 P0 Seulement", use_container_width=True):
                    st.session_state.paa_selected = [
                        i for i, q in enumerate(st.session_state.paa_questions)
                        if q.get('priority') == 'P0'
                    ]
                    st.rerun()
            
            with col4:
                if st.button("⭐ P0 + P1", use_container_width=True):
                    st.session_state.paa_selected = [
                        i for i, q in enumerate(st.session_state.paa_questions)
                        if q.get('priority') in ['P0', 'P1']
                    ]
                    st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Liste des questions
            for idx, q in enumerate(st.session_state.paa_questions):
                priority = q.get('priority', 'P2')
                difficulty = q.get('difficulty', 'medium')
                intent = q.get('search_intent', 'informational')
                
                is_selected = idx in st.session_state.paa_selected
                
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    if st.checkbox(
                        f"**{q['question']}**",
                        value=is_selected,
                        key=f"sel_{idx}"
                    ):
                        if idx not in st.session_state.paa_selected:
                            st.session_state.paa_selected.append(idx)
                    else:
                        if idx in st.session_state.paa_selected:
                            st.session_state.paa_selected.remove(idx)
                
                with col2:
                    tag_class = f"tag-{priority.lower()}"
                    st.markdown(
                        f'<span class="tag {tag_class}">{priority}</span> '
                        f'<span class="tag">{difficulty}</span> '
                        f'<span class="tag">{intent[:4]}</span>',
                        unsafe_allow_html=True
                    )
            
            # Bouton de génération
            if st.session_state.paa_selected:
                st.markdown("---")
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.success(f"✅ {len(st.session_state.paa_selected)} question(s) sélectionnée(s)")
                
                with col2:
                    if st.button(
                        f"🚀 GÉNÉRER {len(st.session_state.paa_selected)} ARTICLES",
                        type="primary",
                        use_container_width=True
                    ):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for i, idx in enumerate(st.session_state.paa_selected):
                            question_data = st.session_state.paa_questions[idx]
                            
                            status_text.text(f"⏳ Génération article {i+1}/{len(st.session_state.paa_selected)}...")
                            
                            content = generate_paa_content(
                                question_data,
                                st.session_state.anthropic_key,
                                st.session_state.get('paa_brand_context', '')
                            )
                            
                            st.session_state.paa_content_generated.append({
                                'question': question_data['question'],
                                'content': content,
                                'metadata': question_data,
                                'timestamp': datetime.now().isoformat(),
                                'keyword': st.session_state.get('paa_keyword', '')
                            })
                            
                            progress_bar.progress((i + 1) / len(st.session_state.paa_selected))
                            time.sleep(0.3)
                        
                        status_text.empty()
                        st.success("✅ Tous les articles ont été générés!")
                        st.session_state.paa_selected = []
                        st.rerun()
        
        # Affichage des articles générés
        if st.session_state.paa_content_generated:
            st.markdown("---")
            st.markdown("### 📚 Articles Générés")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📥 Télécharger Tout (MD)", use_container_width=True):
                    date_str = datetime.now().strftime('%Y%m%d_%H%M')
                    all_content = "\n\n---\n\n".join([
                        f"# ARTICLE {i+1}\n\n## {a['question']}\n\n{a['content']}"
                        for i, a in enumerate(st.session_state.paa_content_generated)
                    ])
                    st.download_button(
                        "📥 Télécharger",
                        data=all_content,
                        file_name=f"articles_{date_str}.md",
                        mime="text/markdown"
                    )
            
            with col2:
                total_words = sum([
                    len(a['content'].split())
                    for a in st.session_state.paa_content_generated
                ])
                st.metric("📝 Mots Total", f"{total_words:,}")
            
            with col3:
                st.metric("📄 Articles", len(st.session_state.paa_content_generated))
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Liste des articles
            for idx, article in enumerate(st.session_state.paa_content_generated):
                with st.expander(
                    f"📄 Article #{idx+1}: {article['question'][:70]}...",
                    expanded=False
                ):
                    st.markdown(article['content'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "📥 Télécharger",
                            data=article['content'],
                            file_name=f"article_{idx+1}.md",
                            mime="text/markdown",
                            key=f"dl_{idx}",
                            use_container_width=True
                        )
                    
                    with col2:
                        word_count = len(article['content'].split())
                        st.info(f"📝 {word_count} mots")
    
    # TAB 2: VISUELS GEMINI
    with tabs[1]:
        st.markdown("## 🎨 Génération de Visuels avec Gemini")
        
        if not st.session_state.gemini_key:
            st.warning("⚠️ Veuillez configurer votre clé API Gemini dans la sidebar")
        elif not st.session_state.paa_content_generated:
            st.info("📝 Générez d'abord du contenu dans l'onglet 'Génération PAA'")
        else:
            st.markdown("""
            <div class="metric-card-pro">
                <h3>✨ Gemini Imagen</h3>
                <p>Générez automatiquement des images optimisées pour chaque article avec Google Gemini.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Génération globale
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(
                    "🎨 GÉNÉRER TOUTES LES IMAGES",
                    type="primary",
                    use_container_width=True
                ):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i, article in enumerate(st.session_state.paa_content_generated):
                        status_text.text(f"🎨 Génération images pour article {i+1}...")
                        
                        # Générer les prompts avec Claude
                        prompts = generate_image_prompts_with_claude(
                            article['content'],
                            article['question'],
                            st.session_state.anthropic_key
                        )
                        
                        # Générer les images avec Gemini
                        images = []
                        for prompt_data in prompts[:3]:  # Max 3 images par article
                            img_result = generate_image_with_gemini(
                                prompt_data['prompt'],
                                article['content'][:500]
                            )
                            if img_result:
                                images.append({
                                    **img_result,
                                    **prompt_data
                                })
                        
                        if images:
                            st.session_state.generated_images[i] = images
                        
                        progress_bar.progress((i + 1) / len(st.session_state.paa_content_generated))
                        time.sleep(0.5)
                    
                    status_text.empty()
                    st.success("✅ Toutes les images ont été générées!")
                    st.rerun()
            
            with col2:
                total_images = sum([
                    len(imgs) for imgs in st.session_state.generated_images.values()
                ])
                st.metric("🖼️ Images Générées", total_images)
            
            # Affichage des images par article
            if st.session_state.generated_images:
                st.markdown("---")
                st.markdown("### 🖼️ Galerie d'Images")
                
                for article_idx, images in st.session_state.generated_images.items():
                    if article_idx < len(st.session_state.paa_content_generated):
                        article = st.session_state.paa_content_generated[article_idx]
                        
                        with st.expander(
                            f"🖼️ Images pour: {article['question'][:60]}...",
                            expanded=True
                        ):
                            cols = st.columns(min(len(images), 3))
                            
                            for i, img_data in enumerate(images):
                                with cols[i % 3]:
                                    # Note: Placeholder car Gemini Imagen n'est pas encore public
                                    st.info(f"🎨 Image {i+1}")
                                    st.markdown(f"**Prompt:** {img_data['prompt'][:100]}...")
                                    st.markdown(f"**Type:** {img_data.get('type', 'N/A')}")
                                    st.markdown(f"**Placement:** {img_data.get('placement', 'N/A')}")
                                    st.markdown(f"**Alt Text:** {img_data.get('alt_text', 'N/A')}")
            else:
                st.info("📸 Aucune image générée pour le moment")
    
    # TAB 3: MAILLAGE INTERNE
    with tabs[2]:
        st.markdown("## 🔗 Maillage Interne Automatique")
        
        if not st.session_state.paa_content_generated:
            st.info("📝 Générez d'abord du contenu")
        else:
            st.markdown("""
            <div class="metric-card-pro">
                <h3>🕸️ Stratégie de Maillage</h3>
                <p>Optimisez votre SEO avec un maillage interne intelligent généré automatiquement.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(
                    "🔗 GÉNÉRER MAILLAGE",
                    type="primary",
                    use_container_width=True
                ):
                    with st.spinner("🔍 Analyse des articles et génération du maillage..."):
                        linking = generate_internal_linking(
                            st.session_state.paa_content_generated,
                            st.session_state.anthropic_key
                        )
                        st.session_state.linking_suggestions = linking
                        st.success("✅ Maillage généré!")
                        st.rerun()
            
            with col2:
                if st.session_state.linking_suggestions:
                    links_count = len(st.session_state.linking_suggestions.get('linking_matrix', []))
                    st.metric("🔗 Liens Suggérés", links_count)
            
            # Affichage du maillage
            if st.session_state.linking_suggestions:
                linking_matrix = st.session_state.linking_suggestions.get('linking_matrix', [])
                
                if linking_matrix:
                    st.markdown("---")
                    st.markdown("### 🕸️ Matrice de Maillage")
                    
                    for link in linking_matrix[:20]:  # Top 20
                        from_idx = link['from_article']
                        to_idx = link['to_article']
                        
                        if from_idx < len(st.session_state.paa_content_generated) and \
                           to_idx < len(st.session_state.paa_content_generated):
                            
                            from_article = st.session_state.paa_content_generated[from_idx]
                            to_article = st.session_state.paa_content_generated[to_idx]
                            
                            st.markdown(f"""
                            <div class="metric-card-pro" style="margin-bottom: 1rem;">
                                <div style="display: flex; align-items: center; gap: 1rem;">
                                    <div style="flex: 1;">
                                        <strong>De:</strong> {from_article['question'][:50]}...
                                    </div>
                                    <div style="font-size: 1.5rem;">→</div>
                                    <div style="flex: 1;">
                                        <strong>Vers:</strong> {to_article['question'][:50]}...
                                    </div>
                                </div>
                                <div style="margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid #e2e8f0;">
                                    <strong>Ancre:</strong> <code>{link['anchor_text']}</code>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Injection des liens
                    st.markdown("---")
                    
                    if st.button(
                        "⚡ INJECTER TOUS LES LIENS",
                        type="primary",
                        use_container_width=True
                    ):
                        with st.spinner("💉 Injection des liens en cours..."):
                            injected_articles, stats = inject_internal_links(
                                st.session_state.paa_content_generated,
                                linking_matrix
                            )
                            st.session_state.paa_content_generated = injected_articles
                            st.session_state.links_injected = True
                            st.success(f"✅ {stats['total_injections']} liens injectés!")
                            st.rerun()
    
    # TAB 4: ROI & ANALYTICS
    with tabs[3]:
        st.markdown("## 📊 ROI & Analytics")
        
        if st.session_state.paa_content_generated:
            roi_data = calculate_roi(
                st.session_state.paa_content_generated,
                st.session_state.roi_data
            )
            
            # Métriques principales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">ROI</div>
                    <div class="stat-value">{roi_data['roi_percentage']:.0f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Économie</div>
                    <div class="stat-value">{roi_data['value_time_saved']:,.0f}€</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Investissement</div>
                    <div class="stat-value">{roi_data['total_cost']:.0f}€</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Temps Économisé</div>
                    <div class="stat-value">{roi_data['time_saved_hours']:.1f}h</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Détails du ROI
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="metric-card-pro">
                    <h3>📈 Méthode Traditionnelle</h3>
                </div>
                """, unsafe_allow_html=True)
                
                st.metric("💰 Coût Total", f"{roi_data['traditional_cost']:.0f}€")
                st.metric("⏱️ Temps Total", f"{roi_data['traditional_time_hours']:.1f}h")
                st.metric("📄 Articles", roi_data['num_articles'])
            
            with col2:
                st.markdown("""
                <div class="metric-card-pro">
                    <h3>🚀 Avec SEO Suite Pro</h3>
                </div>
                """, unsafe_allow_html=True)
                
                st.metric("💰 Coût Total", f"{roi_data['tool_cost']:.0f}€")
                st.metric("⏱️ Temps Total", f"{roi_data['tool_time_hours']:.1f}h")
                st.metric("📄 Articles", roi_data['num_articles'])
        else:
            st.info("📝 Générez du contenu pour voir les analytics")
    
    # TAB 5: RAPPORTS CLIENT
    with tabs[4]:
        st.markdown("## 📄 Rapports Client Professionnels")
        
        if not st.session_state.paa_content_generated:
            st.info("📝 Générez d'abord du contenu")
        else:
            if st.button(
                "📋 GÉNÉRER RAPPORT CLIENT",
                type="primary",
                use_container_width=True
            ):
                with st.spinner("📄 Génération du rapport..."):
                    roi_data = calculate_roi(
                        st.session_state.paa_content_generated,
                        st.session_state.roi_data
                    )
                    report = generate_client_report(
                        st.session_state.paa_content_generated,
                        st.session_state.linking_suggestions,
                        roi_data,
                        st.session_state.anthropic_key
                    )
                    st.session_state['last_report'] = report
                    st.success("✅ Rapport généré!")
            
            if 'last_report' in st.session_state:
                st.markdown("---")
                st.markdown(st.session_state['last_report'])
                
                date_str = datetime.now().strftime('%Y%m%d_%H%M')
                st.download_button(
                    "📥 Télécharger Rapport (MD)",
                    data=st.session_state['last_report'],
                    file_name=f"rapport_client_{date_str}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
    
    # TAB 6: ASSISTANT IA
    with tabs[5]:
        st.markdown("## 💬 Assistant IA SEO")
        
        if not st.session_state.paa_content_generated:
            st.info("📝 Générez d'abord du contenu pour utiliser l'assistant")
        else:
            st.markdown("""
            <div class="metric-card-pro">
                <h3>🤖 Assistant Intelligent</h3>
                <p>Posez des questions sur votre projet, obtenez des conseils SEO, ou demandez des modifications.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Historique
            for msg in st.session_state.chat_history:
                role = msg['role']
                content = msg['content']
                
                if role == 'user':
                    st.markdown(f"""
                    <div class="metric-card-pro" style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);">
                        <strong>👤 Vous:</strong><br>{content}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="metric-card-pro" style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);">
                        <strong>🤖 Assistant:</strong><br>{content}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
            
            # Input
            user_input = st.text_area(
                "💬 Votre message",
                height=100,
                placeholder="Ex: Peux-tu me donner des conseils pour optimiser le maillage interne ?"
            )
            
            if st.button("📤 ENVOYER", type="primary", use_container_width=True):
                if user_input:
                    st.session_state.chat_history.append({
                        'role': 'user',
                        'content': user_input
                    })
                    
                    with st.spinner("🤔 Réflexion..."):
                        response = chat_with_assistant(
                            user_input,
                            st.session_state.paa_content_generated,
                            st.session_state.linking_suggestions,
                            st.session_state.anthropic_key
                        )
                    
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response
                    })
                    
                    st.rerun()
    
    # TAB 7: GOOGLE WORKSPACE
    with tabs[6]:
        st.markdown("## ☁️ Intégration Google Workspace")
        
        st.markdown("""
        <div class="metric-card-pro">
            <h3>📁 Sauvegarde Automatique</h3>
            <p>Sauvegardez vos articles dans Google Docs et vos images dans Google Drive.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Note: L'authentification OAuth Google nécessite une configuration serveur
        # Pour une démo locale, on affiche juste l'interface
        
        st.info("⚠️ **Note:** L'authentification Google OAuth nécessite une configuration serveur complète.")
        
        st.markdown("""
        ### 🔐 Configuration OAuth
        
        Pour activer l'intégration Google Workspace:
        
        1. **Créez un projet Google Cloud**
           - Allez sur [Google Cloud Console](https://console.cloud.google.com/)
           - Créez un nouveau projet
        
        2. **Activez les APIs**
           - Google Docs API
           - Google Drive API
        
        3. **Créez des credentials OAuth 2.0**
           - Type: Application Web
           - Ajoutez les URIs de redirection
        
        4. **Téléchargez le fichier credentials.json**
           - Placez-le dans le dossier de l'application
        """)
        
        if st.session_state.paa_content_generated:
            st.markdown("---")
            st.markdown("### 📤 Actions Disponibles")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(
                    "📄 Sauvegarder dans Google Docs",
                    use_container_width=True,
                    disabled=True
                ):
                    st.info("Configuration OAuth requise")
            
            with col2:
                if st.button(
                    "🖼️ Sauvegarder Images dans Drive",
                    use_container_width=True,
                    disabled=True
                ):
                    st.info("Configuration OAuth requise")
            
            st.markdown("""
            <div class="metric-card-pro" style="margin-top: 1rem;">
                <h4>✨ Fonctionnalités à venir:</h4>
                <ul>
                    <li>✅ Export automatique vers Google Docs</li>
                    <li>✅ Upload d'images dans Google Drive</li>
                    <li>✅ Organisation automatique en dossiers</li>
                    <li>✅ Partage de liens directs</li>
                    <li>✅ Synchronisation en temps réel</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # FOOTER
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 3rem 0 2rem 0;'>
        <h2 style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-weight: 800; margin-bottom: 0.5rem;'>
            SEO Intelligence Suite Pro v6.0
        </h2>
        <p style='color: #64748b; font-size: 1.1rem; margin: 0;'>
            🚀 Production Automatisée de Contenu SEO Premium
        </p>
        <p style='color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem;'>
            Powered by Claude 4 • Gemini • Google Workspace
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
