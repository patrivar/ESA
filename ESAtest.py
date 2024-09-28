import random
#import story
from geopy import distance

import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='demogame_1',
    user='root',
    password='moonS20-un14',
    autocommit=True,
    collation='utf8mb4_general_ci'
)


def get_airports():
    sql = ("SELECT name, ident, type, iso_country, longitude_deg, latitude_deg "
           "FROM airport "
           "Where continent = 'EU' "
           "AND type = 'large_airport'"
           "ORDER BY RAND() LIMIT 22;")
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_goals():
    sql = ("SELECT * FROM goals;")
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def word():
    sql = ("select word from word_list ORDER BY RAND() LIMIT 1;")
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    rows = cursor.fetchone()
    list1 = []
    for i in rows['word']:
        list1.append(i)
    return list1


def create_game(start_money, player_points, current_airport, player_name, all_airports):
    sql = ("INSERT INTO game (money, points, location, screen_name)"
           "VALUES (start_money, player_points, current_airport, player_name);")
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    game_id = cursor.lastrowid

    goals = get_goals()


'''name = input("Anna nimi: ")
points = 20000
money = 2000
'''

# print(word())
# print(get_airports())