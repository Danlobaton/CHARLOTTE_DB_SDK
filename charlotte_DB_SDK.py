import urllib
import urllib2
import sys
import os
import requests
import re
from time import sleep
from charlotte_DB_SDK_config import *
import json


def CHARLOTTE_DB_get_table_names():

    url = "http://"+IP_ADDRESS_DB+"/db/%2Aget_table_names%2A"

    querystring = { "token" : DATABASE_TOKEN }

    response = requests.request("GET", url, params=querystring)

    return response.text

#Returns a list
def CHARLOTTE_DB_get_table_fields(table_name):

    url = "http://"+IP_ADDRESS_DB+"/db/%2Aget_fields%2A"

    querystring = { "token" : DATABASE_TOKEN , "table_name":table_name}

    response =  requests.request("GET",url,params=querystring)

    fields = re.sub("[\[\]\"]", "", response.text)
    fields = fields.split(",")

    return fields

def CHARLOTTE_DB_get_all_objects_json(table_name):

    url = "http://"+IP_ADDRESS_DB+"/db/%2Aget_partial_object_data%2A"
    fields = CHARLOTTE_DB_get_table_fields(table_name)
    querystring = {"token" : DATABASE_TOKEN,"table_name" : table_name,"field_name": fields[0],"search_string" : ""}

    response = requests.request("GET", url, params=querystring)
    try:
        return json.loads(response.content)
    except ValueError:
        return response.content

def CHARLOTTE_DB_create_table(table_name,array_of_fields):
    #Check for duplicates
    if len(array_of_fields) != len(set(array_of_fields)):
        raise Exception("Cannot have duplicate table fields")
    # Param check
    if len(array_of_fields) < 1:
        raise Exception('ERROR CANNOT HAVE EMPTY FIELDS')
    if table_name == "":
        return Exception('TABLE NAME CANNOT BE EMPTY STRING')
    # Parse request
    array_of_fields = '{"' + '","'.join(array_of_fields) + '"}'
    request = requests.get('http://' + IP_ADDRESS_DB + '/db/*create_table*?token=' + DATABASE_TOKEN + '&table_name=' + table_name + '&array_of_fields=' + array_of_fields)
    # Check response
    if request.status_code != 200:
        return 'Request Unsuccessful: ' + str(request.status_code)
    else:
        return request.content

def CHARLOTTE_DB_get_object(table_name,search_field,search_string):

    url = "http://"+IP_ADDRESS_DB+"/db/%2Aget_object_data%2A"

    querystring = {"token": DATABASE_TOKEN, "table_name" : table_name, "field_name" : search_field, "search_string" : search_string}

    response = requests.request("GET", url, params=querystring)

    try:
        datathis = json.loads(response.content)
        return datathis

    except ValueError:
        return response.content

def CHARLOTTE_DB_add_new_keyed_object(table_name,key_field,key_string,json_data):

    url = "http://"+IP_ADDRESS_DB+"/db/%2Aadd_new_object_uniqueKey_json%2A"

    type_check = str(type(json_data))
    if not "str" in type_check:
        if "dict" in type_check:
            json_data = json.dumps(json_data)
        else:
            raise Exception("Expecting json or dict object but got " + type_check + " instead")

    querystring = { "token" : DATABASE_TOKEN, "table_name" : table_name, "key_field" : key_field,
                   "key_string" : key_string }

    payload = {'json_data' : json_data}
    response = requests.post(url, data = payload, params = querystring)

    return response.content

def CHARLOTTE_DB_delete_table(table_name):
    url = "http://" + IP_ADDRESS_DB + "/db/%2Adelete_table%2A"
    querystring = {"token": DATABASE_TOKEN, "table_name": table_name}

    if table_name == "" or table_name.isspace():
        raise Exception("Table name cannot be empty")

    response = requests.request("GET", url, params=querystring)

    return response.content

def CHARLOTTE_DB_delete_object(table_name,search_field,search_string):
    url = "http://" + IP_ADDRESS_DB + "/db/%2Adelete_object%2A"
    querystring = {"token": DATABASE_TOKEN, "table_name": table_name, "field_name": search_field,
                   "search_string": search_string}
    if search_string == "" or search_string.isspace():
        raise Exception("Cannot have empty search_string")

    response = requests.request("GET", url, params=querystring)

    return response.content

def CHARLOTTE_DB_add_new_field(table_name,field_name):
    url = "http://" + IP_ADDRESS_DB + "/db/%2Aadd_new_field%2A"
    querystring = {"token": DATABASE_TOKEN, "table_name": table_name, "field_name": field_name}

    if field_name == "" or field_name.isspace():
        raise Exception("Cannot have empty field name")

    response = requests.request("GET", url, params=querystring)

    return response.content

def CHARLOTTE_DB_rename_table(table_name, new_name):
    url = "http://" + IP_ADDRESS_DB + "/db/%2Arename_table%2A"
    querystring = { "token" : DATABASE_TOKEN, "table_name" : table_name, "new_table_name": new_name }

    if new_name == "" or new_name.isspace():
        raise Exception("New table name cannot be empty")

    response =  requests.request("GET",url, params=querystring)

    if "SUCCESS" in response.content:
        return "SUCCESS " + table_name + " changed to " + new_name
    else:
        return requests.content

def CHARLOTTE_DB_update_field_name(table_name, field_name, new_name):
    url = "http://" + IP_ADDRESS_DB + "/db/%2Aupdate_fieldname%2A"
    querystring = {"token": DATABASE_TOKEN, "table_name": table_name, "field_name": field_name,
                   "new_field_name" : new_name}

    if new_name == "" or new_name.isspace():
        raise Exception("New field name cannot be empty")

    response = requests.request("GET", url, params=querystring)

    if "SUCCESS" in response.content:
        return "SUCCESS " + field_name + " changed to " + new_name
    else:
        return requests.content

def CHARLOTTE_DB_search_partial_matches(table_name, field_name, search_string):
    url = "http://" + IP_ADDRESS_DB + "/db/%2Aget_partial_object_data%2A"
    querystring = {"token" : DATABASE_TOKEN, "table_name" : table_name, "field_name": field_name,
                   "search_string": search_string}
    if field_name == "" or field_name.isspace():
        raise Exception("Cannot have empty field name")

    response = requests.request("GET", url, params=querystring)

    return response.content

def CHARLOTTE_DB_reinit():
    url = "http://" + IP_ADDRESS_DB + "/db/%2Ainitialize%2A"
    querystring = {"token": DATABASE_TOKEN}

    response = requests.request("GET", url, params=querystring)

    return response.content

def CHARLOTTE_DB_get_status():
    url = "http://" + IP_ADDRESS_DB + "/db/%2Astatus%2A"
    querystring = {"token": DATABASE_TOKEN }

    response =  requests.request("GET", url, params=querystring)

    return response.content

def CHARLOTTE_DB_update_object(table_name,key_field,key_string,json_data):
    url = "http://" + IP_ADDRESS_DB + "/db/%2Aupdate_DB_charlotte_json%2A"

    type_check = str(type(json_data))
    if not "str" in type_check:
        if "dict" in type_check:
            json_data = json.dumps(json_data)
        else:
            raise Exception("Expecting json or dict object but got [" + type_check + "] instead")

    querystring = {"token": DATABASE_TOKEN, "table_name": table_name, "field_name": key_field,
                   "search_string": key_string}

    payload = {'json_data': json_data}

    response = requests.post(url, data=payload, params=querystring)

    return response.content

def CHARLOTTE_DB_add_object_noKey(table_name,key_field,key_string,json_data):
    url = "http://" + IP_ADDRESS_DB + "/db/%2Aadd_new_object_NOuniqueKey_json%2A"

    type_check = str(type(json_data))
    if not "str" in type_check:
        if "dict" in type_check:
            json_data = json.dumps(json_data)
        else:
            raise Exception("Expecting json or dict object but got [" + type_check + "] instead")

    querystring = {"token": DATABASE_TOKEN, "table_name": table_name, "key_field": key_field,
                   "key_string": key_string}

    payload = {'json_data': json_data}

    response = requests.post(url, data=payload, params=querystring)

    return response.content

if IP_ADDRESS_DB == 'XXX PLEASE SETUP' or DATABASE_TOKEN == 'XXX PLEASE SETUP':
    print 'Please setup IP address of DB and Database Token in file charlotte_DB_SDK_config.py'
    sleep(100)
    sys.exit


if __name__ == '__main__':
    table = "dev_table"
    data = {"red":"DANYHERE",'white': "Giza", "rose": "Como animales"}
    #print CHARLOTTE_DB_update_object(table,key_field = "red", key_string = "TWOS",json_data = json.dumps(data))
    print CHARLOTTE_DB_update_object(table,"red","TWOS",json.dumps(data))
'''





if '*get_object_data*' in command_string:
    DB_table_name = request.args.get('table_name', '')
    field_name = request.args.get('field_name', '')
    search_string = request.args.get('search_string', '')
    print DB_table_name
    print field_name
    return str(get_object_data(DB_table_name,field_name, search_string))

if '*get_fields*' in command_string:

    table_name = request.args.get('table_name', '')
    print table_name
    return str(get_fields(table_name))

if '*get_partial_object_data*' in command_string:
    DB_table_name = request.args.get('table_name', '')
    field_name = request.args.get('field_name', '')
    search_string = request.args.get('search_string', '')
    print DB_table_name
    print field_name
    return str(get_partial_object_data(DB_table_name,field_name, search_string))

if '*delete_object*' in command_string:
    print 'here in delete object'
    DB_table_name = request.args.get('table_name', '')
    field_name = request.args.get('field_name', '')
    search_string = request.args.get('search_string', '')
    print DB_table_name
    print field_name
    result = delete_object(DB_table_name,field_name, search_string)
    slack_db('XXX saving for testing in production need take these out ')
    save_all_DB()
    return 'number objects deleted: '+ str(result)

if '*update_DB_charlotte_json*' in command_string:
    print 'here in update_DB_charlotte_json '
    DB_table_name = request.args.get('table_name', '')
    search_field = request.args.get('field_name', '')
    search_string = request.args.get('search_string', '')
    charlotte_structure_raw = request.args.get('json_data', '')
    print DB_table_name
    print search_field
    charlotte_structure = str(charlotte_structure_raw)
    result = update_DB_charlotte_struct_json(DB_table_name, search_field, search_string ,charlotte_structure)
    slack_db('XXX saving for testing in production need take these out ')
    save_all_DB()
    return 'updating DB: '+ str(result)

if '*create_table*' in command_string:
    print 'here in create_table'
    DB_table_name = request.args.get('table_name', '')
    array_of_fields_raw = request.args.get('array_of_fields', '')
    array_of_fields = parse_1_array(array_of_fields_raw)

    print array_of_fields

    if len(array_of_fields) < 1:
        return 'ERROR FIELDS'

    if 'ERROR parsing data fdv799' in str(array_of_fields):
        return 'ERROR parsing data fdv799'

    print 'raw data: ' + str(array_of_fields_raw)
    print 'new array of fields: ' + str(array_of_fields)

    result = create_table(DB_table_name, array_of_fields)
    return result


if '*add_new_object_NOuniqueKey_json*' in command_string:
    print 'here in add_new_object_uniqueKey_json '
    DB_table_name = request.args.get('table_name', '')
    charlotte_structure_raw = request.args.get('json_data', '')
    charlotte_structure = str(charlotte_structure_raw)
    result = add_new_object_to_table_NOuniqueKey_struct_json(DB_table_name,charlotte_structure)  #this can process a json string and update

    slack_db('XXX saving for testing in production need take these out ')
    save_all_DB()
    return result

if '*delete_table*' in command_string:
    print 'here in delete_table '
    DB_table_name = request.args.get('table_name', '')
    result = delete_table(DB_table_name)  #this can process a json string and update
    slack_db('XXX saving for testing in production need take these out ')
    save_all_DB()
    return result
'''