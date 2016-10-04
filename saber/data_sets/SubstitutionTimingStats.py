# STATS USEFUL FOR PREDICITING WHEN PITCHING SUBSTITUTIONS ARE MADE

import game_model

__all__ = ["predict_substitution_timing_stats_team_oblivious","predict_substitution_timing_stats_team_oblivious_headers"]

#question mark indicates categorical variable
# to add, rank of current team, rank of tomorrow's team, rank of two, three days team
#date,pitcher,home_team?,inning,top?,score_diff,outs,first?,second?,third?,pitches_since_last,leverage
stats_headers = ["date","pid","substitution","fielding","inning",\
				"top","score_diff","outs","first","second","third",\
				"position_in_lineup","pitches_since_last","leverage","change_in_win_exp"]

def predict_substitution_timing_stats_team_oblivious_headers():
	return stats_headers

def predict_substitution_timing_stats_team_oblivious(domain):
	for g in domain.games:
		if g.american_league:
			#first find all substitution states - this will be important!
			sub_states = set()
			for sub_state,pitch_sub in g.pitching_substitutions.iteritems():
				sub_states.add(sub_state)

			#set leverage equal to start game leverage
			start_state = game_model.GameState.start()
			previous_leverage = domain.win_exp_table.get_leverage(game_model.GameState.start())
			for state in g.game_progression:
				if state != start_state:
					current_leverage = domain.win_exp_table.get_leverage(state)
					if state not in sub_states:
						yield get_stats_for_team_no_sub(g,state,current_leverage,previous_leverage,True)
						yield get_stats_for_team_no_sub(g,state,current_leverage,previous_leverage,False)
					else:
						ps = g.pitching_substitutions[state]
						data = [g.date]
						data.append(ps.pitcher_id)
						data.append(1)
						if (ps.home_team and ps.gamestate.inning.top) or ((not ps.home_team) and (not ps.gamestate.inning.top)):
							data.append(1)
						else:
							data.append(0)
						data = data + ps.gamestate.to_numeric_list(ps.home_team)
						data.append(state.position_in_lineup(perspective_home=ps.home_team))
						data.append(ps.pitches_since_last_substitution)
						data.append(current_leverage)
						data.append(current_leverage - previous_leverage)
						yield data
						#now yield the other team's view
						yield get_stats_for_team_no_sub(g,ps.gamestate,current_leverage,previous_leverage,not ps.home_team)

					previous_leverage = current_leverage

def get_stats_for_team_no_sub(g,state,current_leverage,previous_leverage,home):
	data = [g.date]
	data.append(None)
	data.append(0)
	#fielding?
	if state.inning.top:
		data.append(1 if home else 0)
	else:
		data.append(0 if home else 1)
	data = data + state.to_numeric_list(home)
	data.append(state.position_in_lineup(perspective_home=home))
	data.append(state.pitching_appearance_tracker_home.pitches if home\
					else state.pitching_appearance_tracker_away.pitches)
	data.append(current_leverage)
	data.append(current_leverage - previous_leverage)

	return data