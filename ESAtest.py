import random
#import story
from geopy import distance

import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='demogame_1',
    user='root',
    password='K4rhuKu0l131l3n',
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
    sql = ("SELECT * FROM goal;")
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


def create_game(start_money, player_points, player_range, current_airport, player_name, all_airports):
    sql = ("INSERT INTO game (money, location, screen_name, points, player_range)"
           "VALUES (%s,%s,%s,%s,%s);")
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (start_money, current_airport, player_name, player_points, player_range))
    game_id = cursor.lastrowid

    goals = get_goals()
    goal_list = []
    for goal in goals:
        for i in range(0,goal['probability'], 1):
            goal_list.append(goal['id'])

    # exclude starting airport
    goal_port = all_airports[1:].copy()
    random.shuffle(goal_port)

    for i, goal_id in enumerate(goal_list):
        sql =  ("INSERT INTO ports(game, airport, goal) "
                "VALUES (%s, %s, %s);)")
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (game_id, goal_port[i]['ident'], goal_id))
    return game_id




player = input("Anna nimi: ")
points = 20000
money = 2000
player_range = 0

all_airports = get_airports()
start_airport = all_airports[0]['ident']
current_airport = start_airport

game_id = create_game(money, points, player_range, start_airport, player, all_airports)

# print(word())
# print(get_airports())