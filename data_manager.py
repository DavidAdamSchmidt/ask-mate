import connection
import database_common



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
    record["vote_number"] = vote_number + increase_by
    if answer:
        connection.update_to_csv("data/answer.csv", record, ANSWERS_HEADER)
    else:
        connection.update_to_csv("data/question.csv", record, QUESTIONS_HEADER)


def read_csv(filename):
    return connection.read_csv(filename)


def write_new_to_csv(filename, headers, fieldnames):
    connection.write_new_to_csv(filename, headers, fieldnames)


def update_to_csv(filename, updated_qna, headers):
    connection.update_to_csv(filename, updated_qna, headers)


def get_question_by_id(question_id):
    questions = connection.read_csv("data/question.csv")
    for question in questions:
        if question["id"] == str(question_id):
            return question


@database_common.connection_handler
def get_record_by_id(cursor, record_id, record_type):
    cursor.execute(f"SELECT * FROM {record_type} WHERE id={record_id}")
    record = cursor.fetchall()[0]
    return record


@database_common.connection_handler
def get_record_by_question_id(cursor, question_id, record_type):
    cursor.execute(f"SELECT * FROM {record_type} WHERE question_id={question_id}")
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def get_answer_by_id(cursor, id):
    cursor.execute(f"SELECT message, image, question_id FROM answer WHERE id={id}")
    answer = cursor.fetchall()[0]
    return answer


@database_common.connection_handler
def update_answer(cursor, message, image_url, id):
    cursor.execute(
        f"""UPDATE answer SET message='{message}', image='{image_url}'
            WHERE id={id}""")


def sort_by_any(filename, header_by, reverse_):
    table = connection.read_csv(filename)
    table.sort(key=lambda x: int(x[header_by]) if x[header_by].lstrip(
        "-").isdigit() else x[header_by], reverse=reverse_)
    return table


def delete_by_id(id_to_del, id_type, answer=False):
    filename = f"data/{'answer' if answer else 'question'}.csv"
    table = connection.read_csv(filename)
    table = [x for x in table if x[id_type] != id_to_del]
    for row in table:
        if int(row[id_type]) > int(id_to_del):
            row[id_type] = int(row[id_type]) - 1
    connection.write_data_(
        filename,
        table,
        ANSWERS_HEADER if answer else QUESTIONS_HEADER)
