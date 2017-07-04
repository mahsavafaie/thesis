import xml.etree.ElementTree as ET
import csv
import glob
file_list=[]
for filename in glob.glob('D:/asset/data/tfarsdat/Word/*.WRD.xml'):
	file_list.append(filename[:-8])
def tocsv(filename):
	tree = ET.parse(filename+'.WRD.xml')
	root = tree.getroot()
	# open a file for writing
	Resident_data = open(filename+'.csv', 'w')
	# create the csv writer object
	csvwriter = csv.writer(Resident_data)
	resident_head = []
	count = 0
	for member in root.findall('Root'):
		#resident -> word
		resident = []
		#create the header
		if count == 0:
			grapheme = member.find('Description').tag
			resident_head.append(grapheme)
			Phonemic = member.find('Phonemic').tag
			resident_head.append(Phonemic)
			Phonetic = member.find('Phonetic').tag
			resident_head.append(Phonetic)
			tstart = member.find('Start').tag
			resident_head.append(tstart)
			tend= member.find('End').tag
			resident_head.append(tend)
			csvwriter.writerow(resident_head)
			count = count + 1
		#create the rows
		grapheme = member.find('Description').text
		resident.append(grapheme)
		Phonemic = member.find('Phonemic').text
		resident.append(Phonemic)
		Phonetic = member.find('Phonetic').text
		resident.append(Phonetic)
		#to get the time from the datapoint
		tstart = member.find('Start').text
		resident.append(int(tstart)/(11025*2))
		tend = member.find('End').text
		resident.append(int(tend)/(11025*2))
		csvwriter.writerow(resident)
	Resident_data.close()
for i in file_list:
	tocsv(i)