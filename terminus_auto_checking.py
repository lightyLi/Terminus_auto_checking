import logging
import os
import time
import random
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import SQLiteSession
import google.generativeai as genai

from utils import logger

load_dotenv()

# 设置保存图片的文件夹
SAVE_PATH = './session/files'
session_path = './session'
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

# Use your own values from my.telegram.org
google_api = os.getenv('google_api')

chat_id = 5770101555
Bot_name = '@EmbyPublicBot'

def pic_dect(google_api: str, file_path: str, options: list) -> str:
    """
    使用Google Gemini模型识别图片并从给定选项中选择最匹配的选项
    
    Args:
        google_api: Google API密钥
        file_path: 图片文件路径
        options: 可选项列表
    
    Returns:
        str: 识别结果对应的选项编号
    """
    try:
        # 配置Google API
        genai.configure(api_key=google_api)
        
        # 上传图片文件
        sample_file = genai.upload_file(file_path)
        
        # 初始化Gemini模型
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        
        # 构建提示语
        prompt = (
            f"Identify the image and select the one you feel best fits the "
            "description from the several options I have provided, return its "
            f"number and do not reply any explanations.\nOptions: {options}"
        )
        
        # 获取模型响应
        response = model.generate_content([sample_file, prompt])
        
        return response.text.strip()
        
    except Exception as e:
        logging.error(f"图片识别失败: {str(e)}")
        return None

async def main(client):
    # 发送消息到指定chat ID
    await client.send_message(Bot_name, '/checkin')

async def message_handler(event):
    # 检查消息是否来自目标chat
    if event.sender_id == (await client.get_entity(Bot_name)).id:
        # 检查消息是否包含图片
        if event.message.media:
            # 下载图片
            path = await event.message.download_media(SAVE_PATH)
            logger.info(f'****Pic save to: {path}****')
            time.sleep(2 + random.randint(0, 2))
            # 获取按钮选项
            if hasattr(event.message, 'reply_markup') and event.message.reply_markup:
                buttons = event.message.reply_markup.rows
                options = []
                for row in buttons:
                    for button in row.buttons:
                        options.append(button.text)
                
                logger.info(f'****Options: {options}****')
                
                # 使用pic_dect识别图片
                result = pic_dect(google_api, path, options)
                if result:
                    try:
                        # 将识别结果转为数字索引(1-4)
                        button_index = int(result) - 1
                        if 0 <= button_index < len(options):
                            # 点击对应按钮
                            await event.click(button_index)
                            logger.info(f'****Selected: {result}: {options[button_index]}****')
                        else:
                            logger.info(f'****Invalid option index: {result}****')
                    except ValueError:
                        logger.info(f'****Cannot parse recognition result: {result}****')
                else:
                    logger.info('****Pic dect failed****')
                time.sleep(2 + random.randint(0, 2))

async def start_client(client):
    await client.start()
    await asyncio.sleep(20)  # 等待15秒后断开连接
    await client.disconnect()

# 多账号配置，根据.env文件中的变量名获取不同用户的数据
sessions = [value for key, value in os.environ.items() if key.startswith('session_')]
api_ids = [value for key, value in os.environ.items() if key.startswith('api_id')]
api_hashes = [value for key, value in os.environ.items() if key.startswith('api_hash')]

accounts = [
    {'session':session, 'api_id': api_id, 'api_hash': api_hash}  \
    for session, api_id, api_hash in zip(sessions, api_ids, api_hashes)
]

# 遍历处理每个账号
for account in accounts:
    client = TelegramClient(SQLiteSession(f"{session_path}/{account['session']}"),
                            account['api_id'], account['api_hash'])
    client.add_event_handler(message_handler, events.NewMessage())
    with client:
        client.loop.run_until_complete(main(client))
        client.loop.run_until_complete(start_client(client))
    logger.info(f"Account {account['session']} finished, sleeping...")
    time.sleep(30)  # 每个账号处理完后休息30秒

logger.info('All accounts finished')

# 清理保存的图片
for file in os.listdir(SAVE_PATH):
    if file.endswith('.jpg') or file.endswith('.png'):
        try:
            os.remove(os.path.join(SAVE_PATH, file))
        except Exception as e:
            logger.info(f'Deleting {file} failed: {e}')
logger.info(f'All images in {SAVE_PATH} cleaned up')
