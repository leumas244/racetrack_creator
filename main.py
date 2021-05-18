from xml.dom import minidom
import xml.etree.ElementTree as ET
import csv
import numpy
import copy

mydoc = minidom.parse('streetPart.xml')
streckenTeil = mydoc.childNodes[0]
xmlBase = minidom.parse('strecke.x3d')

wpList = []
with open('converted_track.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        wpList.append(', '.join(row))

new_wp_list = []
idx = len(wpList) - 1
while (idx >= 0):
  new_wp_list.append(wpList[idx])
  idx = idx - 1

i = 0
for item in new_wp_list:
    temp = item.split(',')
    fields = []
    for a in temp:
        fields.append(float(a))

    currentItem = copy.deepcopy(streckenTeil)
    currentItem.attributes['DEF'] = ('Strecke ' + str(i))

    # breite und länge
    scale = str(fields[5] / 10) + ' 1 ' + str(fields[2] / 20)
    currentItem.attributes['scale'] = scale

    #arc tan y / x //arctan für radians für drehung der strecke
    rot = '0 1 0 -' + str(numpy.arctan2(fields[3], fields[4]))
    currentItem.attributes['rotation'] = rot

    #
    translation = str(fields[0]) + ' 0 ' + str(fields[1])
    currentItem.attributes['translation'] = translation
    i += 1

    # schreiben xml dokument
    xmlBase.childNodes[1].childNodes[3].appendChild(currentItem)
    print(streckenTeil.attributes['DEF'].value)


with open("output.x3d", "w") as xml_file:
    xmlBase.writexml(xml_file)


#print(streckenTeil[0].attributes['DEF'].value)