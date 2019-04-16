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



def read_csv(filename):
    return connection.read_csv(filename)


def write_new_to_csv(filename, headers, fieldnames):
    connection.write_new_to_csv(filename, headers, fieldnames)


def get_question_by_id(question_id):
    questions = connection.read_csv("data/question.csv")
    for question in questions:
        if question["id"] == question_id:
            return question


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
    keys_to_sort = sorted(keys_to_sort, reverse=reverse_)
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
