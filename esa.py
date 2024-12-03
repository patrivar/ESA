import random

import story
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

    goal_port = all_airports[1:].copy()
    random.shuffle(goal_port)

    for i, goal_id in enumerate(goal_list):
        sql =  """INSERT INTO ports(game, airport, goal) 
                VALUES (%s, %s, %s);"""
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (game_id, goal_port[i]['ident'], goal_id))
    return game_id

def get_airport_info(icao):
    sql = """SELECT iso_country, ident, name, latitude_deg, longitude_deg
                FROM airport
                WHERE ident = %s"""
    cursor = conn.cursor(dictionary = True)
    cursor.execute(sql,(icao,))
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
    return distance.distance((start['latitude_deg'],start['longitude_deg']),
                             (end['latitude_deg'], end['longitude_deg'])).km

def airports_in_range(icao, all_ports, player_range):
    in_range = []
    for range in all_ports:
        dist = calculate_distance(icao,range['ident'])
        if dist <= player_range and not dist == 0:
            in_range.append(range)
    return in_range

def update_location(icao, player_points, user_money, game_id):
    sql = f"""UPDATE game SET location = %s, points = %s, money = %s WHERE id = %s"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao, player_points, user_money, game_id))

def chest_opened(current_airport, game_id):
    sql = "UPDATE ports SET opened = 1 WHERE airport = %s AND game = %s"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (current_airport, game_id))

player = input("Anna nimi: ")
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
letters = word(goal_letters, goal_word)
letter_display = []
word_display = ""

all_airports = get_airports()
start_airport = all_airports[0]['ident']
current_airport = start_airport

game_id = create_game(money, points, player_range, start_airport, player, all_airports)

storyline = input("Haluatko lukea tarinan? Kyllä = k tai paina enter ohittaaksesi.")
if storyline == 'k':
    input('\033[35mPaina Enter jatkaaksesi...\033[0m')
    for line in story.getStory():
        print(line)
input('\033[35mPaina Enter jatkaaksesi...\033[0m')

while not game_over:
    airport = get_airport_info(current_airport)
    print(f"Olet lentokentällä {airport['name']}")
    print(f"Sinulla on rahaa {money:.0f} ja pisteitä {points:.0f}")
    print(f"Kirjaimia löydetty: {word_display}")
    print(f"\033[32mAlku lentokenttäsi ICAO on: {start_airport}\033[0m")


    goal = check_goals(game_id, current_airport)
    if goal and goal['opened'] == 0:
        if money >= 50:
            question = input(f"Haluatko avata arkun hinnalla 50€? Kyllä = k , Ei = e: ")
            while question != 'k' and question != 'e':
                print("Vastaus ei ollut hyväksyttävä. Kokeile uudestaa.")
                question = input(f"Haluatko avata arkun hinnalla 50€? Kyllä = k , Ei = e: ")
            if question == "k":
                money -= 50
                if goal['money'] > 0:
                    money += goal['money']
                    print(f"Löysit {goal['name']}")
                    print(f"Sinulla on nyt rahaa {money:.0f}. ")
                    chest_opened(current_airport, game_id)
                elif goal['money'] == 0:
                    if goal['name'] == 'LETTER':
                        letters_found.append(letters[0][0])
                        letters[0].remove(letters[0][0])
                        print(f"Löysit kirjaimen {letters_found[-1]}")
                        word_display = ""
                        for j in letters[1]:
                            if j == letters_found[-1]:
                                word_display += j
                                letter_display.append(j)
                            elif j in letter_display:
                                word_display += j
                            else:
                                word_display += "_"
                        print(f"Löydetyt kirjaimet: {word_display}")
                        chest_opened(current_airport, game_id)
                    else:
                        print("Arkku oli tyhjä.")
                        chest_opened(current_airport, game_id)
                elif goal['name'] == 'BANDIT':
                    print("Arkkua avatessasi paikalle ilmestyi rosvo. Heitä noppaa koittaaksesi päästä karkuun")
                    input('\033[31mPaina Enter heittääksesi noppaa.\033[0m')
                    dice = random.randint(1,6)
                    if dice % 2 != 0:
                        money = 0
                        print("Menetit kaikki rahasi rosvolle.")
                        game_over = True
                    elif dice % 2 == 0 and dice != 6:
                        money = money / 2
                        print("Menetit puolet rahoistasi rosvolle.")
                        print(f"Sinulle jäi {money:.0f} euroa.")
                        chest_opened(current_airport, game_id)
                    else:
                        print("Pääsit karkuun.")
                        chest_opened(current_airport, game_id)

    input('\033[35mPaina Enter jatkaaksesi...\033[0m')
    if money >= 250 and points > 0:
        airports = airports_in_range(current_airport, all_airports, player_range)
        print(f'''\033[34mLento etäisyydellä olevia kenttiä: {len(airports)}: \033[0m''')
        for airport in airports:
            airport_distance = calculate_distance(current_airport, airport['ident'])
            icao_list.append(airport['ident'])
            print(f"{airport['name']}, ICAO: \033[34m{airport['ident']}\033[0m, etäisyys: {airport_distance:.0f}")
        destination = input("Anna lentokentän ICAO: ")
        destination = destination.upper()
        if destination not in icao_list:
            while destination not in icao_list:
                print("Antamasi vastaus ei kelpaa. Kokeile uudestaan.")
                destination = input("Anna lentokentän ICAO: ")
                destination = destination.upper()
        if destination in icao_list:
            money -= 250
            points -= 500
            update_location(current_airport, points, money, game_id)
            current_airport = destination
            icao_list.clear()
            if current_airport == start_airport:
                choice = input("Haluatko arvata sanan (kyllä = k, ei = e)? ")
                while choice != "k" and choice != "e":
                    print("Vastaus ei ollut hyväksyttävä. Kokeile uudestaan.")
                    choice = input("Haluatko arvata sanan (kyllä = k, ei = e)? ")
                if choice == "k":
                    attempts -= 1
                    guess = input("Arvaa sana: ")
                    if guess == letters[1]:
                        print("Arvasit sanan oikein.")
                        win = True
                        game_over = True
                    elif attempts == 0 and guess != letters[1]:
                        print("Arvasit sanan väärin ja arvaus kerrat pääsivät loppumaan.")
                        game_over = True
                    else:
                        if points > 0:
                            print("Arvasit sanan väärin. Jatka matkailua ja kokeile myöhemmin uudestaan.")
                            points -= 1000
                        else:
                            print("Arvasit väärin ja pisteesi tippuivat nollaan.")
                            points = 0
                            game_over = True

    else:
        if points > 0:
            print("Rahasi pääsivät loppumaan.")
        game_over = True
    if points == 0:
        print("Pisteesi tippuivat nollaan.")
        game_over = True

if game_over and win == True:
    print("Voitit pelin!")
    print(f"Sinulle jäi {points:.0f} pistettä ja {money:.0f} euroa.")
else:
    print("Hävisit pelin!")