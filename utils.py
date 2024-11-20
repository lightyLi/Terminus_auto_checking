import logging
import os

# 生成日志文件名
log_filename = './Terminus_checking_log.log'

def setup_logger():
    # 配置logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# 创建全局logger实例
logger = setup_logger()