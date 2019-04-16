import connection


ANSWERS_HEADER = [
    "id",
    "submission_time",
    "vote_number",
    "question_id",
    "message",
    "image"
]


QUESTIONS_HEADER = [
    "id",
    "submission_time",
    "view_number",
    "vote_number",
    "title",
    "message",
    "image"
]


def update_vote_number(id_, increase_by, answer=False):
    record = get_record_by_id(id_, answer=answer)
    vote_number = int(record["vote_number"])
    if vote_number > 0 or increase_by > 0:
        record["vote_number"] = vote_number + increase_by
    if answer:
        connection.update_to_csv("data/answer.csv", record, ANSWERS_HEADER)
    else:
        connection.update_to_csv("data/question.csv", record, QUESTIONS_HEADER)


def read_csv(filename):
    return connection.read_csv(filename)


def write_new_to_csv(filename, headers, fieldnames):
    connection.write_new_to_csv(filename, headers, fieldnames)


def get_record_by_id(id_, answer=False):
    filename = f"data/{'answer' if answer else 'question'}.csv"
    records = connection.read_csv(filename)
    for record in records:
        if record["id"] == id_:
            return record


def get_answers_by_question_id(question_id):
    answers = connection.read_csv("data/answer.csv")
    return [x for x in answers if x["question_id"] == question_id]


def sort_by_any(filename, header_by, reverse_):
    table = connection.read_csv(filename)
    keys_to_sort, new_table = [], []
    for row in table:
        keys_to_sort.append(row[header_by])
        temp_dict = {key: value for (key, value) in row.items()}
        new_table.append(temp_dict)
    keys_to_sort = sorted(keys_to_sort, key=lambda item: int(item) if item.isdigit() else item, reverse=reverse_)
    sorted_table = []
    for key in keys_to_sort:
        for qna in new_table:
            if qna[header_by] == key:
                sorted_table.append(qna)
    return sorted_table


def delete_by_id(filename, id_to_del, id_type, headers):
    table = connection.read_csv(filename)
    table = [x for x in table if x[id_type] != id_to_del]
    for row in table:
        if int(row[id_type]) > int(id_to_del):
            row[id_type] = int(row[id_type])-1
    connection.write_data_(filename, table, headers)
