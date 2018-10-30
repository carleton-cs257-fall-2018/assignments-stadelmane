import csv

def get_teams():
	teams = []
	counter = 1
	with open("superlig.csv") as csv_file:
		for row in csv.reader(csv_file, delimiter=','):
			for col in row:
				team_in_list = False
				for team in teams:
					if team['name']==col:
						team_in_list = True
						pass
				if team_in_list == False:
					teams.append({'name': col , 'ID': counter})
					counter +=1
	print(teams)
	return(teams)


def team_name(team_list, csv_file_name):
    output_file = open(csv_file_name, 'w', encoding='utf-8')
    writer = csv.writer(output_file)
    for team in team_list:
        team_row = [team['name'],team['ID']]
        writer.writerow(team_row)
    print("worked")
    output_file.close()

def main():
	teams={}
	teams = get_teams()
	print(teams)
	team_name(teams, 'super.csv')
main()