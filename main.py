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
        if '.htm' in filename:
            print(filename)
            filesToRead.append(filename)
    print(len(filesToRead),' files to process')

    filesToRead = sorted(filesToRead)

    direcciones_de_grupo = []
    grupos_principales = []
    grupos_secundarios = []
    grupos_individuales = []

    for htmlfile in filesToRead:
        print(htmlfile)
        data = open(args.folder+'/'+htmlfile)
        soup = BeautifulSoup(data,'html')
        tables = soup.find_all('table')
        row_table_list = []
        for table in tables:
            rows = table.find_all('tr')
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
            if row:
                if row[0] == "Dirección Individual":
                    print(row[0],' :',row[1])
                if row[0] == "Programa de aplicación":
                    print(row[0],' :',row[1])
                if row[0] == "Número de Serie":
                    print(row[0],' :',row[1])
                # Objects:
                if 'Obj#' in row[0]:
                    print(row[0],' :',row[1])
                    for group_address in row[1].split(' '):
                        if not group_address in direcciones_de_grupo:
                            direcciones_de_grupo.append(group_address)
                        principal, secundario, individual = group_address.split('/')
                        principal =  int(principal)
                        secundario = int(secundario)
                        individual = int(individual)
                        if not principal in grupos_principales:
                            grupos_principales.append(principal)
                        if not secundario in grupos_secundarios:
                            grupos_secundarios.append(secundario)
                        if not individual in grupos_individuales:
                            grupos_individuales.append(individual)

    direcciones_de_grupo = sorted(direcciones_de_grupo)
    print('\tDirecciones de grupo totales:')
    print(direcciones_de_grupo)

    grupos_principales = sorted(grupos_principales)
    print('\tDirecciones principales:')
    print(grupos_principales)
    grupos_secundarios = sorted(grupos_secundarios)
    print('\tDirecciones secundarias:')
    print(grupos_secundarios)
    grupos_individuales = sorted(grupos_individuales)
    print('\tDirecciones individuales:')
    print(grupos_individuales)


        
        
