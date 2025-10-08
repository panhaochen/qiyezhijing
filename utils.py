import json
import logging
from datetime import datetime
from typing import Any, Dict

def setup_logging():
    """设置日志配置"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('enterprise_mirror.log'),
            logging.StreamHandler()
        ]
    )

def save_analysis_result(company_name: str, result: Dict[str, Any]):
    """保存分析结果"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"analysis_{company_name}_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    logging.info(f"分析结果已保存至: {filename}")

def load_config():
    """加载配置文件"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"api_keys": {}, "settings": {}}