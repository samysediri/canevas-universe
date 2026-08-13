@echo off
title Canevas + CLASS
cd /d "%~dp0"
echo.
echo Mise a jour depuis GitHub...
git pull --ff-only
if errorlevel 1 (
  echo.
  echo Git pull impossible. Le calcul va utiliser la version locale actuelle.
)
echo.
echo Lancement de Canevas + CLASS...
python canevas_class.py
if errorlevel 1 (
  echo.
  echo Le calcul a rencontre une erreur. Aucun push automatique.
  pause
  exit /b 1
)
echo.
echo Envoi automatique des resultats sur GitHub...
git add results
git commit -m "Add latest CLASS sensitivity results"
if errorlevel 1 (
  echo Aucun nouveau resultat a committer, ou commit impossible.
)
git push
if errorlevel 1 (
  echo.
  echo Le push GitHub a echoue. Les resultats restent sauvegardes localement.
) else (
  echo.
  echo RESULTATS ENVOYES SUR GITHUB.
)
echo.
pause
