import data_manager
import csv


def read_csv(filename):
    with open(filename, "r", newline="") as datafile:
        reader = csv.DictReader(datafile)
        return [row for row in reader]