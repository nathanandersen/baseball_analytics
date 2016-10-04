# Masks for pandas

def filter_middle_season_mask(df):
	return df['date'].month > 4 and df['date'].month < 9

def training_set_by_date_mask(df):
	return ((df['date'] > '2012-01-01') & (df['date'] < '2012-12-31')) |\
	((df['date'] > '2010-01-01') & (df['date'] <'2010-12-31')) |\
	((df['date'] > '2008-01-01') & (df['date'] <'2008-12-31')) |\
	((df['date'] > '2006-01-01') & (df['date'] <'2006-12-31')) |\
	((df['date'] > '2004-01-01') & (df['date'] <'2004-12-31'))

def test_set_by_date_mask(df):
	return ((df['date'] > '2011-01-01') & (df['date'] < '2011-12-31')) |\
	((df['date'] > '2009-01-01') & (df['date'] <'2009-12-31')) |\
	((df['date'] > '2007-01-01') & (df['date'] <'2007-12-31')) |\
	((df['date'] > '2005-01-01') & (df['date'] <'2005-12-31')) |\
	((df['date'] > '2003-01-01') & (df['date'] <'2003-12-31'))