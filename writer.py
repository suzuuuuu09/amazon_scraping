import csv
import os

class CSV:
    def __init__(self, filename):
        self.filename = filename
        self.file_exists = os.path.isfile(filename)

    def write_data(self, header, data):
        file_exists = os.path.isfile(self.filename)
        with open(self.filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists or os.stat(self.filename).st_size == 0:
                writer.writerow(header)
            writer.writerow(data)