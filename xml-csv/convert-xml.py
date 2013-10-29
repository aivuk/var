import csv
import sys
import xml.etree.ElementTree as etree

file_name = sys.argv[1]
csv_file_name = '.'.join(file_name.split('.')[:-1] + ["csv"])
root = etree.parse(file_name).getroot()

with open(csv_file_name, 'w') as file_:
    writer = csv.writer(file_, quotechar='|', delimiter=";")
    header = False
    hs = []

    for n in root:
        # GRAB NUM_MNHN
        mnhn = n.find('NUM_MNHN').text.encode('utf-8')

        # GRAB PRESENTATION
        presentation_node = n.find('ZAC.PRESENTATION')

        if presentation_node:
            presentation = presentation_node.find('PRESENTATION').text.encode('utf-8')
        else:
            presentation = ''

        # GRAB ORIGINE
        origine = []
        origine_node = n.find('ZAC.ORIGINE')

        if origine_node:
            for d in origine_node:
                origine += [d.text.encode('utf-8') if d.text else '']

        linha = [mnhn, presentation] + origine

        # Create the header
        if not header:
            hs.append('NUM_MNHN')
            hs.append('ZAC.PRESENTATION')
            for c in n.find('ZAC.ORIGINE'):
                hs.append(c.tag)
            writer.writerow(hs)
            header = True

        writer.writerow(linha)
