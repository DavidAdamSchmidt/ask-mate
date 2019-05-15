import connection
from datetime import datetime
from psycopg2 import sql


BASIC_TAGS = ['Python', 'CSS', 'HTML', 'JavaScript', 'Java', 'C#', 'C++', 'C']


@connection.connection_handler
def get_max_id(cursor, table):
    cursor.execute(
        f"""SELECT MAX(id) FROM {table};""")
    id_ = cursor.fetchone()
    return id_


@connection.connection_handler
def update_vote_number(cursor, table, oper, id_):
    if oper not in "+-":
        raise ValueError(f"{oper} should be + or -.")
    cursor.execute((
        sql.SQL("UPDATE {} SET vote_number = vote_number "+oper+" 1 WHERE id=%(id_)s").
        format(sql.Identifier(table))), {"id_": id_})


@connection.connection_handler
def insert_new_record(cursor, table, record):
    record['submission_time'] = str(datetime.now())
    cursor.execute(f" to_date({})").format()
    keys = str(tuple(record.keys())).replace("'","")
    values = str(tuple(record.values())).replace("'","")
    print(keys)
    print(values)
    cursor.execute(sql.SQL("INSERT INTO {table} "+keys+" VALUES "+values+" ").
                   format(table=sql.Identifier(table)))


    if table == "question":
        command = f"""INSERT INTO question {str(tuple(record.keys())).replace("'","")} VALUES("""
    elif table == "answer":
        command = f"""INSERT INTO answer {str(tuple(record.keys())).replace("'","")} VALUES("""
    elif table == "comment":
        command = f"""INSERT INTO comment {str(tuple(record.keys())).replace("'","")} VALUES("""
    for data in record.values():
        if type(data) is str:
            data = data.replace("'", "''")
        command += (f"'{data}'" if type(data) is str else f"{data}") + ', '
    command = command[:-2] + ')'
    cursor.execute(command)


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
    cursor.execute("SELECT * FROM answer WHERE question_id=%(id_)s", {"id_": id_})
    records = cursor.fetchall()
    return records


@connection.connection_handler
def update_comment_by_primary_id(cursor, data, id):
    command = "UPDATE comment SET "
    for key, value in data.items():
        command += "%(key)s="
        command += ("%(value)s" if type(value) is str else "%(value)s") + ", "
    cursor.execute(command[:-2] + " WHERE id=%(id)s", {"key": key, "value": value, "data": data, "id": id})


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


#nem használt
@connection.connection_handler
def add_comment(cursor, message, edited_count, id, parent_type):
    current_datetime = datetime.now()
    parent_plus_id = parent_type + '_id'
    cursor.execute(
        """INSERT INTO comment
            (message, edited_count, submission_time, %(parent_plus_id)s)
            VALUES
            (%(message)s, %(edited_count)s, %(current_datetime)s, %(id)s);""", {"parent_plus_id": parent_plus_id, "current_datetime": current_datetime, "message": message, "edited_count": edited_count, "id": id})


@connection.connection_handler
def sort_by_any(cursor, column, order, limit=None):
    order = 'ASC' if order is True else 'DESC'
    if limit is None:
        cursor.execute(
            f"""SELECT * FROM question ORDER BY {column} {order};""")
    else:
        cursor.execute("SELECT COUNT(*) FROM question;")
        row_num = cursor.fetchone()['count']
        if row_num < limit:
            limit = row_num
        cursor.execute(
            f"""SELECT * FROM question ORDER BY {column} {order}
                OFFSET {row_num} - {limit} FETCH FIRST {limit} ROWS ONLY;""")
    ordered_table = cursor.fetchall()
    return ordered_table


@connection.connection_handler
def get_search_results_from_database(cursor, search_phrase):
    search_phrase = '%'+search_phrase+'%'
    cursor.execute('''
                   SELECT DISTINCT ON (title) title, question.message FROM question, answer
                   WHERE title LIKE %(search_phrase)s OR question.message LIKE %(search_phrase)s
                   OR answer.message LIKE %(search_phrase)s AND question.id=question_id;
                   ''', {"search_phrase": search_phrase})
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