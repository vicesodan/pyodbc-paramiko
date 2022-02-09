import sys
import os
import fnmatch
import datetime
import xml.etree.ElementTree as ET
import glob
import shutil
import time
from datetime import datetime, date, timedelta
from xml.dom import minidom

# This function access the downloaded xml file
# and changes its data

def change(xml):
  with open(xml, "r") as handle:
  
    lines = handle.readlines()
    for i in lines:
      new_lines = i.split('>')
    lines = [x + '>' for x in new_lines][:-1]
    new_list = []
    for line in lines:
        if line.startswith('<Qty v="-'):
          new_list.append('<Qty v="' + line.split('-')[1])
        elif line.startswith('<Qty v="'):
          new_list.append('<Qty v="-' + line.split('"')[1] + '" />')
        else:
          new_list.append(line)


  f = open(xml, "w")
  for i in new_list:
    f.write(i)
      
    

def changeRR(xml):
  with open(xml, encoding="utf8") as f:
    tree = ET.parse(f)
    root = tree.getroot()
    
    for elem in root:
      for elem2 in elem:
        for elem3 in elem2:
          for subelem in elem3:
            try:
              subelem.attrib["v"] = subelem.attrib["v"].replace('-', '')
            except AttributeError:
              pass
    
  tree.write(xml, xml_declaration=True, method='xml', encoding="utf8")

def appendRR(xml):
  with open(xml, "r") as handle:
  
    lines = handle.readlines()
    for i in lines:
      new_lines = i.split('>')
    lines = [x + '>' for x in new_lines][:-1]
    cnt = 0
    new_list = []
    for line in lines:
        if line == '<ScheduleTimeSeries>':
            cnt += 1
        if cnt == 2:
            if line.startswith("<SendersTimeSeriesIdentification v="):
                new_list.append("""<SendersTimeSeriesIdentification v="6" />""")
            elif line.startswith("<MeteringPointIdentification"):
                new_list.append("""<MeteringPointIdentification v="RR-2DN-DEMAND--D" codingScheme=""/>""")
            elif line.startswith("<Qty v="):
                new_list.append('<Qty v="-' + line.split('"')[1] + '" />')
            else:
                new_list.append(line)
            if line == '</ScheduleTimeSeries>':
                break
    
    cnt2 = 0
    lines.pop()
    for line in lines:
        if line == '</ScheduleTimeSeries>':
            cnt2 += 1
    if cnt2 == 5:
      for el in new_list:
        lines.append(el)
    print(lines)

  f = open(xml, "w")
  for i in lines:
    f.write(i)
  f.write("</ScheduleMessage>")

# This function copies files from one folder to another
# and removes last extension


days_old = 1 # how old the files have to be before they are moved
hours_old = 1
move_date = date.today() - timedelta(hours=hours_old)
move_date = time.mktime(move_date.timetuple())


def copy(original_folder, new_folder, archive):  # folders to move files from and to
    for filename in glob.glob1(original_folder, "*.*"):
        newname = (os.path.splitext(filename)[0])
        srcfile = os.path.join(original_folder, filename)
        destfile = os.path.join(new_folder, newname)
        archfile = os.path.join(archive, newname)
        if os.stat(srcfile).st_mtime >= move_date:
            if not os.path.isfile(destfile) and not os.path.isfile(archfile):
                shutil.copyfile(srcfile, destfile)
                print('File is succesfuly copied!')
                if original_folder == "I:\scada\import\MMS_CAX":
                    localpath= 'I:\ProzaAGC\MMS_CAX/' + newname
                    change(localpath)
                if original_folder == "I:\scada\import\MMS_RR":
                    localpath= 'I:\ProzaAGC\MMS_RR/' + newname
                    changeRR(localpath)
                    appendRR(localpath)
            else:
                print('File already exists.')
        

copy("I:\scada\import\MMS_AGCS", "I:\ProzaAGC\MMS_AGCS", "I:\ProzaAGC\MMS_AGCS\archive")
copy("I:\scada\import\MMS_CAX", "I:\ProzaAGC\MMS_CAX", "I:\ProzaAGC\MMS_CAX\archive")
copy("I:\scada\import\MMS_RR", "I:\ProzaAGC\MMS_RR", "I:\ProzaAGC\MMS_RR\archive")
copy("I:\scada\import\MMS_ITS_CF", "I:\ProzaAGC\MMS_ITS_CF", "I:\ProzaAGC\MMS_ITS_CF\archive")
copy("I:\scada\import\MMS_CD_AGC", "I:\ProzaAGC\MMS_CD_AGC", "I:\ProzaAGC\MMS_CD_AGC\archive")





