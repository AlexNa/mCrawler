import os
import csv


class news:
    title_seletor = []
    content_seletor = []

    def __init__(self):
        if os.path.exists(str(os.path.dirname(os.path.abspath(__file__)) + "/title_selector.txt")):
            with open(str(os.path.dirname(os.path.abspath(__file__)) + "/title_selector.txt"), newline='') as csvfile:
                csvreader = csv.reader(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in csvreader:
                    if row and len(row) > 0:
                        self.title_seletor.append(row[0].strip())

        if os.path.exists(str(os.path.dirname(os.path.abspath(__file__)) + "/content_selector.txt")):
            with open(str(os.path.dirname(os.path.abspath(__file__)) + "/content_selector.txt"), newline='') as csvfile:
                csvreader = csv.reader(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in csvreader:
                    if row and len(row) > 0:
                        self.content_seletor.append(row[0].strip())
