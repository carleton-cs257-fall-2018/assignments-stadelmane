#!/usr/bin/env python3
'''
    api.py
    Eric Stadelman and Charlie Broadbent 24 October 2018
    Simple Flask API used in the sample web app for
    CS 257 used for soccer data
'''
import sys
import flask
import json
import psycopg2
import config

app = flask.Flask(__name__, static_folder='static', template_folder='templates')


def get_connection():
    '''
    Returns a connection to the database described
    in the config module. Returns None if the
    connection attempt fails.
    '''
    connection = None
    try:
        connection = psycopg2.connect(database=config.database, user=config.user,
                                      password=config.password)
    except Exception as e:
        print(e, file=sys.stderr)
    return connection


def get_select_query_results(connection, query, parameters=None):
    '''
    Executes the specified query with the specified tuple of
    parameters. Returns a cursor for the query results.
    Raises an exception if the query fails for any reason.
    '''
    cursor = connection.cursor()
    if parameters is not None:
        cursor.execute(query, parameters)
    else:
        cursor.execute(query)
    return cursor


@app.after_request
def set_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/all_stats/')
def get_all_stats():
    final_stats_list = []
    all_stats_list = get_list_of_all_stats()
    for i in range(len(all_stats_list)):
        stats_dict = {}
        stats_dict[i] = all_stats_list[i]
        final_stats_list.append(stats_dict)

    return json.dumps(final_stats_list, sort_keys=True, default=str)


def get_list_of_all_stats():
    '''
    A helper method that returns a list of all stat names from the columns in the
    stats table.
    '''
    all_stats = []
    query_column_names = "SELECT column_name from information_schema.columns " \
                         "where table_name = 'matches'"
    connection = get_connection()
    if connection is not None:
        try:
            i = 0
            for row in get_select_query_results(connection, query_column_names):
                if i != 0:
                    all_stats.append(row[0])
                else:
                    i += 1

        except Exception as e:
            print(e, file=sys.stderr)

    return all_stats


@app.route('/match_stats')
def get_stats():
    '''
    End point that returns a list in json format of all stats specified based
    on the desired teams, dates, and stats.
    Hard coded to always return home_team_id, away_team_id, the date of the game,
    and the result of the game along with
    any other desired stats.
    '''
    stats_string = flask.request.args.get('stats', default=None)
    home_team_id_string = flask.request.args.get('home_team_id', default=None)
    away_team_id_string = flask.request.args.get('away_team_id', default=None)
    date_string = flask.request.args.get('date', default=None)

    parameters_present = False
    get_all_stats = False
    parameters = []
    stats_list = []



    if stats_string != None:
        query = 'SELECT home_team_id, away_team_id, date, final_result, '+ \
                stats_string + ' '
        stats_list = stats_string.split(',')
        parameters.append('home_team_id')
        parameters.append('away_team_id')
        parameters.append('date')
        parameters.append('final_result')
    else:
        query =  'SELECT * '
        get_all_stats = True
        all_stats_list = get_list_of_all_stats()
        for item in all_stats_list:
            stats_list.append(item)

    query = query + 'FROM matches '

    if home_team_id_string != None:
        parameters_present = True
        query = query + 'WHERE ('
        home_team_id_list = home_team_id_string.split(',')
        for i in range(len(home_team_id_list)):
            if i==(len(home_team_id_list)-1):
                if '-' in home_team_id_list[i]:
                    teams_versus = home_team_id_list[i].split('-')
                    query = query + 'home_team_id = ' + teams_versus[0] + \
                            ' AND ' + 'away_team_id = ' + teams_versus[1]
                    query = query + ' OR home_team_id = ' + teams_versus[1] + \
                            ' AND ' + 'away_team_id = ' + \
                            teams_versus[0] + ' '
                else:
                    query = query + 'home_team_id = ' + home_team_id_list[i] + ' '
            else:
                if '-' in home_team_id_list[i]:
                    teams_versus = home_team_id_list[i].split('-')
                    query = query + 'home_team_id = ' + teams_versus[0] + \
                            ' AND ' + 'away_team_id = ' + teams_versus[1]
                    query = query + ' OR home_team_id = ' + teams_versus[1] + \
                            ' AND ' + 'away_team_id = ' + \
                            teams_versus[0] + ' OR '
                else:
                    query = query + 'home_team_id = ' + home_team_id_list[i] \
                            + ' OR '
        

    if away_team_id_string != None:
        if parameters_present == True:
            query = query + 'OR '
        if parameters_present == False:
            parameters_present = True
            query = query + 'WHERE ('
        away_team_id_list = away_team_id_string.split(',')
        for i in range(len(away_team_id_list)):
            if i==(len(away_team_id_list)-1):
                query = query + 'away_team_id = ' + away_team_id_list[i] + ' '
            else:
                query = query + 'away_team_id = ' + away_team_id_list[i] + ' OR '
    query += ') '



    if date_string != None:
        if parameters_present == True:
            query = query + 'AND ('
        if parameters_present == False:
            query = query + 'WHERE ('
        date_list = date_string.split(',')

        date_range = date_list[0].split('*')
        query +='date >= ' + "'" + date_range[0] + "'" + \
                        ' AND ' + 'date <= ' + \
                        "'" + date_range[1] + "')"

        # for i in range(len(date_list)):
        #     if i==(len(date_list)-1):
        #         if '*' in date_list[i]:
        #             date_range = date_list[i].split('*')
        #             query = query + '(date >= ' + "'" + date_range[0] + "'" + \
        #                     ' AND ' + 'date <= ' + \
        #                     "'" + date_range[1] + "')"
        #         else:
        #             query = query + 'date = ' + "'" + date_list[i] + "')"
        #     else:
        #         if '*' in date_list[i]:
        #             date_range = date_list[i].split('*')
        #             query = query + '(date >= ' + "'" + date_range[0] + "'" + \
        #                     ' AND ' + 'date <= ' + \
        #                     "'" + date_range[1] + "'" + ' OR '
        #         else:
        #             query = query + 'date = ' + "'" + date_list[i] + "'" + \
        #                     ' OR '

    for item in stats_list:
        parameters.append(item)

    match_list = []
    connection = get_connection()

    if get_all_stats:
        start = 1
    else:
        start = 0

    query += ' ORDER BY date;'

    print(query)
    if connection is not None:
        try:
            for row in get_select_query_results(connection, query):
                match_info = {}
                for i in range(start, len(row)):
                    match_info[parameters[i-start]] = row[i]
                match_list.append(match_info)
        except Exception as e:
            print(e, file=sys.stderr)
        connection.close()
    return json.dumps(match_list, sort_keys = True, default = str)

@app.route('/team/<name>')
def get_id_from_team_name(name):
    '''
    Endpoint that allows us to retrieve a team's ID
    '''

    query = 'SELECT id FROM teams WHERE team = ' + "'" + name + "';"
    print(query)
    team_name = []
    connection = get_connection()
    if connection is not None:
        try:
            for row in get_select_query_results(connection, query):
                team = {}
                for i in range(len(row)):
                    team['id'] = row[0]
                team_name.append(team)
        except Exception as e:
            print(e, file=sys.stderr)
        connection.close()
    return json.dumps(team_name)


@app.route('/leagues')
def get_teams_from_leagues():
    '''
    Endpoint that returns a list in json format of all teams from specified
    leagues, or all teams by default.
    '''
    league_string = flask.request.args.get('league', default=None)

    parameters = ['team', 'league']
    query = 'SELECT team , league FROM teams'

    if league_string!= None:
        league_list = league_string.split(',')
        query = query + ' WHERE '
        for i in range(len(league_list)):
            if i == (len(league_list) -1):
                query = query + 'league = ' + "'" + league_list[i] + "'"
            else:
                query = query + 'league = ' + "'" + league_list[i] + "'" + \
                        ' or '

    team_list = []
    connection = get_connection()
    if connection is not None:
        try:
            for row in get_select_query_results(connection, query):
                team = {}
                for i in range(len(row)):
                    team[parameters[i]] = row[i]
                team_list.append(team)
        except Exception as e:
            print(e, file=sys.stderr)
        connection.close()
    return json.dumps(team_list)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
app.run(host=host, port=int(port), debug=True)