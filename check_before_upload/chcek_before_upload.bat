
@echo off 
rem 关闭自动输出
:begin

echo 本页面将持续运行
echo 直接拖入需要检查的文件夹即可
echo 工具将自动删除非法文件
echo 并检查文件内的所有xml
echo xml问题将显示在末尾

rem 接收输入

set input=
set /p input=请拖入待检查主题解压后的文件夹:

rem 输出得到的输入信息

echo 正在检查的包是：%input%
python check_xml.py %input%

rem pause>null

echo.

rem 从begin标签出，再次运行

goto begin