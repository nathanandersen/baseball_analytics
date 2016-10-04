# Predict the Closer is used - includes special and general cases

import game_model

__all__ = ['predict_mariano_rivera_used_given_substitution','predict_mariano_rivera_used_given_substitution_headers',\
			'predict_mariano_rivera_used_general_away','predict_mariano_rivera_used_general_away_headers',\
			'predict_mariano_rivera_used_general_home','predict_mariano_rivera_used_general_home_headers']

#Global Vars
YANKEES_ID = 'NYA'
MARIANO_ID = 'rivem002'


def predict_mariano_rivera_used_given_substitution_headers():
	return ["date","mariano","home","fielding","inning","bottom","score_diff","outs","first","second","third",\
			"inning_start","position_in_lineup","leverage","win_exp",'score_diff_lt3']


#lets start simple:
def predict_mariano_rivera_used_given_substitution(domain):
	for g in domain.games:
		if g.american_league and (g.home_team == YANKEES_ID or g.away_team == YANKEES_ID):
			for sub_state,pitch_sub in g.pitching_substitutions.iteritems():
				if pitch_sub.team_id == YANKEES_ID:
					data = []
					data.append(g.date)
					data.append(1 if pitch_sub.pitcher_id == MARIANO_ID else 0)
					data.append(1 if pitch_sub.home_team else 0)
					data.append(1 if pitch_sub.home_team and sub_state.inning.top else 0)
					data = data + sub_state.to_numeric_list(perspective_home=pitch_sub.home_team)
					data.append(1 if sub_state.outs == 0 and (sub_state.base_runners == game_model.BaseRunners.bases_empty()) else 0)
					data.append(pitch_sub.position_in_lineup)
					data.append(domain.win_exp_table.get_leverage(sub_state))
					data.append(domain.win_exp_table.get_win_expectancy(sub_state,pitch_sub.home_team))
					data.append(1 if sub_state.score_differential(pitch_sub.home_team) < 4\
									and sub_state.score_differential(pitch_sub.home_team) >= 0\
								else 0)
					yield data

def predict_mariano_rivera_used_general(domain,home):
	for g in domain.games:
		if g.american_league and (home and g.home_team == YANKEES_ID or (not home) and g.away_team == YANKEES_ID):
			sub_states = set()
			for sub_state,pitch_sub in g.pitching_substitutions.iteritems():
				sub_states.add(sub_state)

			for state in g.game_progression:
				data = []
				if state in sub_states:
					data.append(1 if g.pitching_substitutions[state].pitcher_id == MARIANO_ID else 0)
				else:
					data.append(0)
				data.append(1 if (state.inning.top and home or state.inning.bottom and (not home)) else 0)
				data = data + state.to_numeric_list(perspective_home=home)
				data.append(1 if state.outs == 0 and (state.base_runners == game_model.BaseRunners.bases_empty()) else 0)
				data.append(state.position_in_lineup(home))
				data.append(domain.win_exp_table.get_leverage(state))
				data.append(domain.win_exp_table.get_win_expectancy(state,home))
				data.append(1 if state.score_differential(home) < 4\
								and state.score_differential(home) >= 0\
							else 0)
				yield data

def predict_mariano_rivera_used_general_away_headers():
	return ["mariano_in","fielding","inning","bottom","score_diff","outs","first","second","third",\
			"inning_start","position_in_lineup","leverage","win_exp",'score_diff_lt3']

def predict_mariano_rivera_used_general_away(domain):
	return predict_mariano_rivera_used_general(domain,False)

def predict_mariano_rivera_used_general_home_headers():
	return ["mariano_in","fielding","inning","bottom","score_diff","outs","first","second","third",\
			"inning_start","position_in_lineup","leverage","win_exp",'score_diff_lt3']

def predict_mariano_rivera_used_general_home(domain):
	return predict_mariano_rivera_used_general(domain,True)