#!python3
# -*- coding: utf-8 -*- 
from logging import logProcesses
from flask import Flask, render_template, request, make_response, redirect
import random
import requests
import json
import datetime
import sys

from werkzeug.utils import xhtml
from apscheduler.schedulers.background import BackgroundScheduler

class player:
    def __init__(self, name=None, nuri_pt=None, assist_pt=None, kill_pt=None, death_pt=None, nuri_pt_before=None, assist_pt_before=None, kill_pt_before=None, death_pt_before=None, win_pt=None, total_pt=None):
        self.name = name
        self.nuri_pt = nuri_pt
        self.kill_pt = kill_pt
        self.assist_pt = assist_pt
        self.death_pt = death_pt
        self.nuri_pt_before = nuri_pt_before
        self.kill_pt_before = kill_pt_before
        self.assist_pt_before = assist_pt_before
        self.death_pt_before = death_pt_before
        self.win_pt = win_pt
        self.total_pt = total_pt

login_name = ""

player1 = player()
player2 = player()
player3 = player()
player4 = player()
player5 = player()
player6 = player()
player7 = player()
player8 = player()

end_time = None
stage=None

f = 0
id = 0

app = Flask(__name__, static_url_path='/static')

def test_job():
    r = requests.get('https://stat.ink/api/v2/battle?screen_name=' + login_name)
    # d = json.loads(r)
    d = r.json()

    global id
    global f
    global end_time
    global stage

    me_winlose = d[0]['result']
    if me_winlose == "win":
        other_winlose = "lose"
    else:
        other_winlose = "win"

    if id == d[0]['id']:
        return
    else:
        id = d[0]['id']
        end_time=str((datetime.datetime.fromtimestamp(d[0]['end_at']['time'], datetime.timezone(datetime.timedelta(hours=9))))).split("+")[0]
        stage=d[0]['map']['name']['ja_JP']

    if f == 0:  #初回
        player1.name = d[0]['players'][0]['name']
        player1.nuri_pt = d[0]['players'][0]['point']
        player1.kill_pt = d[0]['players'][0]['kill']
        player1.assist_pt = d[0]['players'][0]['kill_or_assist'] - d[0]['players'][0]['kill']
        player1.death_pt = d[0]['players'][0]['death']
        player1.win_pt = get_win_pt(me_winlose, other_winlose, d, 0)

        player2.name = d[0]['players'][1]['name']
        player2.nuri_pt = d[0]['players'][1]['point']
        player2.kill_pt = d[0]['players'][1]['kill']
        player2.assist_pt = d[0]['players'][1]['kill_or_assist'] - d[0]['players'][1]['kill']
        player2.death_pt = d[0]['players'][1]['death']
        player2.win_pt = get_win_pt(me_winlose, other_winlose, d, 1)

        player3.name = d[0]['players'][2]['name']
        player3.nuri_pt = d[0]['players'][2]['point']
        player3.kill_pt = d[0]['players'][2]['kill']
        player3.assist_pt = d[0]['players'][2]['kill_or_assist'] - d[0]['players'][2]['kill']
        player3.death_pt = d[0]['players'][2]['death']
        player3.win_pt = get_win_pt(me_winlose, other_winlose, d, 2)

        player4.name = d[0]['players'][3]['name']
        player4.nuri_pt = d[0]['players'][3]['point']
        player4.kill_pt = d[0]['players'][3]['kill']
        player4.assist_pt = d[0]['players'][3]['kill_or_assist'] - d[0]['players'][3]['kill']
        player4.death_pt = d[0]['players'][3]['death']
        player4.win_pt = get_win_pt(me_winlose, other_winlose, d, 3)

        player5.name = d[0]['players'][4]['name']
        player5.nuri_pt = d[0]['players'][4]['point']
        player5.kill_pt = d[0]['players'][4]['kill']
        player5.assist_pt = d[0]['players'][4]['kill_or_assist'] - d[0]['players'][4]['kill']
        player5.death_pt = d[0]['players'][4]['death']
        player5.win_pt = get_win_pt(me_winlose, other_winlose, d, 4)

        player6.name = d[0]['players'][5]['name']
        player6.nuri_pt = d[0]['players'][5]['point']
        player6.kill_pt = d[0]['players'][5]['kill']
        player6.assist_pt = d[0]['players'][5]['kill_or_assist'] - d[0]['players'][5]['kill']
        player6.death_pt = d[0]['players'][5]['death']
        player6.win_pt = get_win_pt(me_winlose, other_winlose, d, 5)

        player7.name = d[0]['players'][6]['name']
        player7.nuri_pt = d[0]['players'][6]['point']
        player7.kill_pt = d[0]['players'][6]['kill']
        player7.assist_pt = d[0]['players'][6]['kill_or_assist'] - d[0]['players'][6]['kill']
        player7.death_pt = d[0]['players'][6]['death']
        player7.win_pt = get_win_pt(me_winlose, other_winlose, d, 6)

        player8.name = d[0]['players'][7]['name']
        player8.nuri_pt = d[0]['players'][7]['point']
        player8.kill_pt = d[0]['players'][7]['kill']
        player8.assist_pt = d[0]['players'][7]['kill_or_assist'] - d[0]['players'][7]['kill']
        player8.death_pt = d[0]['players'][7]['death']
        player8.win_pt = get_win_pt(me_winlose, other_winlose, d, 7)

        f = 1
    else:   #2回目以降
        for i in range(8):
            if player1.name == d[0]['players'][i]['name']:
                player1.nuri_pt += d[0]['players'][i]['point']
                player1.kill_pt += d[0]['players'][i]['kill']
                player1.assist_pt += d[0]['players'][i]['kill_or_assist'] - d[0]['players'][i]['kill']
                player1.death_pt += d[0]['players'][i]['death']
                player1.win_pt += get_win_pt(me_winlose, other_winlose, d, 0)

            elif player2.name == d[0]['players'][i]['name']:
                player2.nuri_pt += d[0]['players'][i]['point']
                player2.kill_pt += d[0]['players'][i]['kill']
                player2.assist_pt += d[0]['players'][i]['kill_or_assist'] - d[0]['players'][i]['kill']
                player2.death_pt += d[0]['players'][i]['death']
                player2.win_pt += get_win_pt(me_winlose, other_winlose, d, 1)

            elif player3.name == d[0]['players'][i]['name']:
                player3.nuri_pt += d[0]['players'][i]['point']
                player3.kill_pt += d[0]['players'][i]['kill']
                player3.assist_pt += d[0]['players'][i]['kill_or_assist'] - d[0]['players'][i]['kill']
                player3.death_pt += d[0]['players'][i]['death']
                player3.win_pt += get_win_pt(me_winlose, other_winlose, d, 2)

            elif player4.name == d[0]['players'][i]['name']:
                player4.nuri_pt += d[0]['players'][i]['point']
                player4.kill_pt += d[0]['players'][i]['kill']
                player4.assist_pt += d[0]['players'][i]['kill_or_assist'] - d[0]['players'][i]['kill']
                player4.death_pt += d[0]['players'][i]['death']
                player4.win_pt += get_win_pt(me_winlose, other_winlose, d, 3)

            elif player5.name == d[0]['players'][i]['name']:
                player5.nuri_pt += d[0]['players'][i]['point']
                player5.kill_pt += d[0]['players'][i]['kill']
                player5.assist_pt += d[0]['players'][i]['kill_or_assist'] - d[0]['players'][i]['kill']
                player5.death_pt += d[0]['players'][i]['death']
                player5.win_pt += get_win_pt(me_winlose, other_winlose, d, 4)

            elif player6.name == d[0]['players'][i]['name']:
                player6.nuri_pt += d[0]['players'][i]['point']
                player6.kill_pt += d[0]['players'][i]['kill']
                player6.assist_pt += d[0]['players'][i]['kill_or_assist'] - d[0]['players'][i]['kill']
                player6.death_pt += d[0]['players'][i]['death']
                player6.win_pt += get_win_pt(me_winlose, other_winlose, d, 5)

            elif player7.name == d[0]['players'][i]['name']:
                player7.nuri_pt += d[0]['players'][i]['point']
                player7.kill_pt += d[0]['players'][i]['kill']
                player7.assist_pt += d[0]['players'][i]['kill_or_assist'] - d[0]['players'][i]['kill']
                player7.death_pt += d[0]['players'][i]['death']
                player7.win_pt += get_win_pt(me_winlose, other_winlose, d, 6)

            elif player8.name == d[0]['players'][i]['name']:
                player8.nuri_pt += d[0]['players'][i]['point']
                player8.kill_pt += d[0]['players'][i]['kill']
                player8.assist_pt += d[0]['players'][i]['kill_or_assist'] - d[0]['players'][i]['kill']
                player8.death_pt += d[0]['players'][i]['death']
                player8.win_pt += get_win_pt(me_winlose, other_winlose, d, 7)


    player1.nuri_pt_before = 0
    player1.kill_pt_before = 0
    player1.assist_pt_before = 0
    player1.death_pt_before = 0

    player2.nuri_pt_before = 0
    player2.kill_pt_before = 0
    player2.assist_pt_before = 0
    player2.death_pt_before = 0

    player3.nuri_pt_before = 0
    player3.kill_pt_before = 0
    player3.assist_pt_before = 0
    player3.death_pt_before = 0

    player4.nuri_pt_before = 0
    player4.kill_pt_before = 0
    player4.assist_pt_before = 0
    player4.death_pt_before = 0

    player5.nuri_pt_before = 0
    player5.kill_pt_before = 0
    player5.assist_pt_before = 0
    player5.death_pt_before = 0

    player6.nuri_pt_before = 0
    player6.kill_pt_before = 0
    player6.assist_pt_before = 0
    player6.death_pt_before = 0

    player7.nuri_pt_before = 0
    player7.kill_pt_before = 0
    player7.assist_pt_before = 0
    player7.death_pt_before = 0

    player8.nuri_pt_before = 0
    player8.kill_pt_before = 0
    player8.assist_pt_before = 0
    player8.death_pt_before = 0

    for i in range(8):
        if player1.name == d[0]['players'][i]['name']:
            player1.nuri_pt_before = d[0]['players'][i]['point']
            player1.kill_pt_before = d[0]['players'][i]['kill']
            player1.assist_pt_before = d[0]['players'][i]['kill_or_assist'] - d[0]['players'][0]['kill']
            player1.death_pt_before = d[0]['players'][i]['death']

        elif player2.name == d[0]['players'][i]['name']:
            player2.nuri_pt_before = d[0]['players'][i]['point']
            player2.kill_pt_before = d[0]['players'][i]['kill']
            player2.assist_pt_before = d[0]['players'][i]['kill_or_assist'] - d[0]['players'][1]['kill']
            player2.death_pt_before = d[0]['players'][i]['death']

        elif player3.name == d[0]['players'][i]['name']:
            player3.nuri_pt_before = d[0]['players'][i]['point']
            player3.kill_pt_before = d[0]['players'][i]['kill']
            player3.assist_pt_before = d[0]['players'][i]['kill_or_assist'] - d[0]['players'][2]['kill']
            player3.death_pt_before = d[0]['players'][i]['death']

        elif player4.name == d[0]['players'][i]['name']:
            player4.nuri_pt_before = d[0]['players'][i]['point']
            player4.kill_pt_before = d[0]['players'][i]['kill']
            player4.assist_pt_before = d[0]['players'][i]['kill_or_assist'] - d[0]['players'][3]['kill']
            player4.death_pt_before = d[0]['players'][i]['death']

        elif player5.name == d[0]['players'][i]['name']:
            player5.nuri_pt_before = d[0]['players'][i]['point']
            player5.kill_pt_before = d[0]['players'][i]['kill']
            player5.assist_pt_before = d[0]['players'][i]['kill_or_assist'] - d[0]['players'][4]['kill']
            player5.death_pt_before = d[0]['players'][i]['death']

        elif player6.name == d[0]['players'][i]['name']:
            player6.nuri_pt_before = d[0]['players'][i]['point']
            player6.kill_pt_before = d[0]['players'][i]['kill']
            player6.assist_pt_before = d[0]['players'][i]['kill_or_assist'] - d[0]['players'][5]['kill']
            player6.death_pt_before = d[0]['players'][i]['death']

        elif player7.name == d[0]['players'][i]['name']:
            player7.nuri_pt_before = d[0]['players'][i]['point']
            player7.kill_pt_before = d[0]['players'][i]['kill']
            player7.assist_pt_before = d[0]['players'][i]['kill_or_assist'] - d[0]['players'][6]['kill']
            player7.death_pt_before = d[0]['players'][i]['death']

        elif player8.name == d[0]['players'][i]['name']:
            player8.nuri_pt_before = d[0]['players'][i]['point']
            player8.kill_pt_before = d[0]['players'][i]['kill']
            player8.assist_pt_before = d[0]['players'][i]['kill_or_assist'] - d[0]['players'][7]['kill']
            player8.death_pt_before = d[0]['players'][i]['death']
        


scheduler = BackgroundScheduler()
job = scheduler.add_job(test_job, 'interval', minutes=1)
scheduler.start()


@app.route('/update', methods=['GET'])
def update():
    test_job()
    return index()

@app.route('/')
def index():
    if player1.name == None:
        return render_template('blank.html')

    p_nuri = [player1, player2, player3, player4,
            player5, player6, player7, player8]
    nuri = sorted(p_nuri, key=lambda val : val.nuri_pt, reverse=True)

    p_kill = [player1, player2, player3, player4,
            player5, player6, player7, player8]
    kill = sorted(p_kill, key=lambda val : val.kill_pt, reverse=True)

    p_assist = [player1, player2, player3, player4,
            player5, player6, player7, player8]
    assist = sorted(p_assist, key=lambda val : val.assist_pt, reverse=True)

    p_death = [player1, player2, player3, player4,
            player5, player6, player7, player8]
    death = sorted(p_death, key=lambda val : val.death_pt, reverse=True)

    p_win = [player1, player2, player3, player4,
            player5, player6, player7, player8]
    win = sorted(p_win, key=lambda val : val.win_pt, reverse=True)


    player1.total_pt = (10 - get_pos(player1.name, nuri)) + \
                (10 - get_pos(player1.name, kill)) + \
                (10 - get_pos(player1.name, assist)) + \
                (10 - get_pos(player1.name, win)) + \
                (get_pos(player1.name, death) + 3)
    player2.total_pt = (10 - get_pos(player2.name, nuri)) + \
                (10 - get_pos(player2.name, kill)) + \
                (10 - get_pos(player2.name, assist)) + \
                (10 - get_pos(player2.name, win)) + \
                (get_pos(player2.name, death) + 3)
    player3.total_pt = (10 - get_pos(player3.name, nuri)) + \
                (10 - get_pos(player3.name, kill)) + \
                (10 - get_pos(player3.name, assist)) + \
                (10 - get_pos(player3.name, win)) + \
                (get_pos(player3.name, death) + 3)
    player4.total_pt = (10 - get_pos(player4.name, nuri)) + \
                (10 - get_pos(player4.name, kill)) + \
                (10 - get_pos(player4.name, assist)) + \
                (10 - get_pos(player4.name, win)) + \
                (get_pos(player4.name, death) + 3)
    player5.total_pt = (10 - get_pos(player5.name, nuri)) + \
                (10 - get_pos(player5.name, kill)) + \
                (10 - get_pos(player5.name, assist)) + \
                (10 - get_pos(player5.name, win)) + \
                (get_pos(player5.name, death) + 3)
    player6.total_pt = (10 - get_pos(player6.name, nuri)) + \
                (10 - get_pos(player6.name, kill)) + \
                (10 - get_pos(player6.name, assist)) + \
                (10 - get_pos(player6.name, win)) + \
                (get_pos(player6.name, death) + 3)
    player7.total_pt = (10 - get_pos(player7.name, nuri)) + \
                (10 - get_pos(player7.name, kill)) + \
                (10 - get_pos(player7.name, assist)) + \
                (10 - get_pos(player7.name, win)) + \
                (get_pos(player7.name, death) + 3)
    player8.total_pt = (10 - get_pos(player8.name, nuri)) + \
                (10 - get_pos(player8.name, kill)) + \
                (10 - get_pos(player8.name, assist)) + \
                (10 - get_pos(player8.name, win)) + \
                (get_pos(player8.name, death) + 3)

    p_total = [player1, player2, player3, player4,
            player5, player6, player7, player8]
    total = sorted(p_total, key=lambda val : val.total_pt, reverse=True)

    return render_template('index.html',
        end_time=end_time,
        stage=stage,

        nuri_1_name = nuri[0].name,
        nuri_1_pt = nuri[0].nuri_pt,
        nuri_1_pt_before = nuri[0].nuri_pt_before,
        nuri_2_name = nuri[1].name,
        nuri_2_pt = nuri[1].nuri_pt,
        nuri_2_pt_before = nuri[1].nuri_pt_before,
        nuri_3_name = nuri[2].name,
        nuri_3_pt = nuri[2].nuri_pt,
        nuri_3_pt_before = nuri[2].nuri_pt_before,
        nuri_4_name = nuri[3].name,
        nuri_4_pt = nuri[3].nuri_pt,
        nuri_4_pt_before = nuri[3].nuri_pt_before,
        nuri_5_name = nuri[4].name,
        nuri_5_pt = nuri[4].nuri_pt,
        nuri_5_pt_before = nuri[4].nuri_pt_before,
        nuri_6_name = nuri[5].name,
        nuri_6_pt = nuri[5].nuri_pt,
        nuri_6_pt_before = nuri[5].nuri_pt_before,
        nuri_7_name = nuri[6].name,
        nuri_7_pt = nuri[6].nuri_pt,
        nuri_7_pt_before = nuri[6].nuri_pt_before,
        nuri_8_name = nuri[7].name,
        nuri_8_pt = nuri[7].nuri_pt,
        nuri_8_pt_before = nuri[7].nuri_pt_before,

        kill_1_name = kill[0].name,
        kill_1_pt = kill[0].kill_pt,
        kill_1_pt_before = kill[0].kill_pt_before,
        kill_2_name = kill[1].name,
        kill_2_pt = kill[1].kill_pt,
        kill_2_pt_before = kill[1].kill_pt_before,
        kill_3_name = kill[2].name,
        kill_3_pt = kill[2].kill_pt,
        kill_3_pt_before = kill[2].kill_pt_before,
        kill_4_name = kill[3].name,
        kill_4_pt = kill[3].kill_pt,
        kill_4_pt_before = kill[3].kill_pt_before,
        kill_5_name = kill[4].name,
        kill_5_pt = kill[4].kill_pt,
        kill_5_pt_before = kill[4].kill_pt_before,
        kill_6_name = kill[5].name,
        kill_6_pt = kill[5].kill_pt,
        kill_6_pt_before = kill[5].kill_pt_before,
        kill_7_name = kill[6].name,
        kill_7_pt = kill[6].kill_pt,
        kill_7_pt_before = kill[6].kill_pt_before,
        kill_8_name = kill[7].name,
        kill_8_pt = kill[7].kill_pt,
        kill_8_pt_before = kill[7].kill_pt_before,

        assist_1_name = assist[0].name,
        assist_1_pt = assist[0].assist_pt,
        assist_1_pt_before = assist[0].assist_pt_before,
        assist_2_name = assist[1].name,
        assist_2_pt = assist[1].assist_pt,
        assist_2_pt_before = assist[1].assist_pt_before,
        assist_3_name = assist[2].name,
        assist_3_pt = assist[2].assist_pt,
        assist_3_pt_before = assist[2].assist_pt_before,
        assist_4_name = assist[3].name,
        assist_4_pt = assist[3].assist_pt,
        assist_4_pt_before = assist[3].assist_pt_before,
        assist_5_name = assist[4].name,
        assist_5_pt = assist[4].assist_pt,
        assist_5_pt_before = assist[4].assist_pt_before,
        assist_6_name = assist[5].name,
        assist_6_pt = assist[5].assist_pt,
        assist_6_pt_before = assist[5].assist_pt_before,
        assist_7_name = assist[6].name,
        assist_7_pt = assist[6].assist_pt,
        assist_7_pt_before = assist[6].assist_pt_before,
        assist_8_name = assist[7].name,
        assist_8_pt = assist[7].assist_pt,
        assist_8_pt_before = assist[7].assist_pt_before,

        death_1_name = death[0].name,
        death_1_pt = death[0].death_pt,
        death_1_pt_before = death[0].death_pt_before,
        death_2_name = death[1].name,
        death_2_pt = death[1].death_pt,
        death_2_pt_before = death[1].death_pt_before,
        death_3_name = death[2].name,
        death_3_pt = death[2].death_pt,
        death_3_pt_before = death[2].death_pt_before,
        death_4_name = death[3].name,
        death_4_pt = death[3].death_pt,
        death_4_pt_before = death[3].death_pt_before,
        death_5_name = death[4].name,
        death_5_pt = death[4].death_pt,
        death_5_pt_before = death[4].death_pt_before,
        death_6_name = death[5].name,
        death_6_pt = death[5].death_pt,
        death_6_pt_before = death[5].death_pt_before,
        death_7_name = death[6].name,
        death_7_pt = death[6].death_pt,
        death_7_pt_before = death[6].death_pt_before,
        death_8_name = death[7].name,
        death_8_pt = death[7].death_pt,
        death_8_pt_before = death[7].death_pt_before,

        win_1_name = win[0].name,
        win_1_pt = win[0].win_pt,
        win_2_name = win[1].name,
        win_2_pt = win[1].win_pt,
        win_3_name = win[2].name,
        win_3_pt = win[2].win_pt,
        win_4_name = win[3].name,
        win_4_pt = win[3].win_pt,
        win_5_name = win[4].name,
        win_5_pt = win[4].win_pt,
        win_6_name = win[5].name,
        win_6_pt = win[5].win_pt,
        win_7_name = win[6].name,
        win_7_pt = win[6].win_pt,
        win_8_name = win[7].name,
        win_8_pt = win[7].win_pt,

        total_1_name = total[0].name,
        total_1_pt = total[0].total_pt,
        total_2_name = total[1].name,
        total_2_pt = total[1].total_pt,
        total_3_name = total[2].name,
        total_3_pt = total[2].total_pt,
        total_4_name = total[3].name,
        total_4_pt = total[3].total_pt,
        total_5_name = total[4].name,
        total_5_pt = total[4].total_pt,
        total_6_name = total[5].name,
        total_6_pt = total[5].total_pt,
        total_7_name = total[6].name,
        total_7_pt = total[6].total_pt,
        total_8_name = total[7].name,
        total_8_pt = total[7].total_pt,

        )

def get_pos(name, l):
    for i in range(8):
        if l[i].name == name:
            return i


def get_win_pt(me_winlose, other_winlose, d, i):
    if d[0]['players'][i]['team'] == "my":
        t = me_winlose
    else: 
        t = other_winlose

    if t == "win":
        return 1
    else:
        return 0


if __name__ == '__main__':
    app.debug = True
    #app.run(host='localhost')
    app.run(debug=False, host='0.0.0.0', port=8080)
    login_name = sys.argv[0]