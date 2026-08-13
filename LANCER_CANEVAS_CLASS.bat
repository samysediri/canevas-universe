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
echo.
pause
