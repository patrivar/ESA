import random
from flask import Flask, Response, jsonify, request
import json
from flask_cors import CORS
import story
from geopy import distance
import mysql.connector

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='demogame_1',
    user='root',
    password='K4rhuKu0l131l3n',
    autocommit=True,
    collation='utf8mb4_general_ci'
)

points = 20000
money = 3000
player_range = 2500
attempts = 3
game_over = False
win = False
icao_list = []
letters_found = []
goal_letters = []
goal_word = ""
letter_display = []
word_display = ""

@app.route('/getAirports')
def get_airports():
    sql = """SELECT name, ident, type, iso_country, longitude_deg, latitude_deg 
           FROM airport 
           WHERE continent = 'EU'
           AND type = 'large_airport'
           ORDER BY RAND() LIMIT 22;"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def get_goals():
    sql = "SELECT * FROM goal;"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def word(missing_letters, goal_word):
    sql = """SELECT word FROM word_list ORDER BY RAND() LIMIT 1;"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    rows = cursor.fetchone()
    missing_letters = []
    goal_word = rows['word']
    for i in rows['word']:
        missing_letters.append(i)
    return missing_letters, goal_word

@app.route('/newGame/<player_name>')
def create_game(player_name):
    print(player_name)

    all_airports = get_airports()
    print(all_airports)
    start_airport = all_airports[0]['ident']
    print(start_airport)
    current_airport = start_airport

    # def create_game(start_money, player_points, player_range, current_airport, player_name, all_airports):
    sql = """INSERT INTO game (money, location, screen_name, points, player_range)
           VALUES (%s,%s,%s,%s,%s);"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (money, current_airport, player_name, points, player_range))
    game_id = cursor.lastrowid

    goals = get_goals()
    goal_list = []
    for goal in goals:
        for i in range(0, goal['probability'], 1):
            goal_list.append(goal['id'])

    goal_port = all_airports[1:].copy()
    random.shuffle(goal_port)

    for i, goal_id in enumerate(goal_list):
        sql = """INSERT INTO ports(game, airport, goal) 
                VALUES (%s, %s, %s);"""
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (game_id, goal_port[i]['ident'], goal_id))
    status = 200
    result = {
        "status": status,
        "airports": all_airports,
        "current": current_airport,
        "money": money,
        "points": points,
        "range": player_range,
        "name": player_name,
        "game_id": game_id
    }
    json_result = json.dumps(result)
    return Response(json_result, status=status, mimetype='application/json')

def get_airport_info(icao):
    sql = """SELECT iso_country, ident, name, latitude_deg, longitude_deg
                FROM airport
                WHERE ident = %s"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return result

def check_goals(game_id, current_airport):
    sql = """SELECT ports.id, name, money, opened FROM ports, goal 
           WHERE goal.id = ports.goal 
           AND game = %s 
           AND airport = %s;"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (game_id, current_airport))
    result = cursor.fetchone()
    if result == None:
        return False
    return result

def calculate_distance(current, target):
    start = get_airport_info(current)
    end = get_airport_info(target)
    return distance.distance((start['latitude_deg'], start['longitude_deg']),
                             (end['latitude_deg'], end['longitude_deg'])).km

def airports_in_range(icao, all_ports, player_range):
    in_range = []
    for range in all_ports:
        dist = calculate_distance(icao, range['ident'])
        if dist <= player_range and not dist == 0:
            in_range.append(range)
    return in_range

@app.route('/update', methods=['GET'])
def update_location():
    icao = request.args.get('icao')
    game_id = request.args.get('game_id')
    player_points = request.args.get('points', default=0, type=int)
    user_money = request.args.get('money', default=0, type=int)

    if not icao or not game_id:
        return Response("Missing parameters", status=400)

    try:
        sql = """UPDATE game SET location = %s, points = %s, money = %s WHERE id = %s"""
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (icao, player_points, user_money, game_id))
        conn.commit()

        sql = """SELECT * FROM game WHERE id = %s"""
        cursor.execute(sql, (game_id,))
        game_state = cursor.fetchone()

        if game_state is None:
            return Response("Game state not found", status=404)

        all_airports = get_airports()

        result = {
            "game_state": game_state,
            "all_airports": all_airports
        }
        return jsonify(result)
    except Exception as e:
        return Response(str(e), status=500)

def chest_opened(current_airport, game_id):
    sql = "UPDATE ports SET opened = 1 WHERE airport = %s AND game = %s"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (current_airport, game_id))

if __name__ == "__main__":
    app.run(use_reloader=True, host='127.0.0.1', port=3000)