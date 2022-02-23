import pyodbc
import csv
import datetime
import paramiko
from datetime import datetime, timedelta


try: 
  conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=NAGCA01;'
                      'Database=Archive;'
			'UID=*missing*'
			'PWD=*missing*')
except:
  pass

offset=1
d = datetime.today() - timedelta(days=offset)
timestr = d.strftime("%Y_%m_%d")


    
def export():


    #SPAJANJE NA SERVER

    username = #
    password = #                                          
    host = '10.20.81.67'
    directory = '/ArchiveReportProza/Regulacija/'

    transport = paramiko.Transport(host)
    transport.connect(username = username, password = password) 
    sftp = paramiko.SFTPClient.from_transport(transport)

    path = sftp.listdir(directory)
    print(path)

    cursor = conn.cursor()

    E1 = ('''SELECT o.DataKey, r.UtcTime, r.Value
	    FROM [Archive].[dbo].[DataKeyValue] as r
            JOIN DataKey o
	    ON o.DataKeyId = r.DataKeyId
            WHERE (r.DataKeyId=110 or r.DataKeyId=120 or r.DataKeyId=249  or r.DataKeyId=301 or r.DataKeyId=198
              or r.DataKeyId=1081 or r.DataKeyId=1082 or r.DataKeyId=1079 or r.DataKeyId=399 or r.DataKeyId=453
              or r.DataKeyId=507 or r.DataKeyId=557 or r.DataKeyId=715 or r.DataKeyId=611 or r.DataKeyId=665
              or r.DataKeyId=1087 or r.DataKeyId=1089 or r.DataKeyId=1088 or r.DataKeyId=1084 or r.DataKeyId=3549) 
            and (Time between DATEADD(dd, 0, DATEDIFF(dd, 0, GETDATE()-{})) and  DATEADD(dd, 0, DATEDIFF(dd, 0, GETDATE()-{}+1))) order by UtcTime asc'''.format(offset, offset))
    
    cursor.execute(E1)
    result = cursor.fetchall()

    
    name1 = "AGC_Export_Indikacije_" + timestr + ".csv"
    
    with open(name1,"w", newline='') as file:
        
        #csv.writer(file).writerow(x[0] for x in cursor.description)
        writer = csv.writer(file, delimiter=";")
        writer.writerows(result)
        
    sftp.put(name1, directory + name1)
    
    E2 = ('''SELECT o.DataKey, r.UtcTime, r.Value
	    FROM [Archive].[dbo].[DataKeyValue] as r
            JOIN DataKey o
	    ON o.DataKeyId = r.DataKeyId
            WHERE (r.DataKeyId=1115 or r.DataKeyId=150 or r.DataKeyId=1116 or r.DataKeyId=1117 or r.DataKeyId=1114
              or r.DataKeyId=227 or r.DataKeyId=279 or r.DataKeyId=329 or r.DataKeyId=1118 or r.DataKeyId=1119
              or r.DataKeyId=1120 or r.DataKeyId=426 or r.DataKeyId=483 or r.DataKeyId=535 or r.DataKeyId=1121
              or r.DataKeyId=1124 or r.DataKeyId=1122 or r.DataKeyId=1123 or r.DataKeyId=584 or r.DataKeyId=641
              or r.DataKeyId=693 or r.DataKeyId=742 or r.DataKeyId=8 or r.DataKeyId=32 or r.DataKeyId=72
              or r.DataKeyId=1144 or r.DataKeyId=39 or r.DataKeyId=116 or r.DataKeyId=115 or r.DataKeyId=117
              or r.DataKeyId=3506 or r.DataKeyId=3508 or r.DataKeyId=3507) 
            and (Time between DATEADD(dd, 0, DATEDIFF(dd, 0, GETDATE()-{})) and  DATEADD(dd, 0, DATEDIFF(dd, 0, GETDATE()-{}+1))) order by UtcTime asc'''.format(offset, offset))
    
    cursor.execute(E2)
    result = cursor.fetchall()
    

    name2 = "AGC_Export_2sec_" + timestr + ".csv"
    

    with open(name2,"w", newline='') as file:
        
        #csv.writer(file).writerow(x[0] for x in cursor.description)
        writer = csv.writer(file, delimiter=";")
        writer.writerows(result)

    sftp.put(name2, directory + name2)

    E3 = ('''SELECT o.DataKey, r.UtcTime, r.Value
	    FROM [Archive].[dbo].[DataKeyValue] as r
            JOIN DataKey o
	    ON o.DataKeyId = r.DataKeyId
            WHERE (r.DataKeyId=298 or r.DataKeyId=117 or r.DataKeyId=504 or r.DataKeyId=450 or r.DataKeyId=408
              or r.DataKeyId=407 or r.DataKeyId=462 or r.DataKeyId=461 or r.DataKeyId=516 or r.DataKeyId=515
              or r.DataKeyId=558 or r.DataKeyId=566 or r.DataKeyId=565 or r.DataKeyId=612 or r.DataKeyId=620
              or r.DataKeyId=619 or r.DataKeyId=666 or r.DataKeyId=674 or r.DataKeyId=673 or r.DataKeyId=716
              or r.DataKeyId=724 or r.DataKeyId=723 or r.DataKeyId=121 or r.DataKeyId=129 or r.DataKeyId=128
              or r.DataKeyId=396 or r.DataKeyId=199 or r.DataKeyId=207 or r.DataKeyId=206 or r.DataKeyId=250
              or r.DataKeyId=258 or r.DataKeyId=257 or r.DataKeyId=302 or r.DataKeyId=310 or r.DataKeyId=309
              or r.DataKeyId=400 or r.DataKeyId=454 or r.DataKeyId=508 or r.DataKeyId=662 or r.DataKeyId=608
              or r.DataKeyId=712 or r.DataKeyId=554 or r.DataKeyId=195 or r.DataKeyId=246) 
            and (Time between DATEADD(dd, 0, DATEDIFF(dd, 0, GETDATE()-{})) and  DATEADD(dd, 0, DATEDIFF(dd, 0, GETDATE()-{}+1))) order by UtcTime asc'''.format(offset, offset))
    
    cursor.execute(E3)
    result = cursor.fetchall()
    

    name3 = "AGC_Export_10sec_" + timestr + ".csv"
    

    with open(name3,"w", newline='') as file:
        
        #csv.writer(file).writerow(x[0] for x in cursor.description)
        writer = csv.writer(file, delimiter=";")
        writer.writerows(result)

    sftp.put(name3, directory + name3)
    
export()
