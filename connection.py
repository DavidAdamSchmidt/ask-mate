import data_manager
import csv


def read_csv(filename):
    with open(filename, "r", newline="") as datafile:
        reader = csv.DictReader(datafile)
        return [row for row in reader]


def write_to_csv(filename, headers, fieldnames):
    with open(filename, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # if len(fieldnames) == 6:
        #         writer.writerow({fieldnames[0] : headers[0], fieldnames[1] : headers[1],
        #         fieldnames[2] : headers[2], fieldnames[3] : headers[3],
        #         fieldnames[4] : headers[4], fieldnames[5] : headers[5]})
        # elif len(fieldnames) == 7:
        writer.writerow({fieldnames[0] : headers[0], fieldnames[1] : headers[1],
        fieldnames[2] : headers[2], fieldnames[3] : headers[3],
        fieldnames[4] : headers[4], fieldnames[5] : headers[5], fieldnames[6] : headers[6]})
        return 'Thanks for adding a question'