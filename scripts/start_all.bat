@echo off
setlocal
cd /d "%~dp0.."

start "order-system-backend" cmd /k scripts\start_backend.bat
start "order-system-frontend" cmd /k scripts\start_frontend_dev.bat
