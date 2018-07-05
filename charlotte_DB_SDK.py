import json
import requests
import tensorflow as tf
from charlotte_DB_SDK_config import *
from Matrix_def import *

def CHARLOTTE_DB_get_table_names():

    url = "http://"+IP_ADDRESS_DB+"/db/%2Aget_table_names%2A"

    querystring = { "token" : DATABASE_TOKEN }

    response = requests.request("GET", url, params=querystring)
    names = eval(response.content)
    return names
#Returns a list of dicts
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
        data = json.loads(response.content)
        for index in range(0, len(data)):
            data[index] = { key: value for item in data[index] for key, value in item.items() }
        return data
    except ValueError:
        return response.content

def CHARLOTTE_DB_create_table(table_name, array_of_fields):
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
        data = json.loads(response.content)
        for index in range(0,len(data)):
            data = { key : value for item in data[index] for key, value in item.items() }
        return data
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

def CHARLOTTE_DB_add_matrix(table_name, key_field, key_string, matrix_field, matrix):

    url = "http://"+IP_ADDRESS_DB+"/db/%2Aadd_new_object_uniqueKey_json%2A"

    type_check = str(type(matrix))
    if "numpy.ndarray" in type_check:
        matrix = np_matrix_to_str(matrix)
    elif "list" in type_check:
        matrix = py_matrix_to_str(matrix)
    else:
        raise Exception("Was expecting either a numpy matrix, list matrix, or a tensor but got " + type_check + " instead")

    querystring = { "token" : DATABASE_TOKEN, "table_name" : table_name, "key_field" : key_field,
                   "key_string" : key_string }

    json_data = json.dumps({matrix_field: matrix})
    payload = {"json_data": json_data}

    response = requests.post(url, data = payload, params = querystring)

    return response.content

def CHARLOTTE_DB_get_matrix(table_name,search_field,search_string,matrix_field):

    url = "http://"+IP_ADDRESS_DB+"/db/%2Aget_object_data%2A"

    querystring = {"token": DATABASE_TOKEN, "table_name" : table_name, "field_name" : search_field, "search_string" : search_string}

    response = requests.request("GET", url, params=querystring)

    try:
        data = json.loads(response.content)
        try:
            data = data[0]
            data = { key : value for item in data for key, value in item.items() }
            matrix_str = data[matrix_field]
            if matrix_str[:6] == "PYTHON":
                matrix_str =  matrix_str.encode('ascii','ignore')
                data = str_to_py_matrix(matrix_str)
                return data
            elif matrix_str[:5] == "NUMPY":
                matrix_str = matrix_str.encode('ascii', 'ignore')
                data = str_to_np_matrix(matrix_str)
                return data
            else:
                raise Exception("Called object is not a matrix")
        except KeyError:
            raise Exception("Matrix field DNE")

    except ValueError:
        return response.content

def CHARLOTTE_DB_add_tensor( table_name, key_field, key_string, tensor_field, tensor):
    url = "http://" + IP_ADDRESS_DB + "/db/%2Aadd_new_object_uniqueKey_json%2A"

    type_check = str(type(tensor))
    if "tensorflow" not in type_check:
        raise Exception("Was a expecting a tensor but got a " + type_check + " instead")

    querystring = {"token": DATABASE_TOKEN, "table_name": table_name, "key_field": key_field,
                   "key_string": key_string }

    tensor = tensor_to_str(tensor)
    json_data = json.dumps({tensor_field : tensor})
    payload = {"json_data": json_data}

    response = requests.post(url, data=payload, params=querystring)

    return response.content

def CHARLOTTE_DB_get_tensor( table_name, search_field, search_string, tensor_field):
    url = "http://" + IP_ADDRESS_DB + "/db/%2Aget_object_data%2A"

    querystring = {"token": DATABASE_TOKEN, "table_name": table_name, "field_name": search_field,
                   "search_string": search_string}

    response = requests.request("GET", url, params=querystring)

    try:
        data = json.loads(response.content)
        try:
            data = data[0]
            data = { key : value for item in data for key, value in item.items() }
            tensor_str = data[tensor_field]
            if "tensor" in tensor_str:
                tensor = tensor_str.encode('ascii', 'ignore')
                tensor = str_to_tensor(tensor)
                return tensor
            else:
                raise Exception("Called object is not a tensor")
        except KeyError:
            raise Exception("Tensor field DNE")

    except ValueError:
        return response.content

def CHARLOTTE_DB_get_object_count(table_name):
    data = CHARLOTTE_DB_get_all_objects_json(table_name)
    return len(data)

if __name__ == '__main__':
    table = "dev_table"
    print CHARLOTTE_DB_get_object(table,"red","some_tensor")

'''    
    #SDK Testing v1.0.0
    
    print '\n------- Input Tensor --------\n'
    sess = tf.Session()
    b = tf.constant(np.arange(13.25, 20.5, dtype=np.float32), shape=[3, 3, 2])
    print(sess.run(b))

    print('\n--------------------- Tensor from DB ---------------------\n')
    tensor = CHARLOTTE_DB_get_tensor(table,"red","some_tensor","white")
    print(sess.run(tensor))
    
    
    print('\n--------------------- Matrix from DB ---------------------\n')
    print 'Getting list based matrix: \n'
    print CHARLOTTE_DB_get_matrix(table, "red", "one", "white")
    print '\nGetting numpy based matrix: \n'
    print CHARLOTTE_DB_get_matrix(table, "red", "two", "white")
    print('\n------- Checking converter functionality --------\n')
    print str_to_np_matrix(check)

    #SDK Testing v1.0.0
    
    print 'Begin testing....'

    print '-------------------\nCreating table...'
    print CHARLOTTE_DB_create_table(table,["red","white","rose"])

    print '-------------------\nGetting all tables in DB...'
    print CHARLOTTE_DB_get_table_names()

    print '-------------------\nGetting DB status...'
    print CHARLOTTE_DB_get_status()

    print '-------------------\nAdding unique key object...'
    data = {"white" : "Jamon","rose" : "Champagne"}
    print CHARLOTTE_DB_add_new_keyed_object(table, "red", "Ferrari", json.dumps(data))

    print '-------------------\nAdding NO unique key object...'
    data = {"white" : "Lambo", "rose" : "Huracan"}
    print CHARLOTTE_DB_add_object_noKey(table, "red", "Green", json.dumps(data))

    print '-------------------\nRetriving all objects from table...'
    print CHARLOTTE_DB_get_all_objects_json(table)

    print '-------------------\nUpdating object in table...'
    data = {"red" : "Quantum", "white" : "Dope", "rose" : " Supreme " }
    print CHARLOTTE_DB_update_object(table,"red","Ferrari",json.dumps(data))

    print '-------------------\nGetting single object data from updated object...'
    print CHARLOTTE_DB_get_object(table,"white","Dope")

    print '-------------------\nAdding field to table...'
    print CHARLOTTE_DB_add_new_field(table,"Gray")

    print '-------------------\nGetting table fields...'
    print CHARLOTTE_DB_get_table_fields(table)

    print '-------------------\nDeleting object from DB...'
    print CHARLOTTE_DB_delete_object(table, "white", "Dope")

    print '-------------------\nRetriving all objects from table...'
    print CHARLOTTE_DB_get_all_objects_json(table)

    print '-------------------\nDeleting table...'
    print CHARLOTTE_DB_delete_table(table)

    print '\nThat\'s it (: (: (: '
'''