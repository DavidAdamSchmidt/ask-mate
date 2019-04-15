import csv


# id_type refers to the key of the id which you want to refer to
def get_latest_id(filename, id_type):
    new_id = 0
    with open(filename, 'r+', newline='') as datafile:
        datafile.seek(0)
        reader = csv.DictReader(datafile)
        for row in reader:
            new_id = row[id_type]
        new_id = int(new_id)+1
    return new_id


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


def update_to_csv(filename, updated_qna, headers):
    reader = read_csv(filename)
    for qna in reader:
        if "question_id" in headers:
            if int(qna["question_id"]) == int(updated_qna["question_id"]) and int(qna["id"]) == int(updated_qna["id"]):
                for keys, values in qna.items():
                    qna[keys] = updated_qna[keys]
        else:
            if int(qna["id"]) == int(updated_qna["id"]):
                for keys, values in qna.items():
                    qna[keys] = updated_qna[keys]
    with open(filename, "w", newline="") as datafile:
        data = csv.DictWriter(datafile, fieldnames=headers, extrasaction='raise')
        data.writeheader()
        for qna in reader:
            data.writerow(qna)


def write_new_to_csv(filename, headers, new_qna):
    with open(filename, 'a', newline='') as datafile:
        data = csv.DictWriter(datafile, fieldnames=headers, extrasaction='raise')
        data.writerow(new_qna)
