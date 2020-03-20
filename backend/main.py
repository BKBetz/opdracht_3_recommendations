from connection import create_connection
# this is the overall file used for both recommendation types
database = create_connection()

cursor = database[0]
connection = database[1]


def get_column_names(table):
    # get the field names for a table so that u can filter using names instead of numbers
    columns = {}
    query = """SELECT column_name FROM information_schema.columns WHERE table_name = %s"""
    cursor.execute(query, (table, ))
    col_names = cursor.fetchall()

    for i in range(0, len(col_names)):
        # fields are still a tuple so we turn them into a string
        column = ''.join(col_names[i])
        # add the fields to a dict with a numeric value
        columns[column] = i

    return columns


def filter_recommendations(table, fields):
    # this function is used to get specific field from all the fields in a table
    columns = get_column_names(table)
    filtered_columns = {}
    for field in fields:
        # check if entered field is in the list of all fields
        if field in columns:
            for key, value in columns.items():
                if field == key:
                    # add field to new dictionary
                    filtered_columns[key] = value
        else:
            print("field", field, "not found check for typos")
            continue

    return filtered_columns


def check_if_best(table, item, recommendation_id, fields):
    # from all the fields you want to filter..check how many are equal to the item
    # example: u want to filter on category and subcategory, some products may have the same category
    # but not the same subcategory...these aren't better recommendations than the recommendations that have the same
    # category and subcategory...these are better recommendations so we only want those

    # turn recommendation_id into a str
    r_id = ''.join(recommendation_id)
    # count to check how many values are equal
    same_count = 0
    best_recommended = {}
    query = """SELECT * FROM {} WHERE id = %s"""

    # u want to compare the item_id to other item id's not the same
    if item[0] != r_id:
        # fetch all data from the recommended item
        cursor.execute(query.format(table), (r_id, ))
        recommendation = cursor.fetchone()
        for value in fields.values():
            # if a field is the same add to count
            if item[value] == recommendation[value]:
                same_count += 1
            else:
                continue
        # create a dict that has the id and the same count
        best_recommended[r_id] = same_count
        highest_count = max(best_recommended, key=best_recommended.get)

        for count in best_recommended:
            # if the count is equal to the highest possible count it can be. it is the best possible recommendations
            if count == highest_count:
                return True
            else:
                return False
    else:
        return False


def search_recommended(table, fields, row):
    # this function is big and in my opinion pretty complicated so I made an example

    # This function uses the other functions to make a list of equal items in the table u entered
    # what is equal and what is not is based on what fields u entered

    # example: u entered the parameters products and an array of brand and category (row is auto filled in another file)
    # the filter_recommendations checks if your fields are actually possible and if it's possible..it only returns those fields
    # next it checks for each field u entered where in the table that field has the same value as the item u want to check
    # so lets say there are 100 products with the same brand,
    # 50 with the same category and 40 with both
    # it puts all those id's in the recommendations array
    # then we use the check if best function to get all the id's that have both fields equal (so in this example 40 id's)
    # these are the 40 best recommendations and based on what u wanted they are all equally good.
    # then it just picks the first 3 and puts these in the recommended list

    columns = filter_recommendations(table, fields)
    recommended = []
    recommendations = ''

    # append the item id that u want recommendations for first
    recommended.append(row[0])
    for key, value in columns.items():
        checker = row[value]
        if checker != '' or checker is not None:
            # for each field use this query
            query = """SELECT id FROM {} WHERE {} = %s LIMIT 5000"""
            cursor.execute(query.format(table, key), (checker, ))
            # put all possible recommendations in this
            recommendations = cursor.fetchall()
        else:
            continue
    for i in recommendations:
        # for each recommendation check if is equal to the best possibility
        equal = check_if_best(table, row, i, columns)
        if equal is True and len(recommended) < 4:
            # id is still a tuple so turn it into a string
            i = "".join(i)
            recommended.append(i)
        else:
            continue

    return recommended

