import os
import csv
import pandas as pd
from bs4 import BeautifulSoup

IPs = { '0_Sala_multiple':'192.168.8.254',
        '1_Sala_vip':'192.168.4.214',
        '2_Plaza_comidas':'192.168.2.86',
        '3_Auditorios':'192.168.6.254'}

if __name__ == "__main__":
    output_csv_name = './main_devices.csv'
    output_other_csv_name = './other_devices.csv'
    device_number = 0
    toCSVlist = []
    for key, ipaddress in IPs.items():
        output_file_name = './' + key +'.txt'
        with open(output_file_name,'w') as output_file:
            print('\nStarted file')

        output_file = open(output_file_name,'a')
        print('\nFiles to be tested:')
        filesToRead = []
        for filename in os.listdir('./' + key):
            if '.htm' in filename:
                print('\n\t'+filename)
                filesToRead.append(filename)
        print('\n'+str(len(filesToRead))+' files to process')

        filesToRead = sorted(filesToRead)

        direcciones_de_grupo = []
        grupos_principales = []
        grupos_secundarios = []
        grupos_individuales = []

        for htmlfile in filesToRead:
            lastDevice = htmlfile.split('_')[-1].split('.')[0]
            print('\n'+htmlfile)
            data = open('./' + key + '/'+htmlfile)
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
                        #print('\n\tValue: '+value)
                    row_table_list.append(column_list)
                    #print('\n\tCol: '+str(len(column_list)))
            lastAddress = 'No Address'
            for row in row_table_list:
                if row:
                    if "Individual" in row[0]:
                        print('\n\t'+row[0]+' :'+row[1])
                        lastAddress = row[1]
                    if "Programa de " in row[0]:
                        print('\n\t'+row[0]+' :'+row[1])
                    if "de Serie" in row[0]:
                        print('\n\t'+row[0]+' :'+row[1])
                    # Objects:
                    if 'Obj#' in row[0]:
                        print(row)
                        if len(row) > 1:
                            print('\n\t'+row[0]+' :'+row[1])
                            all_groups = row[1].split(' ')

                            groups = ["","",""]
                            amount_groups = len(all_groups)
                            if amount_groups == 1: 
                                groups[0] = all_groups[0]
                            elif amount_groups == 2:
                                groups[0] = all_groups[0]
                                groups[1] = all_groups[1]
                            elif amount_groups >2:
                                groups[0] = all_groups[0]
                                groups[1] = all_groups[1]
                                groups[2] = ' '.join(all_groups[2:])
                            """
                            for group in groups:
                                if '23/7/' in group:
                                    group.replace('23/7/0','')
                                    group.replace('23/7/1','')
                                    group.replace('23/7/2','')
                                    group.replace('23/7/3','')
                            """

                            for group_address in all_groups:

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
                            toCSVlist.append({   'id': device_number,
                                                'name': '-',
                                                'literal':'-',
                                                'area':key[2:].replace('_',' '),
                                                'IP':ipaddress,
                                                'read group':groups[0],
                                                'write group':groups[1],
                                                'command':'on/off',
                                                'device':lastAddress,
                                                'object':row[0],
                                                'comment':lastDevice,
                                                'other groups':groups[2]})
                            device_number += 1

    with open(output_csv_name, 'w') as csvMainFile:
        fieldnames = ['id', 'name','literal','area','IP','read group','write group','value','command','device','object','comment','other groups']
        writer = csv.DictWriter(csvMainFile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        with open(output_other_csv_name, 'w') as csvOtherFile:
            fieldnames = ['id', 'name','literal','area','IP','read group','write group','value','command','device','object','comment','other groups']
            otherWriter = csv.DictWriter(csvOtherFile, fieldnames=fieldnames, delimiter=',')
            otherWriter.writeheader()
            for item in toCSVlist:
                if 'output' in item['comment']:
                    writer.writerow(item)
                else:
                    otherWriter.writerow(item)

    direcciones_de_grupo = sorted(direcciones_de_grupo)
    
    print('\n####################################################################\n')

    grupos_principales = sorted(grupos_principales)
    print('\nDirecciones principales:')
    for item in grupos_principales:
        print('\n\t-\t'+str(item))

    grupos_secundarios = sorted(grupos_secundarios)
    print('\nDirecciones secundarias:')
    for item in grupos_secundarios:
        print('\n\t-\t'+str(item))

    grupos_individuales = sorted(grupos_individuales)
    print('\nDirecciones individuales:')
    for item in grupos_individuales:
        print('\n\t-\t'+str(item))

    print('\n####################################################################\n')

    print('\nDirecciones de grupo totales:')
    for item in direcciones_de_grupo:
        print('\n\t-\t'+str(item))

    output_file.close()


        
        
