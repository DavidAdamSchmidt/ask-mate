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
def sort_by_any(cursor, table, column, order, limit=None):
    order = 'ASC' if order is True else 'DESC'
    if limit is None:
        cursor.execute(
            f"""SELECT * FROM {table} ORDER BY {column} {order}""")
    else:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        row_num = cursor.fetchall()[0]['count']
        if row_num < limit:
            limit = row_num
        cursor.execute(
            f"""SELECT * FROM {table} ORDER BY {column} {order}
                OFFSET {row_num - limit} FETCH FIRST {limit} ROWS ONLY;""")
    ordered_table = cursor.fetchall()
    return ordered_table


@database_common.connection_handler
def delete_by_id(cursor, table, id_):
    cursor.execute(
        f"""DELETE FROM {table} WHERE id={id_};""")
