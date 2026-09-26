@echo off
title PocketBase Server (:5050)
echo ========================================================
echo         PocketBase 资源库服务已启动 (端口: 5050)
echo ========================================================
echo.
echo 浏览器直接打开 (自动进入后台):
echo   http://127.0.0.1:5050/
echo.
echo 管理后台直链:
echo   http://127.0.0.1:5050/_/
echo.
echo REST API 数据接口根路径:
echo   http://127.0.0.1:5050/api/
echo.
echo 按 Ctrl+C 可停止服务
echo.
"%~dp0pocketbase.exe" serve --http="0.0.0.0:5050"
pause
