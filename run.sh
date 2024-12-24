#!/bin/bash

# 定义虚拟环境名称和脚本路径
ENV_NAME="emby_checking"        # 替换为你的 Conda 虚拟环境名称
SCRIPT_PATH="/Users/lighty/Documents/CODE/Python/Terminus_auto_checking/terminus_auto_checking.py"  # 替换为你的 Python 脚本路径


# 激活 Conda 环境
source /Users/lighty/miniconda3/etc/profile.d/conda.sh  # 替换为你的 Conda 安装路径

conda activate "$ENV_NAME"

# 检查环境是否成功激活
if [ $? -ne 0 ]; then
    echo "Failed to activate Conda environment: $ENV_NAME"
    exit 1
fi

python "$SCRIPT_PATH"

# 检查脚本是否运行成功
if [ $? -ne 0 ]; then
    echo "Script failed: $SCRIPT_PATH"
    conda deactivate
    exit 1
fi

# 退出 Conda 环境
conda deactivate

# 成功提示
echo "Script executed successfully and exited the Conda environment."
