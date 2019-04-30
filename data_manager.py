import connection
from datetime import datetime


@connection.connection_handler
def get_max_id(cursor, table):
    cursor.execute(
        f"""SELECT MAX(id) FROM {table};""")
    id = cursor.fetchall()
    return id[0]


@connection.connection_handler
def update_vote_number(cursor, table, op_change, id_):
    cursor.execute(
        f"""UPDATE {table} SET vote_number = vote_number {op_change}
        WHERE id={id_};""")


@connection.connection_handler
def insert_new_record(cursor, table, record):
    record['submission_time'] = str(datetime.now())
    cursor.execute(
        f"""INSERT INTO {table} 
            {str(tuple(record.keys())).replace("'","")}
            VALUES {tuple(record.values())};""")


@connection.connection_handler
def get_record_by_id(cursor, record_id, table):
    cursor.execute(f"SELECT * FROM {table} WHERE id={record_id}")
    record = cursor.fetchall()[0]
    return record


@connection.connection_handler
def get_record_by_question_id(cursor, question_id, table):
    cursor.execute(f"SELECT * FROM {table} WHERE question_id={question_id}")
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def get_answer_by_id(cursor, id):
    cursor.execute(f"SELECT message, image, question_id FROM answer WHERE id={id}")
    answer = cursor.fetchall()[0]
    return answer


@connection.connection_handler
def update_answer(cursor, message, image_url, id):
    cursor.execute(
        f"""UPDATE answer SET message='{message}', image='{image_url}'
            WHERE id={id}""")


@connection.connection_handler
def update_question(cursor, title, message, image, id_):
    cursor.execute(
        f""" UPDATE question SET title='{title}', message='{message}', image='{image}'
            WHERE id={id_};""")


@connection.connection_handler
def add_comment(cursor, message, edited_count, id, parent_type):
    cursor.execute(
        f"""INSERT INTO comment
            (message, edited_count, submission_time, {parent_type + '_id'})
            VALUES
            ('{message}', {edited_count}, '{datetime.now()}', {id})""")


@connection.connection_handler
def sort_by_any(cursor, table, column, order):
    order = 'ASC' if order is True else 'DESC'
    cursor.execute(
        f"""SELECT * FROM {table} ORDER BY {column} {order};""")
    ordered_table = cursor.fetchall()
    return ordered_table


@connection.connection_handler
def delete_by_id(cursor, table, id_):
    cursor.execute(
        f"""DELETE FROM {table} WHERE id={id_};""")
