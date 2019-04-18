# Huawei_theme_package_utils_v9.x
华为主题包制作-工具集合


# 环境条件

python27

~~7z（压缩hwt包用，打包文件压缩格式有问题，已改用gunwin32中的zip unzip 支持）~~

gunwin32 bin目录添加到path环境变量

# 1.windows 下安装choco

cmd下:

@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"



# 2.choco安装python2.7


# ~~3.choco安装7z~~


# 4.choco安装pip


# 5.pip 修改国内源


# 打包：
界面编辑处理完毕的主题包文件夹   
放至theme_nopackage 文件夹
点击 打包.bat 运行 
生成的hwt文件在theme_package文件夹下


# 解包：
hwt文件放置到theme_package文件夹下 ，
点击 解包.bat 运行
生成的文件夹放置在 theme_nopackage 文件夹下

# Icon批量重命名：
### (相关文件夹 orgin_name_file , trans_name_file)
将原始icon系列图片放置到 orgin_name_file 文件夹内，
并配置好icon_rename_file.conf 文件
点击 批量换名.bat 运行
运行后的系列文件保存至  trans_name_file



# TODO：

测试工具
