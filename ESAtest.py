import random
#import story
from geopy import distance

import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='demogame1',
    user='root',
    password='tatti',
    autocommit=True,
    collation='utf8mb4_general_ci'
)


def get_airports():
    sql = """SELECT name, ident, type, iso_country, longitude_deg, latitude_deg 
           FROM airport 
           Where continent = 'EU'
           AND type = 'large_airport'
           ORDER BY RAND() LIMIT 22;"""
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
    sql = """SELECT word FROM word_list ORDER BY RAND() LIMIT 1;"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    rows = cursor.fetchone()
    list1 = []
    for i in rows['word']:
        list1.append(i)
    return list1


def create_game(start_money, player_points, player_range, current_airport, player_name, all_airports):
    sql = """INSERT INTO game (money, location, screen_name, points, player_range)
           VALUES (%s,%s,%s,%s,%s);"""
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
        sql =  """INSERT INTO ports(game, airport, goal) 
                VALUES (%s, %s, %s);)"""
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (game_id, goal_port[i]['ident'], goal_id))
        return game_id

def get_airport_info(icao):
    sql = """SELECT iso_country, ident, name, latitude_deg, longitud_deg
                FROM airport
                WHERE ident = %s"""
    cursor = conn.cursor(dictionary = True)
    cursor.execute(sql,(icao,))
    result = cursor.fetchone()
    return result

def calculate_distance(current, target):
    start = get_airport_info(current)
    end = get_airport_info(target)
    return distance.distance((start['longitude_deg'],start['latitude_deg'])
                             (end['longitude_deg'], end['latitude_deg'])).km

def airports_in_range(icao,all_ports,player_range):
    in_range = []
    for in_range in in_range:
        dist = calculate_distance(icao,all_ports['ident'])
        if dist < player_range and not dist == 0:
            in_range.append(in_range)
        return in_range

player = input("Anna nimi: ")
points = 20000
money = 2000
player_range = 0
game_over = False
win = False

all_airports = get_airports()
start_airport = all_airports[0]['ident']
current_airport = start_airport

game_id = create_game(money, points, player_range, start_airport, player, all_airports)

# print(word())
# print(get_airports())