from flask import Flask, render_template, request, flash, jsonify, \
    url_for, redirect, session, json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time
import json
import os
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sessionkey123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teams.db'

db = SQLAlchemy(app)

#create db model
class teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    divname = db.Column(db.String(50), nullable=False)
    teamno = db.Column(db.String(10), nullable=False)
    teamname = db.Column(db.String(30), nullable=False)
    playername = db.Column(db.String(30), nullable=False)
    playerno = db.Column(db.Integer, nullable=False)
    playersl = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<name %r>' % self.id

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
txtFilename = os.path.join(SITE_ROOT, 'static/data',
                                'teams.txt')
app.app_context().push()
db.create_all()

def createdb(txtFilename):
    with open(txtFilename, encoding='utf-8') as csvfile:

        data = list(csv.reader(csvfile, delimiter=","))

    for i in data:
        print(i[0])

        team_playername = i[3]
        team_divname = i[0]
        team_teamno = i[1]
        team_teamname = i[2]
        team_playerno = i[4]
        team_playersl = i[5]
        new_team = teams(playername=team_playername,
                             divname=team_divname,
                             teamno=team_teamno,
                             teamname=team_teamname,
                             playerno=team_playerno,
                             playersl=team_playersl)
        try:
            db.session.add(new_team)
            db.session.commit()

        except:
            return "There was a error adding Player"

def updateSession(session):

    if 'scoretable' not in session:

        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, 'static/data',
                                'Scorecard.json')
        session['scoretable'] = json.load(open(json_url))

    # <editor-fold desc="# Scoresheet Data">

    # keys = ['key1','key2']
    # for i in keys:
    #     if i not in session:
    #         session[i] = ''


    if 'submitrackvisible' not in session:
        session['submitrackvisible'] = 'hidden'
    if 'submitrackinvisible' not in session:
        session['submitrackinvisible'] = ''
    if 'teamssellectedinvisable' not in session:
        session['teamssellectedinvisable'] = 'hidden'
    if 'teamssellectedvisable' not in session:
        session['teamssellectedvisable'] = ''

    if 'player1' not in session:
        session['player1'] = ''
    if 'player2' not in session:
        session['player2'] = ''
    if 'player1no' not in session:
        session['player1no'] = ''
    if 'player2no' not in session:
        session['player2no'] = ''
    if 'team1' not in session:
        session['team1'] = ''
    if 'team2' not in session:
        session['team2'] = ''
    if 'player1target' not in session:
        session['player1target'] = ''
    if 'player2target' not in session:
        session['player2target'] = ''
    if 'p1curval' not in session:
        session['p1curval'] = 0
    if 'p2curval' not in session:
        session['p2curval'] = 0
    if 'p3curval' not in session:
        session['p3curval'] = 0
    if 'incurval' not in session:
        session['incurval'] = 0
    if 'p1total' not in session:
        session['p1total'] = 0
    if 'p2total' not in session:
        session['p2total'] = 0
    if 'dbtotal' not in session:
        session['dbtotal'] = 0
    if 'inningtotal' not in session:
        session['inningtotal'] = 0
    if 'currentrack' not in session:
        session['currentrack'] = 1
    if 'currentmatch' not in session:
        session['currentmatch'] = 1
    if 'division' not in session:
        session['division'] = ''
    if 'teama' not in session:
        session['teama'] = "Team A"
    if 'teamano' not in session:
        session['teamano'] = ''
    if 'teamascore' not in session:
        session['teamascore'] = 0
    if 'teamb' not in session:
        session['teamb'] = "Team B"
    if 'teambno' not in session:
        session['teambno'] = ''
    if 'teambscore' not in session:
        session['teambscore'] = 0
    if 'teamnameList' not in session:
        session['teamnameList'] = []
    if 'divisionList' not in session:
        session['divisionList'] = []
    if 'teamsSelected' not in session:
        session['teamsSelected'] = []
    if 'step' not in session:
        session['step'] = 0
    # </editor-fold>

    # Rack Score sheet

    for i in range(15):
        if str('p1r' + str(i + 1)) not in session:  # Player1 score
            session[str('p1r' + str(i + 1))] = ''
        if str('inr' + str(i + 1)) not in session:  # Innings
            session[str('inr' + str(i + 1))] = ''
        if str('dbr' + str(i + 1)) not in session:  # Dead Balls
            session[str('dbr' + str(i + 1))] = ''
        if str('p2r' + str(i + 1)) not in session:  # Player2 score
            session[str('p2r' + str(i + 1))] = ''

    # Pool ball gif's

    for i in range(9):
        if str('p1ball' + str(i + 1)) not in session:
            session[str('p1ball' + str(i + 1))] = str('/static/img/'
                    + str(i + 1) + 'ball.gif')
        if str('p2ball' + str(i + 1)) not in session:
            session[str('p2ball' + str(i + 1))] = str('/static/img/'
                    + str(i + 1) + 'ball.gif')
        if str('p3ball' + str(i + 1)) not in session:
            session[str('p3ball' + str(i + 1))] = str('/static/img/'
                    + str(i + 1) + 'ball.gif')

    # Player Scores

    for i in range(75):
        if str('p1s' + str(i + 1)) not in session:  # Player 1 tick table
            session[str('p1s' + str(i + 1))] = ''
        if str('p2s' + str(i + 1)) not in session:  # Player 2 tick table
            session[str('p2s' + str(i + 1))] = ''

    # Main Score sheet
    mainScoreSheet = ['t1', 't2', 'p1', 'p2', 'p1no', 'p2no', 'p1sl', 'p2sl',
                      'p1saf', 'p2saf', 'p1sco', 'p2sco', 'p1poi', 'p2poi', 'in',
                      'buttonvis', 'numvis']
    for i in range(5):
        for l in mainScoreSheet:
            if str('m' + str(i + 1) + l) not in session:
                session[str('m' + str(i + 1) + l)] = '-'

def contextbuild():
    d={}
    for key in session:
        d[key] = session[key]

    return d

def updateteamScores():
    session['teamascore'] = 0
    session['teambscore'] = 0
    for i in range(5):
        if session['m'+str(i+1)+'p1poi'] == '-':
            return
        if session['m'+str(i+1)+'t1'] == session['teamano']:
            session['teamascore'] = session['teamascore'] + int(session['m' + str(i + 1) + 'p1poi'])
            session['teambscore'] = session['teambscore'] + int(session['m' + str(i + 1) + 'p2poi'])
        else:
            session['teamascore'] = session['teamascore'] + int(session['m' + str(i + 1) + 'p2poi'])
            session['teambscore'] = session['teambscore'] + int(session['m' + str(i + 1) + 'p1poi'])

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    team_to_update = teams.query.get_or_404(id)
    if request.method == "POST":
        team_to_update.playername = request.form['name']
        team_to_update.playerno = request.form['pno']
        team_to_update.playersl = request.form['psl']
        try:
            db.session.commit()
            return redirect('/showteams')
        except:
            return "There was an error updating!!...."
    else:
        return render_template('update.html', team_to_update=team_to_update)

@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    team_to_update = teams.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(team_to_update)
        try:
            db.session.commit()
            return redirect('/showteams')
        except:
            return "There was an error updating!!...."
    else:
        return render_template('delete.html', team_to_update=team_to_update)

@app.route('/query', methods=['POST', 'GET'])
def query():
    names = [session['teamano'], session['teambno']]
    showteams = teams.query.filter(teams.divname==session['division'],teams.teamno.in_(names)).all()
    # division = teams.query.filter_by(divname = 'Thurs Double Jeopardy - 444').all()
    # showteams = teams.query.filter(division.teamname.in_(names)).all()

    return render_template("teams.html", teams=showteams)

@app.route('/showteams', methods=['POST', 'GET'])
def showteams():

    if request.method == "POST":
        team_name = request.form['name']
        team_divno = 'Thursday Double J - 444'
        team_teamno = '08'
        team_team = 'Crazy 8s'
        team_no = 12345
        team_sl = 4
        new_team = teams(name=team_name,
                             divno=team_divno,
                             teamno=team_teamno,
                             team=team_team,
                             no=team_no,
                             sl=team_sl)
        try:
            db.session.add(new_team)
            db.session.commit()
            return redirect('/teams')
        except:
            return "There was a error adding Player"
    else:
        showteams = teams.query.order_by(teams.date_created)

        return render_template("teams.html", teams=showteams)

@app.route('/reloadteams')
def reloadteams():
    showteams = teams.query.order_by(teams.date_created)
    for team in showteams:
        db.session.delete(team)
        db.session.commit()
    createdb(txtFilename)
    time.sleep(2)
    showteams = teams.query.order_by(teams.date_created)
    return render_template("teams.html", teams=showteams)

@app.route('/home')
def home():
    updateteamScores()

    context = {}; context = contextbuild()

    return render_template(
        'home.html', **context)


@app.route('/editsession', methods=['POST', 'GET'])
def editsession():
    if request.method == "POST":
        for k in session:
            if type(session[k]) == int:
                session[k] = int(request.form[k])
            else:
                session[k] = request.form[k]

        context = {}; context = contextbuild()

        return render_template('home.html',**context)
    else:
        context = {}; context = contextbuild()

        return render_template(
            'editsession.html', context=context)

@app.route('/updatehome', methods=['POST', 'GET'])
def updatehome():
    if request.method == "POST":
        formdata = ['t1', 't2', 'p1', 'p2', 'p1no', 'p1no', 'in',
                    'p1saf', 'p2saf', 'p1sco', 'p2sco', 'p1poi', 'p2poi']

        for i in range(5):
            for s in formdata:
                session['m' + str(i + 1) + s] = request.form['m' + str(i + 1) + s]

        context = {}; context = contextbuild()

        return render_template('home.html',**context)
    else:

        context = {}; context = contextbuild()

        return render_template('ehome.html',**context)

@app.route('/testdata')
def testdata():

    x = session["currentmatch"]

    curtno1 = '01'
    curpla1 = 'Jeff Nelson'
    curplano1 = '13245'
    curpsl1 = 3

    curtno2 = '02'
    curpla2 = 'Jana Nelson'
    curplano2 = '53421'
    curpsl2 = 2

    session[str('m' + str(x) + 't1')] = session["team1"] = curtno1
    session[str('m' + str(x) + 'p1')] = session["player1"] = curpla1
    session[str('m' + str(x) + 'p1no')] = session["player1no"] = curplano1
    session[str('m' + str(x) + 'p1sl')] = curpsl1
    session["player1target"] = str(session["scoretable"]["psl"][str(curpsl1)])

    session[str('m' + str(x) + 't2')] = session["team2"] = curtno2
    session[str('m' + str(x) + 'p2')] = session["player2"] = curpla2
    session[str('m' + str(x) + 'p2no')] = session["player2no"] = curplano2
    session[str('m' + str(x) + 'p2sl')] = curpsl2
    session["player2target"] = str(session["scoretable"]["psl"][str(curpsl2)])

    return redirect(url_for('home'))

@app.route('/teamselect', methods=['POST', 'GET'])
def teamselect():
    def step1(): # Select division
        session['step'] = 1
        session['division'] = request.form.get('division')
        teamnameList = []
        templist = []
        showteams = teams.query.filter_by(divname=session['division'])

        for team in showteams:
            if ([team.teamno, team.teamname]) not in session['teamnameList']:
                templist = [team.teamno, team.teamname]
                session['teamnameList'].append(templist)

        context = {
            'step': session['step'],
            'teamnameList': session['teamnameList'],
            'divname': session['division']
        }

        return context
    def step2(): # Select Teams
        session['step'] = 2
        teams_selected = request.form.getlist('teamscheckbox')
        teamsSelected = []
        if len(teams_selected) > 0:

            temptxt = teams_selected[0].replace("'","").replace('"',"").replace("]","")
            templist = temptxt.split(',')
            teamsSelected.append(templist)
            temptxt = teams_selected[1].replace("'", "").replace('"',"").replace("]","")
            templist = temptxt.split(',')

            teamsSelected.append(templist)

            session['teama'] = teamsSelected[0][0].replace('[','') +"-"+ teamsSelected[0][1]
            session['teamano'] = teamsSelected[0][0].replace('[','')
            session['teamb'] = teamsSelected[1][0].replace('[','') +"-"+ teamsSelected[1][1]
            session['teambno'] = teamsSelected[1][0].replace('[','')

            session['teamssellectedinvisable'] = ''
            session['teamssellectedvisable'] = 'hidden'
            session['m1buttonvis'] = ''
            session['m1numvis'] = 'hidden'


            context = {};
            context = contextbuild()

            return context

    if request.method == "POST":
        if session['step'] == 0:
            context = step1()
        elif session['step'] == 1:
            context = step2()

        if session['step'] < 2:
            return render_template('teamselect.html',**context)
        else:
            context = {};
            context = contextbuild()

            return render_template('home.html', **context)

    else:
        session['step'] = 0
        getdivisions = teams.query.order_by(teams.date_created)
        for team in getdivisions:
            if team.divname not in session['divisionList']:
                session['divisionList'].append(team.divname)
        return render_template('teamselect.html',
                               step=session['step'],
                               divnameList=session['divisionList'])

@app.route('/playerselect', methods=['POST', 'GET'])
def playerselect():
    def step1(): # Select players
        session['step'] = 1
        players_selected = request.form.getlist('playerscheckbox')

        session['playerida'] = players_selected[0]
        session['playeridb'] = players_selected[1]

        ids = [session['playerida'],session['playeridb']]

        players = teams.query.filter(teams.divname == session['division'], teams.id.in_(ids)).all()

        context = {
            'step': session['step'],
            'players': players
        }

        return context
    def step2(): # Select lag winner
        session['step'] = 2
        lagwinnerid = request.form.get('lagwinner')


        x = session["currentmatch"]

        teama = teams.query.filter_by(id = lagwinnerid).all()

        if session['playerida'] != lagwinnerid:
            teamb = teams.query.filter_by(id=session['playerida']).all()
        else:
            teamb = teams.query.filter_by(id=session['playeridb']).all()



        curtno1 = teama[0].teamno
        curpla1 = teama[0].playername
        curplano1 = teama[0].playerno
        curpsl1 = teama[0].playersl

        curtno2 = teamb[0].teamno
        curpla2 = teamb[0].playername
        curplano2 = teamb[0].playerno
        curpsl2 = teamb[0].playersl

        session[str('m' + str(x) + 't1')] = session["team1"] = curtno1
        session[str('m' + str(x) + 'p1')] = session["player1"] = curpla1
        session[str('m' + str(x) + 'p1no')] = session["player1no"] = curplano1
        session[str('m' + str(x) + 'p1sl')] = curpsl1
        session["player1target"] = str(session["scoretable"]["psl"][str(curpsl1)])

        session[str('m' + str(x) + 't2')] = session["team2"] = curtno2
        session[str('m' + str(x) + 'p2')] = session["player2"] = curpla2
        session[str('m' + str(x) + 'p2no')] = session["player2no"] = curplano2
        session[str('m' + str(x) + 'p2sl')] = curpsl2
        session["player2target"] = str(session["scoretable"]["psl"][str(curpsl2)])

        return redirect(url_for('home'))

    if request.method == "POST":
        if session['step'] == 0:
            context = step1()
        elif session['step'] == 1:
            context = step2()

        if session['step'] < 2:
            return render_template('playerselect.html',**context)
        else:
            context = {};
            context = contextbuild()

            return render_template('home.html', **context)

    else:
        session['step'] = 0

        names = [session['teamano']]
        playersa = teams.query.filter(teams.divname == session['division'], teams.teamno.in_(names)).all()

        names = [session['teambno']]
        playersb = teams.query.filter(teams.divname == session['division'], teams.teamno.in_(names)).all()

        return render_template('playerselect.html',
                               step=session['step'],
                               playersa=playersa,
                               playersb=playersb)

@app.route('/gform')
def gform():

    return render_template('gform.html')

@app.route('/slp')
def slp():
    return render_template('skillpoints.html')

@app.route('/som')
def som():
    return render_template('scoreofmatch.html')

@app.route('/racks')
def racks():

    context = {}; context = contextbuild()

    return render_template('racks.html',**context)

@app.route('/updaterack', methods=['POST', 'GET'])
def updaterack():

    if request.method == "POST":
        for i in range(session['currentrack']):
            tmpval1 = request.form['p1r'+str(i+1)]
            tmpval2 = request.form['inr'+str(i+1)]
            tmpval3 = request.form['dbr'+str(i+1)]
            tmpval4 = request.form['p2r'+str(i+1)]

            if tmpval1 == '':
                tmpval1 = 0
            if tmpval2 == '':
                tmpval2 = 0
            if tmpval3 == '':
                tmpval3 = 0
            if tmpval4 == '':
                tmpval4 = 0

            session['p1r' + str(i + 1)] = int(tmpval1)
            session['inr' + str(i + 1)] = int(tmpval2)
            session['dbr' + str(i + 1)] = int(tmpval3)
            session['p2r' + str(i + 1)] = int(tmpval4)

        return redirect('/racks')
    else:

        context = {}; context = contextbuild()

        return render_template('eracks.html', **context)

@app.route('/p1safety', methods=['POST', 'GET'])
def p1safety():

    x = session["currentmatch"]
    if session["m" + str(x) + "p1saf"] == "-":
        session["m" + str(x) + "p1saf"] = "0"

    session["m" + str(x) + "p1saf"] = str(int(session["m" + str(x) + "p1saf"]) + 1)

    return redirect(url_for('racks'))

@app.route('/p2safety', methods=['POST', 'GET'])
def p2safety():

    x = session["currentmatch"]
    if session["m" + str(x) + "p2saf"] == "-":
        session["m" + str(x) + "p2saf"] = "0"

    session["m" + str(x) + "p2saf"] = str(int(session["m" + str(x) + "p2saf"]) + 1)

    return redirect(url_for('racks'))

@app.route('/inning', methods=['POST', 'GET'])
def inning():

    x = session["currentrack"]

    session["incurval"] = session["incurval"] + 1
    session["inr" + str(x)] = str(session["incurval"])
    return redirect(url_for('racks'))

@app.route('/valup', methods=['POST', 'GET'])
def valup():
    x = session["currentmatch"]

    if "currentrack" not in session:
        updateSession(session)

    # Get Ball Clicked Name

    list = []
    for key in request.values.dicts[1].keys():
        list.append(key)

    # Get Player & Ball Number

    lstval = list[0]
    lstval = lstval[:2]
    plrval = int(lstval[0])
    ballval = int(lstval[1])

    # Check if ball has been clicked - if so unhide it and subtract 1 point
    if "a.gif" in session['p1ball' + str(ballval)] or \
            "a.gif" in session['p2ball' + str(ballval)] or \
            "b.gif" in session['p3ball' + str(ballval)]:

        # subtract 1 point

        if ballval != 9:
            session['p' + str(plrval) + 'curval'] = session['p'
                    + str(plrval) + 'curval'] - 1
        else:
            session['p' + str(plrval) + 'curval'] = session['p'
                    + str(plrval) + 'curval'] - 2

        # Make ball visible again

        session['p1ball' + str(ballval)] = '/static/img/' \
            + str(ballval) + 'ball.gif'
        session['p2ball' + str(ballval)] = '/static/img/' \
            + str(ballval) + 'ball.gif'
        session['p3ball' + str(ballval)] = '/static/img/' \
            + str(ballval) + 'ball.gif'
    else:

        # Add a point

        if ballval != 9:
            session['p' + str(plrval) + 'curval'] = session['p'
                    + str(plrval) + 'curval'] + 1
        else:
            session['p' + str(plrval) + 'curval'] = session['p'
                    + str(plrval) + 'curval'] + 2

        # hide ball

        if plrval == 1:
            session['p1ball' + str(ballval)] = '/static/img/' \
            + str(ballval) + 'balla.gif'
            session['p2ball' + str(ballval)] = ""
            session['p3ball' + str(ballval)] = ""
        elif plrval == 2:
            session['p2ball' + str(ballval)] = '/static/img/' \
            + str(ballval) + 'balla.gif'
            session['p1ball' + str(ballval)] = ""
            session['p3ball' + str(ballval)] = ""
        elif plrval == 3:
            session['p3ball' + str(ballval)] = '/static/img/' \
            + str(ballval) + 'ballb.gif'
            session['p1ball' + str(ballval)] = ""
            session['p2ball' + str(ballval)] = ""

    # update player 1,2 and Dead current rack Ball count

    if session['currentrack'] > 1:
        session['p1total'] = \
            session['p1r' + str(session['currentrack'])] = \
            session['p1curval'] + session['p1r' + str(session['currentrack'] - 1)]
        session['p2total'] = \
            session['p2r' + str(session['currentrack'])] = \
            session['p2curval'] + session['p2r' + str(session['currentrack'] - 1)]
        session['dbtotal'] = \
            session['dbr' + str(session['currentrack'])] = \
            session['p3curval']
    else:
        session['p1total'] = session['p1r1'] = session['p1curval']
        session['p2total'] = session['p2r1'] = session['p2curval']
        session['dbtotal'] = session['dbr1'] = session['p3curval']

    # update Score tickers
    for i in range(76):
        if session['p1total'] >= i:
            session['p1s' + str(i)] = 'bg_AntiqueWhite'
        else:
            session['p1s' + str(i)] = ''

        if str(i) == session['player1target']:
            session['p1s' + str(i)] = 'bg_AntiqueWhite'

        if session['p2total'] >= i:
            session['p2s' + str(i)] = 'bg_AntiqueWhite'
        else:
            session['p2s' + str(i)] = ''

        if str(i) == session['player2target']:
            session['p2s' + str(i)] = 'bg_AntiqueWhite'

        # if Player 1 reaches target highlight all Green
        if session['p1total'] >= int(session['player1target']):
            p21 = str(session['m'+str(x)+'p2sl'])
            p22 = str(session['p2total'])
            if session['p1total'] >= i:
                session['p1s' + str(i)] = 'bg_green'
            else:
                session['p1s' + str(i)] = ''
            # update home screen player score
            session['m'+str(x)+'p1sco'] = session['p1total']
            session['m'+str(x)+'p2sco'] = session['p2total']
            # update home screen team points
            session['m'+str(x)+'p1poi'] = session['scoretable']['som'][p21][p22]['w']
            session['m'+str(x)+'p2poi'] = session['scoretable']['som'][p21][p22]['l']


        # if Player 2 reaches target highlight all Green
        if session['p2total'] >= int(session['player2target']):
            p11 = str(session['m'+str(x)+'p1sl'])
            p12 = str(session['p1total'])
            if session['p2total'] >= i:
                session['p2s' + str(i)] = 'bg_green'
            else:
                session['p2s' + str(i)] = ''
            # update home screen player score
            session['m'+str(x)+'p1sco'] = session['p1total']
            session['m'+str(x)+'p2sco'] = session['p2total']
            # update home screen team points
            session['m'+str(x)+'p1poi'] = session['scoretable']['som'][p11][p12]['l']
            session['m'+str(x)+'p2poi'] = session['scoretable']['som'][p11][p12]['w']

    # if rack complete show submit rack
    if session['p1curval'] + session['p2curval'] \
        + session['p3curval'] == 10:
        session['submitrackvisible'] = ''
        session['submitrackinvisible'] = 'hidden'

    return redirect(url_for('racks'))

@app.route('/submitform', methods=['POST', 'GET'])
def submitform():
    if request.method == 'POST':
        x = session["currentmatch"]

        curtno1 = request.form.get('tno1')
        curpla1 = request.form.get('pname1')
        curplano1 = request.form.get('pno1')
        curpsl1 = request.form.get('psl1')

        curtno2 = request.form.get('tno2')
        curpla2 = request.form.get('pname2')
        curplano2 = request.form.get('pno2')
        curpsl2 = request.form.get('psl2')

        # Verify data
        if curtno1 != "Team #" \
            and curtno2 != "Team #" \
            and curpsl1 != "Skill Level" \
            and curpsl2 != "Skill Level" \
            and curpla1 != "" \
            and curpla2 != "" \
            and curplano1 != "" \
            and curplano2 != "":

            session[str('m' + str(x) + 't1')] = session["team1"] = curtno1
            session[str('m' + str(x) + 'p1')] = session["player1"] = curpla1
            session[str('m' + str(x) + 'p1no')] = session["player1no"] = curplano1
            session[str('m' + str(x) + 'p1sl')] = curpsl1
            session["player1target"] = str(session["scoretable"]["psl"][str(curpsl1)])

            session[str('m' + str(x) + 't2')] = session["team2"] = curtno2
            session[str('m' + str(x) + 'p2')] = session["player2"] = curpla2
            session[str('m' + str(x) + 'p2no')] = session["player2no"] = curplano2
            session[str('m' + str(x) + 'p2sl')] = curpsl2
            session["player2target"] = str(session["scoretable"]["psl"][str(curpsl2)])



            return redirect(url_for('home'))
        else:
            return redirect(url_for('home'))

@app.route('/submitRack', methods=['POST', 'GET'])
def submitRack():
    updateSession(session)
    session['currentrack'] = session['currentrack'] + 1
    for i in range(9):
        session['p1ball' + str(i + 1)] = '/static/img/' + str(i + 1) \
            + 'ball.gif'
        session['p2ball' + str(i + 1)] = '/static/img/' + str(i + 1) \
            + 'ball.gif'
        session['p3ball' + str(i + 1)] = '/static/img/' + str(i + 1) \
            + 'ball.gif'

    session['p1curval'] = 0
    session['p2curval'] = 0
    session['p3curval'] = 0
    session['incurval'] = 0
    session['submitrackvisible'] = 'hidden'
    session['submitrackinvisible'] = ''

    return redirect(url_for('racks'))


@app.route('/submitRack', methods=['POST', 'GET'])
def submitMatch():
    pass

@app.route('/', methods=['POST', 'GET'])
def index():
    ## Clear All
    for key in list(session.keys()):
        session.pop(key)

    updateSession(session)
    return redirect(url_for('home'))

def replace_ifelif_example():
    def first():
        print('Calling first')

    def second():
        print('Calling second')

    def third():
        print('Calling third')

    def default():
        print('Calling default')

    var: int = 4

    funcs: dict = {0: first,
                  1: second,
                  2: third}

    final = funcs.get(var, default)
    final()

if __name__ == '__main__':
    app.run(debug=True)
