import connection
import database_common
from datetime import datetime


@database_common.connection_handler
def get_new_id(cursor, table):
    cursor.execute(
        f"""SELECT MAX(id) FROM {table};""")
    id = cursor.fetchall()
    return id


@database_common.connection_handler
def update_vote_number(cursor, table, op_change, id_):
    cursor.execute(
        f"""UPDATE {table} SET vote_number = vote_number {op_change}
        WHERE id={id_};""")


@database_common.connection_handler
def insert_new_record(cursor, table, values):
    cursor.execute(f"""INSERT INTO {table} VALUES ({values});""")


@database_common.connection_handler
def update_record(cursor, table, values, id_):
    cursor.execute(
        f"""UPDATE {table} SET {values} WHERE id={id_};""")


@database_common.connection_handler
def get_record_by_id(cursor, record_id, table):
    cursor.execute(f"SELECT * FROM {table} WHERE id={record_id}")
    record = cursor.fetchall()[0]
    return record


@database_common.connection_handler
def get_record_by_question_id(cursor, question_id, table):
    cursor.execute(f"SELECT * FROM {table} WHERE question_id={question_id}")
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


@database_common.connection_handler
def add_comment(cursor, message, edited_count, id, parent_type):
    cursor.execute(
        f"""INSERT INTO comment
            (message, edited_count, submission_time, {parent_type + '_id'})
            VALUES
            ('{message}', {edited_count}, '{datetime.now()}', {id})""")


@database_common.connection_handler
def sort_by_any(cursor, table, column, order):
    order = 'ASC' if order is True else 'DESC'
    cursor.execute(
        f"""SELECT * FROM {table} ORDER BY {column} {order};""")
    ordered_table = cursor.fetchall()
    return ordered_table


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


@database_common.connection_handler
def get_data_from_database(cursor, search_phrase):
    cursor.execute('''
                   SELECT DISTINCT ON (title) title, question.message FROM question, answer
                   WHERE title LIKE %(search_phrase)s OR question.message LIKE %(search_phrase)s
                   OR answer.message LIKE %(search_phrase)s AND question.id=question_id;
                   ''',
                   {'search_phrase': search_phrase})
    results = cursor.fetchall()

    return results


@database_common.connection_handler
def delete_by_id(cursor, table, id_):
    cursor.execute(
        f"""DELETE FROM {table} WHERE id={id_};""")
