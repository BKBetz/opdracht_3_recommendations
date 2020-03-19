from connection import create_connection

database = create_connection()

cursor = database[0]
connection = database[1]


def get_column_names(table):
    columns = {}
    query = """SELECT column_name FROM information_schema.columns WHERE table_name = %s"""
    cursor.execute(query, (table, ))
    col_names = cursor.fetchall()

    for i in range(0, len(col_names)):
        column = ''.join(col_names[i])
        columns[column] = i

    return columns


def filter_recommendations(table, fields):
    columns = get_column_names(table)
    filtered_columns = {}
    for field in fields:
        if field in columns:
            for key, value in columns.items():
                if field == key:
                    filtered_columns[key] = value
        else:
            print("field", field, "not found check for typos")
            continue

    return filtered_columns


def check_if_best(table, item, recommendation_id, fields):
    r_id = ''.join(recommendation_id)
    same_count = 0
    best_recommended = {}
    query = """SELECT * FROM {} WHERE id = %s"""

    if item[0] != r_id:
        cursor.execute(query.format(table), (r_id, ))
        recommendation = cursor.fetchone()
        for value in fields.values():
            if item[value] == recommendation[value]:
                same_count += 1
            else:
                continue
        best_recommended[r_id] = same_count
        highest_count = max(best_recommended, key=best_recommended.get)

        for count in best_recommended:
            if count == highest_count:
                return True
            else:
                return False
    else:
        return False


def search_recommended(table, fields, row):

    columns = filter_recommendations(table, fields)
    recommended = []
    recommendations = ''

    recommended.append(row[0])
    for key, value in columns.items():
        checker = row[value]
        if checker != '' or checker is not None:
            query = """SELECT id FROM {} WHERE {} = %s LIMIT 5000"""
            cursor.execute(query.format(table, key), (checker, ))
            recommendations = cursor.fetchall()
        else:
            continue

    for i in recommendations:
        equal = check_if_best(table, row, i, columns)
        if equal is True and len(recommended) < 4:
            i = "".join(i)
            recommended.append(i)
        else:
            continue

    return recommended

