import os
import sys
import subprocess
import ctypes

# 获取程序自身文件名，构建对应的ini文件名
executable_name = os.path.basename(sys.argv[0])
# 去掉扩展名
name_prefix = os.path.splitext(executable_name)[0]
# 构建ini文件名
ini_file = f'{name_prefix}.ini'

# 检查配置文件是否存在，不存在则生成默认配置
if not os.path.exists(ini_file):
    try:
        # 构建默认的target路径：自身文件名文件夹/自身文件名.exe
        default_target = f'{name_prefix}/{name_prefix}.exe'
        with open(ini_file, 'w', encoding='utf-8') as f:
            f.write('; 配置文件范例\n')
            f.write('; target=要启动的程序路径\n')
            f.write(f'target={default_target}\n')
    except Exception as e:
        # 无控制台版本无法打印，直接退出
        sys.exit(1)

# 读取配置文件
try:
    with open(ini_file, 'r', encoding='utf-8') as f:
        content = f.read()
except Exception as e:
    sys.exit(1)

# 解析配置
target = ''
for line in content.split('\n'):
    line = line.strip()
    if not line or line.startswith(';') or line.startswith('#'):
        continue
    if '=' in line:
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()
        if key == 'target':
            target = value
            break

if not target:
    print('配置文件中未找到target项')
    sys.exit(1)

# 启动目标程序
try:
    # 检测是否为网址（带http或不带http的网址）
    lower_target = target.lower()
    if (lower_target.startswith('http://') or lower_target.startswith('https://') or 
        lower_target.startswith('www.') or '.' in lower_target and lower_target.count('.') >= 1):
        # 可能是网址，尝试用浏览器打开
        subprocess.Popen(f'start {target}', shell=True)
    elif os.path.exists(target):
        # 是本地文件，使用start命令打开（Windows会用默认打开方式处理）
        # 支持所有文件类型，包括appx、exe、jpg、docx等
        subprocess.Popen(f'start "" "{target}"', shell=True)
    else:
        # 显示Windows消息框提示文件不存在
        ctypes.windll.user32.MessageBoxW(
            0,
            f"指定的文件或网址不存在: {target}",
            "错误",
            0x10  # MB_ICONERROR
        )
except Exception as e:
    # 显示Windows消息框提示启动失败
    ctypes.windll.user32.MessageBoxW(
        0,
        f"无法打开 {target}: {str(e)}",
        "错误",
        0x10  # MB_ICONERROR
    )
    sys.exit(1)