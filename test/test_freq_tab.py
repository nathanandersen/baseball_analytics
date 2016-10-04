from parser import *
from game_model import *
from saber import *
import cPickle as pickle

file_table = open("data_parsed/frequency_table.pkl", 'rb')
freq_tab = pickle.load(file_table)
file_table.close()

freq_tab.write_table_latex("freq_tab.txt",start_inning=8,end_inning=9,score_differential = 1,perspective_home=True)