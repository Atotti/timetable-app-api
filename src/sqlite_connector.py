"""
$ sqlite3 sqlite3.db
でdbに入れるので楽だよ
"""

import sqlite3
import csv

def create_tables(cur):
    with open("../data/table_settings.sql", "r", encoding="utf-8") as stgfile:
        sqlstr=stgfile.read()
        cur.executescript(sqlstr)
    return cur.fetchall()

def insert_lecture_rooms(cur):
    # CSVファイルを開く
    with open('../data/lecture_rooms.csv', 'r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        # CSVファイルの各行をデータベースに挿入
        for row in csv_reader:
            cur.execute("INSERT INTO lecture_rooms (campus, building, room_id) VALUES (?, ?, ?)", row)

def insert_classroom_allocation(cur):
    # CSVファイルを開く
    with open('../data/classroom_allocation.csv', 'r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        # CSVファイルの各行をデータベースに挿入
        for row in csv_reader:
            cur.execute("INSERT INTO classroom_allocation (lecture_id, campus, building, room_id) VALUES (?, ?, ?, ?)", row)

def insert_syllabus_base_info(cur):
    # CSVファイルを開く
    with open('../data/syllabus_base_info.tsv', 'r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        next(csv_reader)

        # CSVファイルの各行をデータベースに挿入
        for row in csv_reader:
            cur.execute("INSERT INTO syllabus_base_info (year, season, day, period, teacher, name, lecture_id, credits, url, type, faculty) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)

def insert_syllabus_base_info_splited_by_day_and_period(cur):
    # CSVファイルを開く
    with open('../data/syllabus_base_info_splited_by_day_and_period.tsv', 'r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        next(csv_reader)

        # CSVファイルの各行をデータベースに挿入
        for row in csv_reader:
            cur.execute("INSERT INTO syllabus_base_info_splited_by_day_and_period (year, season, day, period, teacher, name, lecture_id, credits, url, type, faculty) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)

if __name__=="__main__":
    # SQLiteデータベースに接続
    conn = sqlite3.connect("sqlite3.db")
    cur = conn.cursor()

    create_tables(cur)
    insert_lecture_rooms(cur)
    insert_classroom_allocation(cur)
    insert_syllabus_base_info(cur)
    insert_syllabus_base_info_splited_by_day_and_period(cur)

    # 変更をコミット
    conn.commit()

    # データベース接続を閉じる
    conn.close()