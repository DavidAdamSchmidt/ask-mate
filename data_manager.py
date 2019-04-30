import database_common


@database_common.connection_handler
def get_new_id(cursor, table):
    cursor.execute\
    (f"""
        SELECT MAX(id) FROM {table};   
    """)
    id = cursor.fetchall()
    return id


@database_common.connection_handler
def update_vote_number(cursor, table, op_change, id_):
    cursor.execute\
    (f"""
        UPDATE {table} 
        SET vote_number = vote_number {op_change}
        WHERE id={id_};
    """)


@database_common.connection_handler
def insert_new_record(cursor, table, values):
    cursor.execute\
    (f"""
        INSERT INTO {table}
        VALUES ({values});
    """)


@database_common.connection_handler
def update_record(cursor, values, id_):
    cursor.execute\
    (f"""
        UPDATE {table}
        SET {values}
        WHERE id={id_};
    """)


@database_common.connection_handler
def get_answer_by_id(cursor, id):
    cursor.execute(f"SELECT message, image, question_id FROM answer WHERE id={id}")
    answer = cursor.fetchall()
    return answer


@database_common.connection_handler
def get_answers_by_question_id(cursor, question_id):
    cursor.execute(f"SELECT * FROM answer WHERE question_id={question_id}")
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def update_answers(cursor, message, image_url, id):
    cursor.execute(
        f"""UPDATE answer SET message='{message}', image='{image_url}'
            WHERE id={id}""")


@database_common.connection_handler
def sort_by_any(cursor, table, column, order):
    order = 'ASC' if order is True else 'DESC'
    cursor.execute\
    (f"""
        SELECT * FROM {table}
        ORDER BY {column} {order};
    """)
    ordered_table = cursor.fetchall()
    return ordered_table


@database_common.connection_handler
def delete_by_id(cursor, table, id_):
    cursor.execute\
    (f"""
        DELETE FROM {table} WHERE id={id_};
    """)
