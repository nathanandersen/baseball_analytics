#Generates data set to tell if starter is removed

__all__ = ["predict_starter_removed_team_oblivious","predict_starter_removed_team_oblivious_headers"]

import game_model

stats_headers = ["date","pid","starter_pulled_this_play","starter_pulled_already","fielding","inning",\
				"top","score_diff","outs","first","second","third",\
				"position_in_lineup","pitches_since_last","hits_since_last","leverage","change_in_leverage"]

def predict_starter_removed_team_oblivious_headers():
	return stats_headers

def predict_starter_removed_team_oblivious(domain):
	for g in domain.games:
		if g.american_league:
			#first find all substitution states - this will be important!
			sub_states = set()
			for sub_state,pitch_sub in g.pitching_substitutions.iteritems():
				sub_states.add(sub_state)

			#set leverage equal to start game leverage
			start_state = game_model.GameState.start()
			previous_leverage = domain.win_exp_table.get_leverage(game_model.GameState.start())
			home_pulled,away_pulled = False,False
			for state in g.game_progression:
				if state != start_state:
					current_leverage = domain.win_exp_table.get_leverage(state)
					if state not in sub_states:
						yield get_stats_for_team_no_starter_pull(g,\
																state,\
																current_leverage,\
																previous_leverage,\
																home_pulled,
																True)
						yield get_stats_for_team_no_starter_pull(g,\
																state,\
																current_leverage,\
																previous_leverage,\
																away_pulled,\
																False)
					else:
						ps = g.pitching_substitutions[state]
						if not ((ps.home_team and home_pulled) or ((not ps.home_team) and away_pulled)):
							#update tracking
							home_pulled = True if ps.home_team else home_pulled
							away_pulled = away_pulled if ps.home_team else True

							#now build the row
							data = [g.date]
							data.append(ps.pitcher_id)
							data.append(1)
							data.append(0)
							if (ps.home_team and ps.gamestate.inning.top) or\
								((not ps.home_team) and (not ps.gamestate.inning.top)):
								data.append(1)
							else:
								data.append(0)
							data = data + ps.gamestate.to_numeric_list(ps.home_team)
							data.append(state.position_in_lineup(perspective_home=ps.home_team))
							data.append(ps.pitches_since_last_substitution)
							data.append(ps.gamestate.pitching_appearance_tracker_home.hits if ps.home_team\
											else ps.gamestate.pitching_appearance_tracker_away.hits)
							data.append(current_leverage)
							data.append(current_leverage - previous_leverage)
							yield data
						else:
							get_stats_for_team_no_starter_pull(g,\
																ps.gamestate,\
																current_leverage,\
																previous_leverage,\
																home_pulled if ps.home_team else away_pulled,\
																ps.home_team)

						#need to add other teams perspective
						yield get_stats_for_team_no_starter_pull(g,\
																ps.gamestate,\
																current_leverage,\
																previous_leverage,\
																away_pulled if ps.home_team else home_pulled,\
																not ps.home_team)
					previous_leverage = current_leverage

def get_stats_for_team_no_starter_pull(g,state,current_leverage,previous_leverage,starter_pulled,home):
	data = [g.date]
	data.append(None)
	data.append(0)
	data.append(1 if starter_pulled else 0)
	#fielding?
	if state.inning.top:
		data.append(1 if home else 0)
	else:
		data.append(0 if home else 1)
	data = data + state.to_numeric_list(home)
	data.append(state.position_in_lineup(perspective_home=home))
	data.append(state.pitching_appearance_tracker_home.pitches if home else state.pitching_appearance_tracker_away.pitches)
	data.append(state.pitching_appearance_tracker_home.hits if home else state.pitching_appearance_tracker_away.hits)
	data.append(current_leverage)
	data.append(current_leverage - previous_leverage)
	return data