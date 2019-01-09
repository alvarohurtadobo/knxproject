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
            output_file.write('\nStarted file')

        output_file = open(output_file_name,'a')
        output_file.write('\nFiles to be tested:')
        filesToRead = []
        for filename in os.listdir('./' + key):
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
            lastDevice = htmlfile.split('_')[-1].split('.')[0]
            output_file.write('\n'+htmlfile)
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
                        #output_file.write('\n\tValue: '+value)
                    row_table_list.append(column_list)
                    #output_file.write('\n\tCol: '+str(len(column_list)))
            lastAddress = 'No Address'
            for row in row_table_list:
                if row:
                    if "Individual" in row[0]:
                        output_file.write('\n\t'+row[0]+' :'+row[1])
                        lastAddress = row[1]
                    if "Programa de " in row[0]:
                        output_file.write('\n\t'+row[0]+' :'+row[1])
                    if "de Serie" in row[0]:
                        output_file.write('\n\t'+row[0]+' :'+row[1])
                    # Objects:
                    if 'Obj#' in row[0]:
                        output_file.write('\n\t'+row[0]+' :'+row[1])
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
                                            'name': 'unknown',
                                            'literal':'Control Domotico',
                                            'area':key[2:].replace('_',' '),
                                            'IP':ipaddress,
                                            'read group':groups[0],
                                            'write group':groups[1],
                                            'command':'on/off',
                                            'device':lastAddress,
                                            'comment':lastDevice,
                                            'other groups':groups[2]})
                        device_number += 1

    with open(output_csv_name, 'w') as csvMainFile:
        fieldnames = ['id', 'name','literal','area','IP','read group','write group','value','command','device','comment','other groups']
        writer = csv.DictWriter(csvMainFile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        with open(output_other_csv_name, 'w') as csvOtherFile:
            fieldnames = ['id', 'name','literal','area','IP','read group','write group','value','command','device','comment','other groups']
            otherWriter = csv.DictWriter(csvOtherFile, fieldnames=fieldnames, delimiter=',')
            otherWriter.writeheader()
            for item in toCSVlist:
                if 'output' in item['comment']:
                    writer.writerow(item)
                else:
                    otherWriter.writerow(item)

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


        
        
