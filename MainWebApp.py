from flask import Flask, jsonify, request, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('hgwbanners.db')
    conn.row_factory = sqlite3.Row
    return conn

def calc_remaining_time(end_date):
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
    now = datetime.now()
    remaining_time = end_date_dt - now
    return remaining_time.days

@app.route('/')
def index():
    conn = get_db_connection()
    