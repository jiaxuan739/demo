"""数据库配置"""
import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root123456',
    'database': 'wms_db',
    'charset': 'utf8mb4',
}


def get_connection():
    """获取数据库连接"""
    return mysql.connector.connect(**DB_CONFIG)
