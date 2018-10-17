import csv
import unittest
import api

class apiTest(unittest.TestCase):

	def setUp(self):
		self.football_data = api.api("football_test.csv")

	def tearDown(self):
		pass

	#tests odds
	def test_odds_no_team(self):
		self.assertEqual(self.football_data.get_odds(date = "12/8/17", company_list=
		 ["Bet365"]), [[{"date": "12/8/17", "home_team" : 'Watford' , 'away_team':
		'Liverpool'},[{"company_name": "Bet365" , "home_odds": 6, "draw_odds": 4.2, 
		"away_odds": 1.62}]]])

	def test_odds_all_parameters(self):
		self.assertEqual(self.football_data.get_odds(date = "20/08/17", team_list = 
			["Utrecht"], company_list = ["InterWeten"]),[[{"date": "20/8/17", 
		"home_team" : 'Utrecht','away_team': 'Willem II'} ,[{"company_name": 
		"InterWeten" , "home_odds": 1.55, "draw_odds": 4, "away_odds": 5.5}]]])

	def test_odds_no_results_old_date(self):
		self.assertEqual(self.football_data.get_odds(date = "11/20/93", team_list = 
			["Celtic"], company_list = ["Stanley Bet"]), [[[]]])

	def test_odds_no_date(self):
		self.assertEqual(self.football_data.get_odds(team_list = ["Mechelen"], 
			company_list =['Bet&Win']), [[{"date": "20/8/17", "home_team":'Mechelen'
			,'away_team' : 'Waasland_Beveren'},[{"company_name": "Bet&Win" , 
			"home_odds": 1.6,"draw_odds": 4.2, "away_odds": 5.25}]]])

	def test_odds_no_company(self):
		self.assertEqual(self.football_data.get_odds(date = "20/08/17", team_list = 
			["Utrecht"]), [{"date": "20/08/17", "home_team" : 'Utrecht' , 'away_team'
			:'Willem II'} , [{"company_name": "Bet365" , "home_odds": 1.55, 
			"draw_odds": 4, "away_odds": 5.5} , {"company_name": "Bet&Win",
			"home_odds": 1.55, "draw_odds": 4.2, "away_odds": 6} , {"company_name": 
			"InterWeten" , "home_odds": 1.55, "draw_odds": 4, "away_odds": 5.5}]])

	def test_odds_no_parameters(self):
		self.assertEqual(self.football_data.get_odds(), [[[{"date": 
			"12/8/17", "home_team" : 'Watford' , 'away_team' : 'Liverpool'} ,
			[{"company_name": "Bet365" , "home_odds": 6, "draw_odds": 4.2, 
			"away_odds": 1.62} , {"company_name": "Bet&Win" , "home_odds": 6, 
			"draw_odds": 4.2, "away_odds": 1.55} , {"company_name": "Interweten" , 
			"home_odds": 5.5, "draw_odds": 4, "away_odds": 1.6}]]], 
			[{"date": "20/08/17", "home_team" : 'Utrecht' , 'away_team' : 
			'Willem II'} , [{"company_name": "Bet365" , "home_odds": 1.55, 
			"draw_odds": 4, "away_odds": 5.5} , {"company_name": "Bet&Win" , 
			"home_odds": 1.55, "draw_odds": 4.2, "away_odds": 6} , {"company_name": 
			"InterWeten" , "home_odds": 1.55, "draw_odds": 4, "away_odds": 5.5}]],
			[{"date": "20/8/17", "home_team" : 'Mechelen' , 'away_team' :
			'Waasland-Beveren'} , [{"company_name": "Bet365" , "home_odds": 2.75, 
			"draw_odds": 3.5, "away_odds": 2.39} ,{"company_name": "Bet&Win" , 
			"home_odds": 2.9, "draw_odds": 3.3, "away_odds": 2.5} ,{"company_name": 
			"Interweten" , "home_odds":2.75, "draw_odds": 3.3, "away_odds": 2.4}]]])

	#tests team stats
	def test_get_stats_one_team_home_goals(self):
		self.assertEqual(self.football_data.get_stats(team_list = ["Watford"],
			stat_list =["home_goals"]), [{'team_name': 'Watford', 'home_goals': 3}])

	def test_get_stats_two_teams_AS(self):
		self.assertEqual(self.football_data.get_stats(team_list = ["Watford",
			"Liverpool"],stat_list = ["away_shots"]), [{'team_name':'Watford', 
		'away_shots': 0},{'team_name': 'Liverpool', 'away_shots': 14}])

	def test_get_stats_two_teams_HC_AG(self):
		self.assertEqual(self.football_data.get_stats(team_list = ['Utrecht',
			'Waasland-Beveren'], stat_list =['home_corners' , 'away_goals']), 
		[{'team_name': 'Utrecht', 'home_corners': 3 , 'away_goals':0} ,{'team_name': 
		'Waasland-Beveren', 'home_corners': 4 , 'away_goals':0} ])

	def test_get_stats_two_teams_HST_HF_AY(self):
		self.assertEqual(self.football_data.get_stats(
			team_list=['Waasland-Beveren', 'Standard'],stat_list=[
			'home_shots_on_target' , 'home_fouls', 'away_yellow_cards']),[{
		'team_name': 'Waasland-Beveren', 'home_shots_on_target': 7 , 'home_fouls':19
		, 'away_yellow_cards': 3} , {'team_name': 'Standard','home_shots_on_target':
		0 , 'home_fouls':0 , 'away_yellow_cards': 2}])

	def test_get_stats_one_team_HS_AS_null_dates(self):
		self.assertEqual(self.football_data.get_stats(
			team_list=['Waasland-Beveren'],stat_list=['home_shots' , 'away_shots']),
			[{'team_name':'Waasland-Beveren' , 'home_shots':16 , 'away_shots':3}])

	def test_get_stats_one_team_HS_AS_begining_date(self):
		self.assertEqual(self.football_data.get_stats(start_date=['11/3/2018'],
			team_list=['Waasland-Beveren'],stat_list=['home_shots' , 'away_shots']),
		[{'team_name':'Waasland-Beveren' , 'home_shots':0 , 'away_shots':3}])

	def test_get_stats_one_team_HS_AS_end_date(self):
		self.assertEqual(self.football_data.get_stats(end_date=['8/12/17'],
			team_list=['Waasland-Beveren'],stat_list=['home_shots' , 'away_shots'])
		, [{'team_name':'Waasland-Beveren' , 'home_shots':16 , 'away_shots':0}])

	def test_get_stats_all_parameters(self):
		self.assertEquals(self.football_data.get_stats(team_list='all',
			stat_list='all'), [{'team_name': 'Liverpool','wins' : 0, 'losses':0, 
		'draws': 1, 'home_goals': 0, 'away_goals': 3, 'home_half_time_goals': 0, 
		'away_half_time_goals': 1,'home_shots': 0, 'away_shots': 14, 
		'home_shots_on_target' : 0, 'away_shots_on_target': 5, 'home_fouls': 0,
		'away_fouls': 8, 'home_corners': 0, 'away_corners':3, 'home_yellow_cards':0,
		'away_yellow_cards': 3,'home_red_cards': 0, 'away_red_cards': 0}, {
		'team_name': 'Mechelen', 'wins': 1, 'losses': 0, 'draws': 0,'home_goals': 2,
		'away_goals': 0, 'home_half_time_goals': 0, 'away_half_time_goals': 0, 
		'home_shots': 15,'away_shots': 0, 'home_shots_on_target': 8, 
		'away_shots_on_target': 0, 'home_fouls': 22, 'away_fouls': 0,'home_corners':
		12, 'away_corners': 0, 'home_yellow_cards': 3, 'away_yellow_cards': 0, 
		'home_red_cards': 0,'away_red_cards': 0}, {'team_name': 'Standard', 
		'wins': 0, 'losses': 1, 'draws': 0, 'home_goals': 0,'away_goals': 1, 
		'home_half_time_goals': 0,'away_half_time_goals': 1, 'home_shots': 0,
		'away_shots': 9, 'home_shots_on_target': 0,'away_shots_on_target': 4, 
		'home_fouls': 0,'away_fouls': 27,'home_corners': 0, 'away_corners': 6, 
		'home_yellow_cards': 0, 'away_yellow_cards': 3, 'home_red_cards': 0,
		'away_red_cards':0}, {'team_name': 'Waasland-Beveren', 'wins':1, 'losses':1,
		'draws': 0, 'home_goals': 3,'away_goals': 0, 'home_half_time_goals': 1, 
		'away_half_time_goals': 0, 'home_shots': 16, 'away_shots': 3,
		'home_shots_on_target': 7, 'away_shots_on_target': 0, 'home_fouls': 19, 
		'away_fouls': 19, 'home_corners': 4,'away_corners':1, 'home_yellow_cards':1,
		'away_yellow_cards': 3, 'home_red_cards': 0,'away_red_cards': 0},{
		'team_name': 'Watford', 'wins': 0, 'losses': 0,'draws': 1, 'home_goals': 3,
		'away_goals': 0,'home_half_time_goals': 2,'away_half_time_goals': 0, 
		'home_shots': 9,'away_shots': 0,'home_shots_on_target': 4, 
		'away_shots_on_target':0, 'home_fouls': 14, 'away_fouls':0,'home_corners':3,
		'away_corners': 0, 'home_yellow_cards': 0, 'away_yellow_cards': 0, 
		'home_red_cards':0,'away_red_cards':0}, {'team_name': 'Willem II', 'wins':0,
		'losses': 1, 'draws': 0, 'home_goals': 0,'away_goals': 1, 
		'home_half_time_goals': 0,'away_half_time_goals': 0, 'home_shots': 0,
		'away_shots': 4,'home_shots_on_target': 0, 'away_shots_on_target': 4, 
		'home_fouls': 0,'away_fouls': 13,'home_corners': 0,'away_corners': 4, 
		'home_yellow_cards': 0, 'away_yellow_cards': 2, 'home_red_cards': 0, 
		'away_red_cards': 0},{'team_name': 'Utrecht', 'wins': 1, 'losses': 0, 
		'draws': 0, 'home_goals': 2, 'away_goals': 0,'home_half_time_goals': 2, 
		'away_half_time_goals': 0, 'home_shots': 9,'away_shots': 0,
		'home_shots_on_target': 7, 'away_shots_on_target': 0, 'home_fouls': 19, 
		'away_fouls': 0,'home_corners': 4,'away_corners': 0, 'home_yellow_cards': 0,
		'away_yellow_cards': 0, 'home_red_cards': 0, 'away_red_cards': 0}])

	def test_get_stats_no_parameters(self):
		self.assertEquals(self.football_data.get_stats(), [])

	def test_get_stats_single_team_HS_HC(self):
		self.assertEquals(self.football_data.get_stats(team_list=['Willem II'],
			stat_list=['HS','HC']), [{'team_name': 'Willem II','home_shots': 9, 
		'home_corners': 4}])
		
	def test_get_stats_single_team_FTHG_AR(self):
		self.assertEquals(self.football_data.get_stats(team_list=['Watford'],
			stat_list=['FTHG','AR']), [{'team_name': 'Watford','home_goals': 3,
		'away_red_cards': 0}])

	def test_get_stats_single_team_HC_AC(self):
		self.assertEquals(self.football_data.get_stats(team_list=['Mechelen'],
			stat_list=['HC','AC']), [{'team_name': 'Mechelen','home_corners': 12, 
		'away_corners': 0}])

	def test_get_stats_single_team_FTAG_AF(self):
		self.assertEquals(self.football_data.get_stats(team_list=['Standard'],
			stat_list=['FTAG','AF']), [{'team_name': 'Standard','away_goals': 1, 
		'away_fouls': 27}])

	def test_get_stats_single_team_record(self):
		self.assertEquals(self.football_data.get_stats(team_list=['Watford'],
			stat_list=['wins','losses', 'draws']), [{'team_name':'Watford', 
		'wins': 0, 'losses': 1}])

	def test_get_stats_single_team_HS_HC_AF(self):
		self.assertEquals(self.football_data.get_stats(team_list=['Willem II'],
			stat_list=['HS','HC','AF']), [{'team_name': 'Willem II','home_shots': 0,
		'away_fouls': 13, 'home_corners': 0}])

	def test_get_stats_single_team_HTHG_HF_AST(self):
		self.assertEquals(self.football_data.get_stats(team_list=['Utrecht'],
			stat_list=['HTHG','HF','AST']), [{'team_name': 'Utrecht',
		'home_half_time_goals': 2, 'home_fouls': 19, 'away_shots_on_target': 0}])
		
	def test_get_stats_single_team_FTHG_FTAG_AS(self):
		self.assertEquals(self.football_data.get_stats(team_list=['Mechelen'],
			stat_list=['FTHG','FTAG','AS']), [{'team_name': 'Mechelen',
		'home_goals': 2, 'away_goals': 0, 'away_shots': 0}])

	def test_get_stats_single_team_HY_AY_HR_AR(self):
		self.assertEquals(self.football_data.get_stats(team_list=['Liverpool'],
			stat_list=['HY','AY','HR','AR']), [{'team_name':'Liverpool', 
		'home_yellow_cards': 3, 'away_yellow_cards': 0, 'home_red_cards': 0, 
		'away_red_cards': 0}])

	def test_get_stats_single_team_FTHG_FTAH_HTHG_HTAG(self):
		self.assertEquals(self.football_data.get_stats(team_list=['Watford'],
			stat_list=['FTHG','FTAH','HTHG','HTAG']), [{'team_name':'Watford', 
		'home_goals': 3, 'away_goals': 0, 'home_half_time_goals': 2, 
		'away_half_time_goals': 0}])

	def test_get_stats_single_team_FTHG_FTAH_HTHG_HTAG_AS(self):
		self.assertEquals(self.football_data.get_stats(team_list=['Watford'],
			stat_list=['FTHG','FTAH','HTHG','HTAG','AS']), [{'team_name':'Watford', 
		'home_goals': 3,'away_goals': 0, 'home_half_time_goals': 2, 
		'away_half_time_goals': 0, 'away_shots': 0}])

	def test_get_stats_four_teams_FTHG_FTAG_HS_AS_HY_AY_HR_AR(self):
		self.assertEquals(self.football_data.get_stats(team_list=['Liverpool',
			'Standard','Watford','Willem II'], stat_list=['FTHG', 'FTAG', 'HS', 
			'AS', 'HY', 'AY', 'HR', 'AR']),[{'team_name': 'Liverpool', 
		'home_goals': 0, 'away_goals': 3,'home_shots': 0, 'away_shots': 14, 
		'home_yellow_cards': 0, 'away_yellow_cards': 3, 'home_red_cards': 0,
		'away_red_cards': 0}, {'team_name': 'Standard', 'home_goals': 0, 
		'away_goals': 1, 'home_shots': 0, 'away_shots': 9,'home_yellow_cards': 0, 
		'away_yellow_cards': 3, 'home_red_cards': 0, 'away_red_cards': 0}, {
		'team_name': 'Watford','home_goals': 3, 'away_goals': 0, 'home_shots': 9, 
		'away_shots': 0, 'home_yellow_cards': 0, 'away_yellow_cards': 0,
		'home_red_cards': 0, 'away_red_cards': 0}, {'team_name': 'Willem II', 
		'home_goals': 0, 'away_goals': 1,'home_shots': 0, 'away_shots': 4, 
		'home_yellow_cards': 0, 'away_yellow_cards': 2, 'home_red_cards': 0,
		'away_red_cards': 0}])

if __name__ == '__main__':
	unittest.main()



		

