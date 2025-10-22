@echo off
echo ========================================
echo   SEO Intelligence Suite Pro v6.0
echo   Demarrage de l'application...
echo ========================================
echo.

REM Activer l'environnement virtuel
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo [OK] Environnement virtuel active
) else (
    echo [ERREUR] Environnement virtuel non trouve
    echo Veuillez d'abord executer:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo [INFO] Lancement de Streamlit...
echo [INFO] L'application va s'ouvrir dans votre navigateur
echo [INFO] URL: http://localhost:8501
echo.
echo Appuyez sur Ctrl+C pour arreter l'application
echo.

streamlit run main.py

pause
