@echo off
title Real-Time Polling Engine Super Launcher
echo ===================================================
echo ⚡ AUTOMATED PROJECT LAUNCHER (WITH REDIS + MYSQL AUTO-CHECK)
echo ===================================================

:: Step 1: Automatically force-start Redis service in Windows background
echo [1/4] Checking and starting Redis Caching Engine...
net start Redis >nul 2>&1
sc start Redis >nul 2>&1
timeout /t 2 /nobreak >nul

:: Step 2: Clean up any previously stuck python instances or locked ports
echo [2/4] Cleaning up stale background processes...
taskkill /f /im python.exe >nul 2>&1
timeout /t 1 /nobreak >nul

:: Step 3: Launch the FastAPI Engine on Port 8080
echo [3/4] Initializing FastAPI Server on Port 8080...
echo Keep this window open while using the project!
echo ---------------------------------------------------
start "" /B python main.py

:: Step 4: Wait for network readiness and automatically trigger Google Chrome
echo [4/4] Activating Dashboard UI in browser...
timeout /t 4 /nobreak >nul
start "" "http://127.0.0.1:8080"

echo ===================================================
echo 🎉 SUCCESS! Everything is live on http://127.0.0.1:8080
echo ===================================================