import os
import csv
import argparse
import pandas as pd
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description = 'Next options available')
parser.add_argument("-f", "--folder", type=str, default = './3_auditorios', help = "Specify folder to work with")
args = parser.parse_args()

IPs = { '0_sala_multiple':'192.168.8.254',
        '1_sala_vip':'192.168.4.214',
        '2_plaza_comidas':'192.168.2.86',
        '3_auditorios':'192.168.6.254'}

if __name__ == "__main__":
    output_file_name = args.folder+'.txt'
    with open(output_file_name,'w') as output_file:
        output_file.write('\nStarted file')

    output_file = open(output_file_name,'a')
    output_file.write('\nFiles to be tested:')
    filesToRead = []
    for filename in os.listdir(args.folder):
        if '.htm' in filename:
            output_file.write('\n\t'+filename)
            filesToRead.append(filename)
    output_file.write('\n'+str(len(filesToRead))+' files to process')

    filesToRead = sorted(filesToRead)

    direcciones_de_grupo = []
    grupos_principales = []
    grupos_secundarios = []
    grupos_individuales = []

    for htmlfile in filesToRead:
        output_file.write('\n'+htmlfile)
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
                    #output_file.write('\n\tValue: '+value)
                row_table_list.append(column_list)
                #output_file.write('\n\tCol: '+str(len(column_list)))

        for row in row_table_list:
            if row:
                if "Individual" in row[0]:
                    output_file.write('\n\t'+row[0]+' :'+row[1])
                if "Program" in row[0]:
                    output_file.write('\n\t'+row[0]+' :'+row[1])
                if "de Serie" in row[0]:
                    output_file.write('\n\t'+row[0]+' :'+row[1])
                # Objects:
                if 'Obj#' in row[0]:
                    output_file.write('\n\t'+row[0]+' :'+row[1])
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
    
    output_file.write('\n####################################################################\n')

    grupos_principales = sorted(grupos_principales)
    output_file.write('\nDirecciones principales:')
    for item in grupos_principales:
        output_file.write('\n\t-\t'+str(item))

    grupos_secundarios = sorted(grupos_secundarios)
    output_file.write('\nDirecciones secundarias:')
    for item in grupos_secundarios:
        output_file.write('\n\t-\t'+str(item))

    grupos_individuales = sorted(grupos_individuales)
    output_file.write('\nDirecciones individuales:')
    for item in grupos_individuales:
        output_file.write('\n\t-\t'+str(item))

    output_file.write('\n####################################################################\n')

    output_file.write('\nDirecciones de grupo totales:')
    for item in direcciones_de_grupo:
        output_file.write('\n\t-\t'+str(item))

    output_file.close()


        
        
