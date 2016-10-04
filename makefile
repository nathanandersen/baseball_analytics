rosters:
	python -m build.build_rosters

parsed_games:
	python -m build.build_parsed_games

parsed_data: rosters parsed_games
	python -m build.build_win_expectancy_and_leverage_table

clean:
	find ./data_parsed/ -type f -name "*.pkl" -exec rm -f {} \;
	find ./data_parsed/ -type f -name "*.csv" -exec rm -f {} \;
	find ./ -type f -name "*.pyc" -exec rm -f {} \;

all_test:
	python -m build.build_rosters --years 2010 2011
	python -m build.build_parsed_games --years 2010 2011
	python -m build.build_win_expectancy_and_leverage_table --years 2010 2011

all: clean parsed_data