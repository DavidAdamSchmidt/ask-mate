import connection
from datetime import datetime
from psycopg2 import sql
import bcrypt


@connection.connection_handler
def get_max_id(cursor, table):
    cursor.execute(
        f"""SELECT MAX(id) FROM {table};""")
    id_ = cursor.fetchone()
    return id_


@connection.connection_handler
def update_vote_number(cursor, table, oper, id_):
    if oper not in "+1-1":
        raise ValueError(f"{oper} should be +1 or -1.")
    cursor.execute((
        sql.SQL("UPDATE {} SET vote_number = vote_number " + oper + " WHERE id=%(id_)s").
        format(sql.Identifier(table))), {"id_": id_})


@connection.connection_handler
def insert_new_record(cursor, table, record):
    record['submission_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    values = ""
    for value in record.values():
        if type(value) is str:
            value = value.replace("'", "''")
        values += (f"'{value}'" if type(value) is str else f"{value}") + ', '
    values = values[:-2] + ')'
    keys = str(tuple(record.keys())).replace("'","")
    cursor.execute(sql.SQL("INSERT INTO {table} " + keys + " VALUES (" + values).
                   format(table=sql.Identifier(table)))


@connection.connection_handler
def get_record_by_id(cursor, table, _id):
    cursor.execute(sql.SQL("SELECT * FROM {table} WHERE id=%(_id)s").
                   format(table=sql.Identifier(table)), {"_id": _id})
    record = cursor.fetchone()
    return record


@connection.connection_handler
def get_comment_by_parent_id(cursor, parent, id_):
    cursor.execute(sql.SQL("SELECT * FROM comment WHERE {parent} = %(id_)s").
                   format(parent=sql.Identifier(parent)), {"id_": id_})
    records = cursor.fetchall()
    return records


@connection.connection_handler
def get_answer_by_question_id(cursor, id_):
    cursor.execute("SELECT * FROM answer WHERE question_id=%(id_)s ORDER BY vote_number DESC", {"id_": id_})
    records = cursor.fetchall()
    return records


@connection.connection_handler
def update_comment_by_primary_id(cursor, data, id):
    count, msg = data['edited_count'], data['message']
    cursor.execute(
        """UPDATE comment SET edited_count= %(count)s, message= %(msg)s
            WHERE id=%(id)s""", {"count": count, "msg": msg, "id": id})


@connection.connection_handler
def update_answer(cursor, message, image_url, id):
    cursor.execute(
        """UPDATE answer SET message= %(message)s, image= %(image_url)s
            WHERE id=%(id)s""", {"message": message, "image_url": image_url, "id": id})


@connection.connection_handler
def update_question(cursor, title, message, image, id_):
    cursor.execute(
        """ UPDATE question SET title= %(title)s, message= %(message)s, image= %(image)s
            WHERE id=%(id_)s;""", {"title": title, "message": message, "image": image, "id_": id_})


@connection.connection_handler
def get_sorted_questions(cursor, column_to_order_by, asc=True, limit=None):
    order_direction = 'ASC' if asc is True else 'DESC'
    command = f"""SELECT question.id, submission_time, user_account.name
                  AS posted_by, view_number, vote_number, title, message, image
                  FROM question FULL JOIN user_account ON user_id = user_account.id
                  WHERE submission_time IS NOT NULL
                  ORDER BY {column_to_order_by} {order_direction}
                  """
    if limit:
        cursor.execute("SELECT COUNT(*) FROM question;")
        row_num = cursor.fetchone()['count']
        if row_num < limit:
            limit = row_num
        command += f" OFFSET {row_num} - {limit} FETCH FIRST {limit} ROWS ONLY"
    cursor.execute(command)
    ordered_table = cursor.fetchall()
    return ordered_table


@connection.connection_handler
def get_search_results_from_database(cursor, search_phrase):
    cursor.execute('''
                   SELECT DISTINCT ON (title) title, question.message FROM question
                   JOIN answer ON question.id = answer.question_id
                   WHERE title ILIKE %(search_phrase)s OR question.message
                   ILIKE %(search_phrase)s OR answer.message ILIKE %(search_phrase)s;
                   ''',
                   {'search_phrase': search_phrase})
    search_results = cursor.fetchall()
    return search_results


@connection.connection_handler
def delete_by_id(cursor, table, id_, parent_="id"):
    cursor.execute((sql.SQL("DELETE FROM {table} WHERE {parent_} = %(id_)s").
                    format(table=sql.Identifier(table), parent_=sql.Identifier(parent_))), {"id_": id_})


@connection.connection_handler
def get_answer_ids(cursor, question_id):
    cursor.execute("SELECT id FROM answer WHERE question_id=%(question_id)s", {"question_id": question_id})
    answer_ids = cursor.fetchall()
    return answer_ids


@connection.connection_handler
def get_tag_by_question_id(cursor, id_):
    cursor.execute("SELECT * FROM question_tag WHERE question_id=%(id_)s", {"id_": id_})
    records = cursor.fetchall()
    return records


@connection.connection_handler
def insert_new_tag(cursor, new_tag):
    new_tag_name = new_tag['name']
    cursor.execute(
        """ INSERT INTO tag (name) 
        VALUES (%(new_tag_name)s)""", {"new_tag_name": new_tag_name})
    new_tag_id = get_max_id('tag')['max']
    new_tag_question_id = new_tag['question_id']
    cursor.execute(
        """ INSERT INTO question_tag (question_id, tag_id) 
        VALUES (%(new_tag_question_id)s, %(new_tag_id)s)""", {"new_tag_question_id": new_tag_question_id, "new_tag_id": new_tag_id})


@connection.connection_handler
def delete_tags(cursor, question_id, tag):
    cursor.execute("""DELETE FROM question_tag WHERE question_id=%(question_id)s;
            DELETE FROM tag WHERE id=%(tag)s;""", {"question_id": question_id, "tag": tag})


@connection.connection_handler
def update_tag(cursor, tag):
    tag_name = tag['name']
    tag_id = tag['tag_id']
    cursor.execute(
        """ UPDATE tag SET name=%(tag_name)s 
        WHERE id=%(tag_id)s;""", {"tag_name": tag_name, "tag_id": tag_id})


@connection.connection_handler
def get_basic_tags(cursor):
    cursor.execute("SELECT * FROM tag WHERE id <= 9")
    basic_tags = cursor.fetchall()
    tag_s = []
    for tag in basic_tags:
        tag_s.append(tag['name'])
    return tag_s


@connection.connection_handler
def check_if_user_exists(cursor, name):
    cursor.execute("""
                   SELECT name FROM user_account
                   WHERE name LIKE %(name)s;
                   """,
                   {'name': name})
    user_exists = bool(cursor.fetchone())
    return user_exists


@connection.connection_handler
def register_user(cursor, name, password):
    user_exists = check_if_user_exists(name)
    if user_exists:
        pass
    else:
        hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        password_hash = hashed_bytes.decode('utf-8')
        registration_date = datetime.now()
        cursor.execute("""
                       INSERT INTO user_account (name, password_hash, role_id, registration_date) VALUES (
                       %(name)s, %(password_hash)s, 2, %(registration_date)s);
                       """,
                       {'name': name, 'password_hash': password_hash, 'registration_date': registration_date}
                       )