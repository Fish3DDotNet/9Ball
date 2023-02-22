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
csvFilename = os.path.join(SITE_ROOT, 'static/data',
                                'teams.txt')
app.app_context().push()
db.create_all()

def createdb(csvFilename):
    with open(csvFilename, encoding='utf-8') as csvfile:
        # def row_count(filename):
        #     with open(filename) as in_file:
        #         return sum(1 for _ in in_file)
        #
        # csvRead = csv.DictReader(csvfile)
        # last_line_number = row_count(csvFilename)


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

    # for team in teams:
    #     db.session.delete(team)
    #     db.session.commit()


def convjson(csvFilename):
    # creating a dictionary
    teams = {}
    t = {}
    p = {}
    # reading the data from CSV file
    with open(csvFilename, encoding='utf-8') as csvfile:
        def row_count(filename):
            with open(filename) as in_file:
                return sum(1 for _ in in_file)

        csvRead = csv.DictReader(csvfile)
        last_line_number = row_count(csvFilename)
        team = "0"
        # Converting rows into dictionary and adding it to data
        for rows in csvRead:
            if rows["Team"] != team:
                if team == "0":
                    team = rows["Team"]
                    t = {rows["Team"]:{}}
                    t[rows["Team"]].update({rows["name"]: {"no":rows["no"],"sl": rows["sl"]}})
                elif rows["Team"] != team:
                    teams.update(t)
                    team = rows["Team"]
                    t = {rows["Team"]: {}}
                    t[rows["Team"]].update({rows["name"]: {"no": rows["no"], "sl": rows["sl"]}})
                else:
                    pass
            else:
                t[rows["Team"]].update({rows["name"]: {"no":rows["no"],"sl": rows["sl"]}})
                if last_line_number == 2:
                    teams.update(t)
            last_line_number -= 1

    return teams
def updateSession(session):


    if 'scoretable' not in session:

        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, 'static/data',
                                'Scorecard.json')
        session['scoretable'] = json.load(open(json_url))

    # <editor-fold desc="# Scoresheet Data">

    if 'submitrackvisible' not in session:
        session['submitrackvisible'] = 'hidden'
    if 'submitrackinvisible' not in session:
        session['submitrackinvisible'] = ''

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

    #if 'teams' not in session:
        #session['teams']= convjson(csvFilename)
    # </editor-fold>
    #
    # Rack Score sheet

    for i in range(15):
        if str('p1r' + str(i + 1)) not in session:  # Player1 score
            session[str('p1r' + str(i + 1))] = ''
        if str('inr' + str(i + 1)) not in session:  # Innings
            session[str('inr' + str(i + 1))] = ""
        if str('dbr' + str(i + 1)) not in session:  # Dead Balls
            session[str('dbr' + str(i + 1))] = ''
        if str('p2r' + str(i + 1)) not in session:  # Player2 score
            session[str('p2r' + str(i + 1))] = ''

    # Pool ball gif's

    for i in range(9):
        if str('p1ball' + str(i + 1)) not in session:
            session[str('p1ball' + str(i + 1))] = str('/static/img/'
                    + str(i + 1) + 'ball.gif')

    # Player Scores

    for i in range(55):
        if str('p1s' + str(i + 1)) not in session:  # Player 1 tick table
            session[str('p1s' + str(i + 1))] = ''
        if str('p2s' + str(i + 1)) not in session:  # Player 2 tick table
            session[str('p2s' + str(i + 1))] = ''

    # Main Score sheet

    for i in range(5):
        if str('m' + str(i + 1) + 't1') not in session:  # Team 1 no
            session[str('m' + str(i + 1) + 't1')] = '-'
        if str('m' + str(i + 1) + 't2') not in session:  # Team 2 no
            session[str('m' + str(i + 1) + 't2')] = '-'
        if str('m' + str(i + 1) + 'p1') not in session:  # Player 1 name
            session[str('m' + str(i + 1) + 'p1')] = '-'
        if str('m' + str(i + 1) + 'p2') not in session:  # Player 2 name
            session[str('m' + str(i + 1) + 'p2')] = '-'
        if str('m' + str(i + 1) + 'p1no') not in session:  # Player 1 number
            session[str('m' + str(i + 1) + 'p1no')] = '-'
        if str('m' + str(i + 1) + 'p2no') not in session:  # Player 2 number
            session[str('m' + str(i + 1) + 'p2no')] = '-'
        if str('m' + str(i + 1) + 'p1sl') not in session:  # Player 1 Skill Level
            session[str('m' + str(i + 1) + 'p1sl')] = '-'
        if str('m' + str(i + 1) + 'p2sl') not in session:  # Player 2 Skill Level
            session[str('m' + str(i + 1) + 'p2sl')] = '-'
        if str('m' + str(i + 1) + 'p1saf') not in session:  # Player 1 Safetys
            session[str('m' + str(i + 1) + 'p1saf')] = '-'
        if str('m' + str(i + 1) + 'p2saf') not in session:  # Player 2 Safetys
            session[str('m' + str(i + 1) + 'p2saf')] = '-'
        if str('m' + str(i + 1) + 'p1sco') not in session:  # Player 1 Score
            session[str('m' + str(i + 1) + 'p1sco')] = '-'
        if str('m' + str(i + 1) + 'p2sco') not in session:  # Player 2 Score
            session[str('m' + str(i + 1) + 'p2sco')] = '-'
        if str('m' + str(i + 1) + 'p1poi') not in session:  # Player 1 Points
            session[str('m' + str(i + 1) + 'p1poi')] = '-'
        if str('m' + str(i + 1) + 'p2poi') not in session:  # Player 2 Points
            session[str('m' + str(i + 1) + 'p2poi')] = '-'
        if str('m' + str(i + 1) + 'in') not in session:  # Match Innings
            session[str('m' + str(i + 1) + 'in')] = '-'

        if 'players' not in session:
            session['players'] = {'team1': {'Nelson, Jeff': {'sl': 3,
                                  'no': 2345}, 'Nelson, Jana': {'sl': 2,
                                  'no': 1567}}}

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    team_to_update = teams.query.get_or_404(id)
    if request.method == "POST":
        team_to_update.playername = request.form['name']
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
    names = ["08", "04"]
    showteams = teams.query.filter(teams.divname=='Tue Double Jeopardy - 442',teams.teamno.in_(names)).all()
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
    createdb(csvFilename)
    time.sleep(2)
    showteams = teams.query.order_by(teams.date_created)
    return render_template("teams.html", teams=showteams)

@app.route('/home')
def home():


    return render_template(
        'home.html',
        m1t1=session['m1t1'],
        m1p1=session['m1p1'],
        m1p1no=session['m1p1no'],
        m1p1sl=session['m1p1sl'],
        m1in=session['m1in'],
        m1p1saf=session['m1p1saf'],
        m1p1sco=session['m1p1sco'],
        m1p1poi=session['m1p1poi'],
        m1t2=session['m1t2'],
        m1p2=session['m1p2'],
        m1p2no=session['m1p2no'],
        m1p2sl=session['m1p2sl'],
        m1p2saf=session['m1p2saf'],
        m1p2sco=session['m1p2sco'],
        m1p2poi=session['m1p2poi'],
        m2t1=session['m2t1'],
        m2p1=session['m2p1'],
        m2p1no=session['m2p1no'],
        m2p1sl=session['m2p1sl'],
        m2in=session['m2in'],
        m2p1saf=session['m2p1saf'],
        m2p1sco=session['m2p1sco'],
        m2p1poi=session['m2p1poi'],
        m2t2=session['m2t2'],
        m2p2=session['m2p2'],
        m2p2no=session['m2p2no'],
        m2p2sl=session['m2p2sl'],
        m2p2saf=session['m2p2saf'],
        m2p2sco=session['m2p2sco'],
        m2p2poi=session['m2p2poi'],
        m3t1=session['m3t1'],
        m3p1=session['m3p1'],
        m3p1no=session['m3p1no'],
        m3p1sl=session['m3p1sl'],
        m3in=session['m3in'],
        m3p1saf=session['m3p1saf'],
        m3p1sco=session['m3p1sco'],
        m3p1poi=session['m3p1poi'],
        m3t2=session['m3t2'],
        m3p2=session['m3p2'],
        m3p2no=session['m3p2no'],
        m3p2sl=session['m3p2sl'],
        m3p2saf=session['m3p2saf'],
        m3p2sco=session['m3p2sco'],
        m3p2poi=session['m3p2poi'],
        m4t1=session['m4t1'],
        m4p1=session['m4p1'],
        m4p1no=session['m4p1no'],
        m4p1sl=session['m4p1sl'],
        m4in=session['m4in'],
        m4p1saf=session['m4p1saf'],
        m4p1sco=session['m4p1sco'],
        m4p1poi=session['m4p1poi'],
        m4t2=session['m4t2'],
        m4p2=session['m4p2'],
        m4p2no=session['m4p2no'],
        m4p2sl=session['m4p2sl'],
        m4p2saf=session['m4p2saf'],
        m4p2sco=session['m4p2sco'],
        m4p2poi=session['m4p2poi'],
        m5t1=session['m5t1'],
        m5p1=session['m5p1'],
        m5p1no=session['m5p1no'],
        m5p1sl=session['m5p1sl'],
        m5in=session['m5in'],
        m5p1saf=session['m5p1saf'],
        m5p1sco=session['m5p1sco'],
        m5p1poi=session['m5p1poi'],
        m5t2=session['m5t2'],
        m5p2=session['m5p2'],
        m5p2no=session['m5p2no'],
        m5p2sl=session['m5p2sl'],
        m5p2saf=session['m5p2saf'],
        m5p2sco=session['m5p2sco'],
        m5p2poi=session['m5p2poi'],
        )


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

    return render_template(
        'racks.html',
        player1=session['player1'],
        player2=session['player2'],
        player1no=session['player1no'],
        player2no=session['player2no'],
        team1=session['team1'],
        team2=session['team2'],
        player1target=session['player1target'],
        player2target=session['player2target'],
        p1curval=session['p1curval'],
        p2curval=session['p2curval'],
        p3curval=session['p3curval'],
        p1r1=session['p1r1'],
        p1r2=session['p1r2'],
        p1r3=session['p1r3'],
        p1r4=session['p1r4'],
        p1r5=session['p1r5'],
        p1r6=session['p1r6'],
        p1r7=session['p1r7'],
        p1r8=session['p1r8'],
        p1r9=session['p1r9'],
        p1r10=session['p1r10'],
        p1r11=session['p1r11'],
        p1r12=session['p1r12'],
        p1r13=session['p1r13'],
        p1r14=session['p1r14'],
        p1r15=session['p1r15'],
        inr1=session['inr1'],
        inr2=session['inr2'],
        inr3=session['inr3'],
        inr4=session['inr4'],
        inr5=session['inr5'],
        inr6=session['inr6'],
        inr7=session['inr7'],
        inr8=session['inr8'],
        inr9=session['inr9'],
        inr10=session['inr10'],
        inr11=session['inr11'],
        inr12=session['inr12'],
        inr13=session['inr13'],
        inr14=session['inr14'],
        inr15=session['inr15'],
        dbr1=session['dbr1'],
        dbr2=session['dbr2'],
        dbr3=session['dbr3'],
        dbr4=session['dbr4'],
        dbr5=session['dbr5'],
        dbr6=session['dbr6'],
        dbr7=session['dbr7'],
        dbr8=session['dbr8'],
        dbr9=session['dbr9'],
        dbr10=session['dbr10'],
        dbr11=session['dbr11'],
        dbr12=session['dbr12'],
        dbr13=session['dbr13'],
        dbr14=session['dbr14'],
        dbr15=session['dbr15'],
        p2r1=session['p2r1'],
        p2r2=session['p2r2'],
        p2r3=session['p2r3'],
        p2r4=session['p2r4'],
        p2r5=session['p2r5'],
        p2r6=session['p2r6'],
        p2r7=session['p2r7'],
        p2r8=session['p2r8'],
        p2r9=session['p2r9'],
        p2r10=session['p2r10'],
        p2r11=session['p2r11'],
        p2r12=session['p2r12'],
        p2r13=session['p2r13'],
        p2r14=session['p2r14'],
        p2r15=session['p2r15'],
        p1ball1=session['p1ball1'],
        p1ball2=session['p1ball2'],
        p1ball3=session['p1ball3'],
        p1ball4=session['p1ball4'],
        p1ball5=session['p1ball5'],
        p1ball6=session['p1ball6'],
        p1ball7=session['p1ball7'],
        p1ball8=session['p1ball8'],
        p1ball9=session['p1ball9'],
        p1s1=session['p1s1'],
        p1s2=session['p1s2'],
        p1s3=session['p1s3'],
        p1s4=session['p1s4'],
        p1s5=session['p1s5'],
        p1s6=session['p1s6'],
        p1s7=session['p1s7'],
        p1s8=session['p1s8'],
        p1s9=session['p1s9'],
        p1s10=session['p1s10'],
        p1s11=session['p1s11'],
        p1s12=session['p1s12'],
        p1s13=session['p1s13'],
        p1s14=session['p1s14'],
        p1s15=session['p1s15'],
        p1s16=session['p1s16'],
        p1s17=session['p1s17'],
        p1s18=session['p1s18'],
        p1s19=session['p1s19'],
        p1s20=session['p1s20'],
        p1s21=session['p1s21'],
        p1s22=session['p1s22'],
        p1s23=session['p1s23'],
        p1s24=session['p1s24'],
        p1s25=session['p1s25'],
        p1s26=session['p1s26'],
        p1s27=session['p1s27'],
        p1s28=session['p1s28'],
        p1s29=session['p1s29'],
        p1s30=session['p1s30'],
        p1s31=session['p1s31'],
        p1s32=session['p1s32'],
        p1s33=session['p1s33'],
        p1s34=session['p1s34'],
        p1s35=session['p1s35'],
        p1s36=session['p1s36'],
        p1s37=session['p1s37'],
        p1s38=session['p1s38'],
        p1s39=session['p1s39'],
        p1s40=session['p1s40'],
        p1s41=session['p1s41'],
        p1s42=session['p1s42'],
        p1s43=session['p1s43'],
        p1s44=session['p1s44'],
        p1s45=session['p1s45'],
        p1s46=session['p1s46'],
        p1s47=session['p1s47'],
        p1s48=session['p1s48'],
        p1s49=session['p1s49'],
        p1s50=session['p1s50'],
        p1s51=session['p1s51'],
        p1s52=session['p1s52'],
        p1s53=session['p1s53'],
        p1s54=session['p1s54'],
        p1s55=session['p1s55'],
        p2s1=session['p2s1'],
        p2s2=session['p2s2'],
        p2s3=session['p2s3'],
        p2s4=session['p2s4'],
        p2s5=session['p2s5'],
        p2s6=session['p2s6'],
        p2s7=session['p2s7'],
        p2s8=session['p2s8'],
        p2s9=session['p2s9'],
        p2s10=session['p2s10'],
        p2s11=session['p2s11'],
        p2s12=session['p2s12'],
        p2s13=session['p2s13'],
        p2s14=session['p2s14'],
        p2s15=session['p2s15'],
        p2s16=session['p2s16'],
        p2s17=session['p2s17'],
        p2s18=session['p2s18'],
        p2s19=session['p2s19'],
        p2s20=session['p2s20'],
        p2s21=session['p2s21'],
        p2s22=session['p2s22'],
        p2s23=session['p2s23'],
        p2s24=session['p2s24'],
        p2s25=session['p2s25'],
        p2s26=session['p2s26'],
        p2s27=session['p2s27'],
        p2s28=session['p2s28'],
        p2s29=session['p2s29'],
        p2s30=session['p2s30'],
        p2s31=session['p2s31'],
        p2s32=session['p2s32'],
        p2s33=session['p2s33'],
        p2s34=session['p2s34'],
        p2s35=session['p2s35'],
        p2s36=session['p2s36'],
        p2s37=session['p2s37'],
        p2s38=session['p2s38'],
        p2s39=session['p2s39'],
        p2s40=session['p2s40'],
        p2s41=session['p2s41'],
        p2s42=session['p2s42'],
        p2s43=session['p2s43'],
        p2s44=session['p2s44'],
        p2s45=session['p2s45'],
        p2s46=session['p2s46'],
        p2s47=session['p2s47'],
        p2s48=session['p2s48'],
        p2s49=session['p2s49'],
        p2s50=session['p2s50'],
        p2s51=session['p2s51'],
        p2s52=session['p2s52'],
        p2s53=session['p2s53'],
        p2s54=session['p2s54'],
        p2s55=session['p2s55'],
        submitrackvisible=session['submitrackvisible'],
        submitrackinvisible=session['submitrackinvisible'],
        )


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
    if "currentrack" not in session:
        updateSession(session)

    # Get Button Name

    list = []
    for key in request.values.dicts[1].keys():
        list.append(key)

    # get Player value & Ball Number

    lstval = list[0]
    lstval = lstval[:2]
    plrval = int(lstval[0])
    ballval = int(lstval[1])

    # Check if ball has been clicked - if so unhide it and subtract 1 point

    if session['p1ball' + str(ballval)] == '':

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
    else:

        # Add a point

        if ballval != 9:
            session['p' + str(plrval) + 'curval'] = session['p'
                    + str(plrval) + 'curval'] + 1
        else:
            session['p' + str(plrval) + 'curval'] = session['p'
                    + str(plrval) + 'curval'] + 2

        # hide ball

        session['p1ball' + str(ballval)] = ''

    if session['currentrack'] > 1:
        session['p1total'] = session['p1r' + str(session['currentrack'
                ])] = session['p1curval'] + session['p1r'
                + str(session['currentrack'] - 1)]
        session['p2total'] = session['p2r' + str(session['currentrack'
                ])] = session['p2curval'] + session['p2r'
                + str(session['currentrack'] - 1)]
        session['dbtotal'] = session['dbr' + str(session['currentrack'
                ])] = session['p3curval']
    else:
        session['p1total'] = session['p1r1'] = session['p1curval']
        session['p2total'] = session['p2r1'] = session['p2curval']
        session['dbtotal'] = session['dbr1'] = session['p3curval']

    # update Score tickers
    for i in range(55):
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
            if session['p1total'] >= i:
                session['p1s' + str(i)] = 'bg_green'
            else:
                session['p1s' + str(i)] = ''

        # if Player 2 reaches target highlight all Green
        if session['p2total'] >= int(session['player2target']):
            if session['p2total'] >= i:
                session['p2s' + str(i)] = 'bg_green'
            else:
                session['p2s' + str(i)] = ''

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

    session['p1curval'] = 0
    session['p2curval'] = 0
    session['p3curval'] = 0
    session['incurval'] = 0
    session['submitrackvisible'] = 'hidden'
    session['submitrackinvisible'] = ''

    return redirect(url_for('racks'))


@app.route('/', methods=['POST', 'GET'])
def index():
    for key in list(session.keys()):
        session.pop(key)

    updateSession(session)
    return redirect(url_for('home'))

@app.route('/clear', methods=['POST', 'GET'])
def clear():
    for key in list(session.keys()):
        session.pop(key)

    updateSession(session)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
