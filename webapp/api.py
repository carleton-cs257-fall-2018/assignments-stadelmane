#!/usr/bin/env python3
'''
    api.py
    Eric Stadelman and Charlie Broadbent 21 October 2018
    Simple Flask API used in the sample web app for
    CS 257 used for soccer data
'''
import sys
import flask
import json
import psycopg2

app = flask.Flask(__name__, static_folder='static', template_folder='templates')


def get_connection():
    '''
    Returns a connection to the database described
    in the config module. Returns None if the
    connection attempt fails.
    '''
    connection = None
    try:
        connection = psycopg2.connect(database='stadelmane',
                                      user='stadelmane',
                                      password='mango375eyee')
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


@app.route('/stats/all_stats')
def get_all_stats():
    query = 'SELECT * FROM matches;'
    parameters = []
    query_column_names = "SELECT column_name from information_schema.columns where table_name = 'matches'"
    connection = get_connection()
    if connection is not None:
        try:
            for row in get_select_query_results(connection, query_column_names):
                for i in range(len(row)):
                    parameters.append(row[i])
        except Exception as e:
            print(e, file=sys.stderr)
    stats_list = []
    if connection is not None:
        try:
            for row in get_select_query_results(connection, query):
                stat = {}
                for i in range(len(row)):
                    stat[parameters[i]] = row[i]
                stats_list.append(stat)
        except Exception as e:
            print(e, file=sys.stderr)
        connection.close()
    return json.dumps(stats_list, sort_keys = True, default = str)


@app.route('/stats/<team_id>')
def get_stats(team_id):
    parameters = ['VCH' , 'home_team_id']
    query = 'SELECT '
    for i in range(len(parameters)):
        if i==(len(parameters)-1):
            query = query + parameters[i] + ' '
        else:
            query = query + parameters[i] + ', '
    query = query + 'FROM matches'
    query = query + ' WHERE home_team_id = ' + team_id


    stats_list = []
    connection = get_connection()
    if connection is not None:
        try:
            for row in get_select_query_results(connection, query):
                stat = {}
                for i in range(len(row)):
                    stat[parameters[i]] = row[i]
                print(stat)
                stats_list.append(stat)
        except Exception as e:
            print(e, file=sys.stderr)
        connection.close()
    return json.dumps(stats_list, sort_keys = True, default = str)


@app.route('/teams/')
def get_teams():
    parameters = ['league','team']
    query = 'SELECT '
    for i in range(len(parameters)):
        if i==(len(parameters)-1):
            query = query + parameters[i] + ' '
        else:
            query = query + parameters[i] + ', '
    query = query + 'FROM teams'

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
