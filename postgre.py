import psycopg2
import pandas as pd
import re


def getUId(condition):
    req = (f"SELECT u_id "
           f"FROM main "
           f"WHERE {condition}")
    cursor.execute(req)
    record = cursor.fetchall()
    return record


def getIdByValue(tableName, field, searchField, searchValue):
    if(searchValue == "NULL"):
        return 0
    req = (f"SELECT {field} "
           f"FROM {tableName} "
           f"WHERE {searchField} = {searchValue}")
    cursor.execute(req)
    record = cursor.fetchone()
    if(record):
        return record[0]
    return None


def select(tableName, field, where=False, condition=""):
    req = (f"SELECT {field} "
           f"FROM {tableName} "
           f"INNER JOIN name ON {tableName}.name=name.n_id "
           f"INNER JOIN family ON {tableName}.family=family.f_id "
           f"INNER JOIN patronymic ON {tableName}.patronymic=patronymic.p_id "
           f"INNER JOIN street ON {tableName}.street=street.s_id ")
    if(where):
        req += f"WHERE {condition}"
    print(req)
    cursor.execute(req)
    record = cursor.fetchall()
    #
    df = pd.DataFrame(record)
    return df.to_json(orient="records")


def insert(tableName, values):
    if(tableName == "main"):
        values = values.split(", ")
        familyVal = values[0]
        nameVal = values[1]
        patronymicVal = values[2]
        streetVal = values[-1]

        familyId = getIdByValue("family", "f_id", "f_val", familyVal)
        if not(familyId):
            insert("family", "default, " + familyVal)
            familyId = getIdByValue("family", "f_id", "f_val", familyVal)

        nameId = getIdByValue("name", "n_id", "n_val", nameVal)
        if not(nameId):
            insert("name", "default, " + nameVal)
            nameId = getIdByValue("name", "n_id", "n_val", nameVal)

        patronymicId = getIdByValue("patronymic", "p_id", "p_val", patronymicVal)
        if not(patronymicId):
            insert("patronymic", "default, " + patronymicVal)
            patronymicId = getIdByValue("patronymic", "p_id", "p_val", patronymicVal)

        streetId = getIdByValue("street", "s_id", "s_val", streetVal)
        if not(streetId):
            insert("street", "default, " + streetVal)
            streetId = getIdByValue("street", "s_id", "s_val", streetVal)

        values[0] = familyId
        values[1] = nameId
        values[2] = patronymicId
        values[-1] = streetId
        values = "default, " + re.sub(r"\[|\]|'", "", str(values))
        print(values)
    req = f"INSERT INTO {tableName} VALUES ({values})"
    try:
        cursor.execute(req)
        connection.commit()
    except Exception as error:
        print(error)


def delete(tableName, values):
    print(values)
    if(re.findall(r"(?<=f_val=)\S*", values)):
        familyId = getIdByValue("family", "f_id", "f_val", re.findall(r"(?<=f_val=)\S*", values)[0])
        values = re.sub(r"(?<=f_val=)\S*", str(familyId), values)

    if(re.findall(r"(?<=n_val=)\S*", values)):
        nameId = getIdByValue("name", "n_id", "n_val", re.findall(r"(?<=n_val=)\S*", values)[0])
        values = re.sub(r"(?<=n_val=)\S*", str(nameId), values)

    if(re.findall(r"(?<=p_val=)\S*", values)):
        patronymicId = getIdByValue("patronymic", "p_id", "p_val", re.findall(r"(?<=p_val=)\S*", values)[0])
        values = re.sub(r"(?<=p_val=)\S*", str(patronymicId), values)

    if(re.findall(r"(?<=s_val=)\S*", values)):
        streetId = getIdByValue("street", "s_id", "s_val", re.findall(r"(?<=s_val=)\S*", values)[0])
        values = re.sub(r"(?<=s_val=)\S*", str(streetId), values)

    values = values.replace("f_val", "family")
    values = values.replace("n_val", "name")
    values = values.replace("p_val", "patronymic")
    values = values.replace("s_val", "street")
    uIds = getUId(values)
    print(len(uIds))
    if(len((uIds)) == 0):
        return {"code": 404}
    elif(len(uIds) > 1):
        return {"code": 400}
    else:
        print(uIds[0][0])
        cursor.execute(f"DELETE FROM main WHERE u_id = {uIds[0][0]};")
        connection.commit()
        return {"code": 200}


def update(tableName, fieldName, newValue, oldValue):
    res = select(cursor, "main", "*", True, "f_val", newValue)
    if(res.empty):
        insert(connection, cursor, "family", f"(default, {newValue})")

    newId = getIdByValue(cursor, "family", "f_id", "f_val", newValue)
    oldId = getIdByValue(cursor, "family", "f_id", "f_val", oldValue)
    req = f"UPDATE {tableName} SET {fieldName}={newId} WHERE {fieldName} = {oldId};"
    cursor.execute(req)
    connection.commit()


connection = psycopg2.connect(user="postgres",
                              password="farbod",
                              host="127.0.0.1",
                              port="5432",
                              database="phone_book")
cursor = connection.cursor()

print(getIdByValue("patronymic", "p_id", "p_val", "NULL"))
