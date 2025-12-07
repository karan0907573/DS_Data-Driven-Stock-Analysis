import mysql.connector
import pandas as pd
from datetime import date

DB_CONFIG = {
    "host": "localhost",   # Or the IP address of your MySQL server
    "user": "root",
    "password": "Karan09",
    "database": "stock_analysis" 
}
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def fetchone(query, params=()):
    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor(dictionary=True,buffered=True)
    cur.execute(query, params)
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def fetchall(query, params=()):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def execute(query, params=()):
    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    lastid = cur.lastrowid
    cur.close()
    conn.close()
    return lastid

def get_stock_data():
    query = "SELECT ticker as Ticker,close,date,high,low,month,open,volume FROM stock_data"
    return pd.DataFrame(fetchall(query))

def get_sector_data():
    query = "SELECT Company,Ticker,Sector,Symbol FROM sector_data"
    return pd.DataFrame(fetchall(query))