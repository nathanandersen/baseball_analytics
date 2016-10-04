# This script will create pitcher lists for specified years

import os
import argparse
import csv
from GLOBAL_VARS import *

#create the argument parser
argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--years",nargs='+',type=int)

def parse_rosters(dir_list):
    for year in dir_list:
        data = []
        for data_file in os.listdir(RAW_DATA_PATH + "/" + year):
            _,extension = os.path.splitext(data_file)
            if extension == ".ROS":
                with open(RAW_DATA_PATH + "/" + year + "/" + data_file,'rb') as csvfile:
                    csvreader = csv.reader(csvfile, delimiter=',',quotechar='"')
                    for row in csvreader:
                        data.append([row[0],row[2] + " " + row[1],row[4],row[3],row[6]])

        #now write all players from dir to file
        with open(PARSED_DATA_PATH + "/" + year + "/" + ROSTER_FILE_NAME,'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)

            #write header
            csvwriter.writerow(['retrosheet_code','full_name','throws','bats','position'])
            for row in data:
                csvwriter.writerow(row)

if __name__ == "__main__":
    args = argument_parser.parse_args()
    dir_list = None
    if args.years:
        dir_list = [str(y) for y in args.years]
    else:
        dir_list = [ name for name in os.listdir(RAW_DATA_PATH) if os.path.isdir(os.path.join(RAW_DATA_PATH, name)) ]

    parse_rosters(dir_list)