import os
import argparse
import pandas as pd
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description = 'Next options available')
parser.add_argument("-f", "--folder", type=str, default = './test_data', help = "Specify folder to work with")
args = parser.parse_args()

if __name__ == "__main__":
    print('Files to be tested:')
    filesToRead = []
    for filename in os.listdir(args.folder):
        if '.html' in filename:
            print(filename)
            filesToRead.append(filename)
    print(len(filesToRead),' files to process')

    filesToRead = sorted(filesToRead)

    for htmlfile in filesToRead:
        print(htmlfile)
        data = open(args.folder+'/'+htmlfile)
        soup = BeautifulSoup(data,'html')
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            row_table_list = []
            for row in rows:
                columns = row.find_all('td')
                column_list = []
                for column in columns:
                    value = column.get_text()
                    column_list.append(value)
                    #print('\tValue: ',value)
                row_table_list.append(column_list)
                #print('\tCol: ',len(column_list))
            for row in row_table_list:
                print(row)
        