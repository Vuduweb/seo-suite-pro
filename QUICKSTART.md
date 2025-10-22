# ⚡ Démarrage Rapide - 5 Minutes

## 🚀 Installation Express

### 1. Créer l'environnement virtuel
```bash
python -m venv venv
```

### 2. Activer l'environnement
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Lancer l'application

**Option A - Scripts automatiques:**
```bash
# Windows
start.bat

# macOS/Linux
./start.sh
```

**Option B - Commande directe:**
```bash
streamlit run main.py
```

L'application s'ouvrira automatiquement sur http://localhost:8501

## 🔑 Configuration

1. Obtenez votre clé API Anthropic sur [console.anthropic.com](https://console.anthropic.com/)
2. Dans l'application, ouvrez la sidebar (coin supérieur gauche)
3. Collez votre clé API dans le champ "🔑 Clé API Anthropic"
4. Cliquez ailleurs pour valider
5. Vous verrez "✅ Claude connecté"

## 🎯 Premier Test

1. **Entrez un mot-clé:** Ex: "marketing digital"
2. **Cliquez sur:** "🚀 EXTRAIRE LES QUESTIONS PAA"
3. **Sélectionnez:** Quelques questions (ou cliquez "🔥 P0 Seulement")
4. **Générez:** Cliquez "🚀 GÉNÉRER X ARTICLES"
5. **Téléchargez:** Vos articles sont prêts !

## 💰 Coûts

- **Claude API:** ~$0.50 par article
- **Gratuit:** 10 premiers articles offerts (selon votre crédit Anthropic)

## 🆘 Problèmes ?

### "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### "Invalid API key"
- Vérifiez que la clé commence par `sk-ant-`
- Vérifiez vos crédits sur console.anthropic.com

### Application ne démarre pas
```bash
python --version  # Vérifiez Python 3.8+
pip install streamlit --upgrade
```

## ✨ Fonctionnalités

- ✅ Génération d'articles SEO
- ✅ Questions PAA automatiques
- ✅ Maillage interne intelligent
- ✅ Analytics et ROI
- 🔜 Images Gemini
- 🔜 Google Workspace

**Bon SEO ! 🚀**
