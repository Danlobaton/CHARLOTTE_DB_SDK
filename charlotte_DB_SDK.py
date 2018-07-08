import json
import requests
import warnings
from Matrix_def import *


class CHARLOTTTE_DB:

    def __init__(self, IP_ADDRESS_DB, DATABASE_TOKEN):
        self.IP_ADDRESS_DB = IP_ADDRESS_DB
        self.DATABASE_TOKEN = DATABASE_TOKEN

    def simple_object_add(self, table_name, key_field, key_value, field_1=None, value_1=None, field_2=None, value_2=None, field_3=None, value_3=None, field_4=None, value_4=None, field_5=None, value_5=None, field_6=None, value_6=None, field_7=None, value_7=None, field_8=None, value_8=None,field_9=None, value_9=None,field_10=None, value_10=None):
        params = locals()
        del params['self']
        del params['table_name']
        del params['key_value']
        del params['key_field']
        print params
        fin_json = {}
        for key,value in params.items():
            if params[key] is None:
                del params[key]
                continue
            fin_json[key] = value
        return self.add_new_keyed_object(table_name,key_field,key_value,fin_json)

    def add_json_batch(self, table_name, key_field, dict_of_json,keyed=True):
        # get amount of json objects in dict
        for key, value in dict_of_json.iteritems():
            if keyed:
                status = self.add_new_keyed_object(table_name, key_field, key, value)
            else:
                status = self.add_object_noKey(table_name, key_field, key, value)
            if 'SUCCESS' not in status:
                warnings.warn("Object with key_string " + key + " data: " + str(json) + " could was could not be added.\nServer Message: " + str(status))

    # In Docs
    def get_table_names(self):
        url = "http://" + self.IP_ADDRESS_DB + "/db/%2Aget_table_names%2A"
        querystring = {"token": self.DATABASE_TOKEN}
        response = requests.request("GET", url, params=querystring)
        try:
            if response.content == 200:
                names = eval(response.content)
                return names
            else:
                return response.content
        except (RuntimeError, TypeError, NameError, KeyError, ValueError, OSError, Exception):
            return response.content

    # In Docs
    def get_table_fields(self, table_name):
        url = "http://" + self.IP_ADDRESS_DB + "/db/%2Aget_fields%2A"

        querystring = {"token": self.DATABASE_TOKEN, "table_name": table_name}

        response = requests.request("GET", url, params=querystring)
        try:
            # Check if response went as planned
            if response.status_code != 200:
                return 'ERROR: Request did not success - Status ' + str(response.status_code)
            # Parse response content and turn it into a list
            fields = re.sub("[\[\]\"]", "", response.text)
            fields = fields.split(",")
        except (RuntimeError, TypeError, NameError, KeyError, ValueError, OSError, Exception):
            return str(response.content)
        return fields

    # In Docs
    def get_all_objects_json(self, table_name):
        url = "http://" + self.IP_ADDRESS_DB + "/db/%2Aget_partial_object_data%2A"
        fields = self.get_table_fields(table_name)
        querystring = {"token": self.DATABASE_TOKEN, "table_name": table_name, "field_name": fields[0],
                       "search_string": ""}

        response = requests.request("GET", url, params=querystring)
        # Check request status and proceed with data parsing if successful
        if response.status_code == 200:
            try:
                data = json.loads(response.content)
                for index in range(0, len(data)):
                    # list comprehension
                    data[index] = {key: value for item in data[index] for key, value in item.items()}
                return data
            # Returns API response if there're no object in DB or other API err message
            except (RuntimeError, TypeError, NameError, KeyError, ValueError, OSError, Exception):
                return response.content
        else:
            return 'ERROR: Request did not success - Status ' + str(response.status_code)

    # In Docs
    def create_table(self, table_name, array_of_fields):
        # Check for duplicates
        if len(array_of_fields) != len(set(array_of_fields)):
            raise Exception("Cannot have duplicate table fields")
        # Param check
        if len(array_of_fields) < 1:
            raise Exception('ERROR CANNOT HAVE EMPTY FIELDS')
        if table_name == "":
            return Exception('TABLE NAME CANNOT BE EMPTY STRING')
        # Parse request
        array_of_fields = '{"' + '","'.join(array_of_fields) + '"}'
        request = requests.get(
            'http://' + self.IP_ADDRESS_DB + '/db/*create_table*?token=' + self.DATABASE_TOKEN + '&table_name=' + table_name + '&array_of_fields=' + array_of_fields)
        # Check response
        try:
            if request.status_code != 200:
                return 'Request Unsuccessful: ' + str(request.status_code)
            else:
                return request.content
        except (RuntimeError, TypeError, NameError, KeyError, ValueError, OSError, Exception):
            return str(request.content)

    # In Docs
    def get_object(self, table_name, search_field, search_string):
        url = "http://" + self.IP_ADDRESS_DB + "/db/%2Aget_object_data%2A"

        querystring = {"token": self.DATABASE_TOKEN, "table_name": table_name, "field_name": search_field,
                       "search_string": search_string}

        response = requests.request("GET", url, params=querystring)
        # Check request status
        try:
            if response.status_code == 200:
                # If object exists parse and return it
                data = json.loads(response.content)
                for index in range(0, len(data)):
                    data = {key: value for item in data[index] for key, value in item.items()}
                return data
        except (RuntimeError, TypeError, NameError, KeyError, ValueError, OSError, Exception):
            return str(response.content)

    # In Docs
    def add_new_keyed_object(self, table_name, key_field, key_string, json_data):
        url = "http://" + self.IP_ADDRESS_DB + "/db/%2Aadd_new_object_uniqueKey_json%2A"
        # Check that user input for json is either json or a dict
        type_check = str(type(json_data))
        if not "str" in type_check:
            if "dict" in type_check:
                json_data = json.dumps(json_data)
            else:
                raise Exception("Expecting json or dict object but got " + type_check + " instead")

        querystring = {"token": self.DATABASE_TOKEN, "table_name": table_name, "key_field": key_field,
                       "key_string": key_string}

        payload = {'json_data': json_data}
        response = requests.post(url, data=payload, params=querystring)
        try:
            if response.status_code == 200:
                return str(response.content)
            else:
                return 'ERROR: Request did not success - Status ' + str(response.status_code)
        except (RuntimeError, TypeError, NameError, KeyError, ValueError, OSError, Exception):
            return str(response.content)

    # In Docs
    def delete_table(self, table_name):
        url = "http://" + self.IP_ADDRESS_DB + "/db/%2Adelete_table%2A"
        querystring = {"token": self.DATABASE_TOKEN, "table_name": table_name}

        if table_name == "" or table_name.isspace():
            raise Exception("Table name cannot be empty")

        response = requests.request("GET", url, params=querystring)
        try:
            # Check if request succeeded
            if response.status_code == 200:
                return str(response.content)
            else:
                return 'ERROR: Request did not success - Status ' + str(response.status_code)
        except (RuntimeError, TypeError, NameError, KeyError, ValueError, OSError, Exception):
            return str(response.content)

    # In Docs
    def delete_object(self, table_name, search_field, search_string):
        url = "http://" + self.IP_ADDRESS_DB + "/db/%2Adelete_object%2A"
        querystring = {"token": self.DATABASE_TOKEN, "table_name": table_name, "field_name": search_field,
                       "search_string": search_string}
        if search_string == "" or search_string.isspace():
            raise Exception("Cannot have empty search_string")

        response = requests.request("GET", url, params=querystring)
        # Check if request succeded
        try:
            if response.status_code == 200:
                return str(response.content)
            else:
                return 'ERROR: Request did not success - Status ' + str(response.status_code)
        except (RuntimeError, TypeError, NameError, KeyError, ValueError, OSError, Exception):
            return str(response.content)

    # In Docs
    def add_new_field(self, table_name, field_name):
        url = "http://" + self.IP_ADDRESS_DB + "/db/%2Aadd_new_field%2A"
        querystring = {"token": self.DATABASE_TOKEN, "table_name": table_name, "field_name": field_name}

        if field_name == "" or field_name.isspace():
            raise Exception("Cannot have empty field name")

        response = requests.request("GET", url, params=querystring)
        try:
            # Check if request succeeded
            if response.status_code == 200:
                return response.content
            else:
                return 'ERROR: Request did not success - Status ' + str(response.status_code)
        except (RuntimeError, TypeError, NameError, KeyError, ValueError, OSError, Exception):
            return str(response.content)

    # In Docs
    def rename_table(self, table_name, new_name):
        url = "http://" + self.IP_ADDRESS_DB + "/db/%2Arename_table%2A"
        querystring = {"token": self.DATABASE_TOKEN, "table_name": table_name, "new_table_name": new_name}

        if new_name == "" or new_name.isspace():
            raise Exception("New table name cannot be empty")

        response = requests.request("GET", url, params=querystring)
        # Check if request succeeded
        try:
            if response.status_code == 200:
                if "SUCCESS" in response.content:
                    # Format name change
                    return "SUCCESS " + table_name + " changed to " + new_name
                else:
                    return response.content
            else:
                return 'ERROR: Request did not success - Status ' + str(response.status_code)
        except (RuntimeError, TypeError, NameError, KeyError, ValueError, OSError, Exception):
            return str(response.content)

    # In Docs
    def update_field_name(self, table_name, field_name, new_name):
        url = "http://" + self.IP_ADDRESS_DB + "/db/%2Aupdate_fieldname%2A"
        querystring = {"token": self.DATABASE_TOKEN, "table_name": table_name, "field_name": field_name,
                       "new_field_name": new_name}

        if new_name == "" or new_name.isspace():
            raise Exception("New field name cannot be empty")

        response = requests.request("GET", url, params=querystring)
        try:
            if response.status_code == 200:
                if "SUCCESS" in response.content:
                    return "SUCCESS " + field_name + " changed to " + new_name
                else:
                    return response.content
            else:
                return 'ERROR: Request did not success - Status ' + str(response.status_code)
        except (RuntimeError, TypeError, NameError, KeyError, ValueError, OSError, Exception):
            return str(response.content)

    # In Docs
    def search_partial_matches(self, table_name, field_name, search_string):
        url = "http://" + self.IP_ADDRESS_DB + "/db/%2Aget_partial_object_data%2A"
        querystring = {"token": self.DATABASE_TOKEN, "table_name": table_name, "field_name": field_name,
                       "search_string": search_string}
        if field_name == "" or field_name.isspace():
            raise Exception("Cannot have empty field name")

        response = requests.request("GET", url, params=querystring)
        # Check if request succeeded
        try:
            if response.status_code == 200:
                return response.content
            else:
                return 'ERROR: Request did not success - Status ' + str(response.status_code)
        except (RuntimeError, TypeError, NameError, KeyError, ValueError, OSError, Exception):
            return str(response.content)

    # In Docs
    def reinit(self):
        url = "http://" + self.IP_ADDRESS_DB + "/db/%2Ainitialize%2A"
        querystring = {"token": self.DATABASE_TOKEN}
        response = requests.request("GET", url, params=querystring)
        return response.content

    # In Docs
    def update_object(self, table_name, key_field, key_string, json_data):
        url = "http://" + self.IP_ADDRESS_DB + "/db/%2Aupdate_DB_charlotte_json%2A"

        type_check = str(type(json_data))
        if not "str" in type_check:
            if "dict" in type_check:
                json_data = json.dumps(json_data)
            else:
                raise Exception("Expecting json or dict object but got [" + type_check + "] instead")

        querystring = {"token": self.DATABASE_TOKEN, "table_name": table_name, "field_name": key_field,
                       "search_string": key_string}

        payload = {'json_data': json_data}

        response = requests.post(url, data=payload, params=querystring)
        # Check if request succeeded
        try:
            if response.status_code == 200:
                return response.content
            else:
                return 'ERROR: Request did not success - Status ' + str(response.status_code)
        except (RuntimeError, TypeError, NameError, KeyError, ValueError, OSError, Exception):
            return str(response.content)

    # In Docs
    def add_object_noKey(self, table_name, key_field, key_string, json_data):
        url = "http://" + self.IP_ADDRESS_DB + "/db/%2Aadd_new_object_NOuniqueKey_json%2A"

        type_check = str(type(json_data))
        if not "str" in type_check:
            if "dict" in type_check:
                json_data = json.dumps(json_data)
            else:
                raise Exception("Expecting json or dict object but got [" + type_check + "] instead")

        querystring = {"token": self.DATABASE_TOKEN, "table_name": table_name, "key_field": key_field,
                       "key_string": key_string}

        payload = {'json_data': json_data}

        response = requests.post(url, data=payload, params=querystring)
        try:
            # Check if request succeeded
            if response.status_code == 200:
                return response.content
            else:
                return 'ERROR: Request did not success - Status ' + str(response.status_code)
        except (RuntimeError, TypeError, NameError, KeyError, ValueError, OSError, Exception):
            return str(response.content)

    # In Docs
    def add_matrix(self, table_name, key_field, key_string, matrix_field, matrix):
        url = "http://" + self.IP_ADDRESS_DB + "/db/%2Aadd_new_object_uniqueKey_json%2A"

        type_check = str(type(matrix))
        if "numpy.ndarray" in type_check:
            matrix = np_matrix_to_str(matrix)
        elif "list" in type_check:
            matrix = py_matrix_to_str(matrix)
        else:
            raise Exception(
                "Was expecting either a numpy matrix, list matrix, or a tensor but got " + type_check + " instead")

        querystring = {"token": self.DATABASE_TOKEN, "table_name": table_name, "key_field": key_field,
                       "key_string": key_string}

        json_data = json.dumps({matrix_field: matrix})
        payload = {"json_data": json_data}

        response = requests.post(url, data=payload, params=querystring)
        try:
            # Check if request succeeded
            if response.status_code == 200:
                return response.content
            else:
                return 'ERROR: Request did not success - Status ' + str(response.status_code)
        except (RuntimeError, TypeError, NameError, KeyError, ValueError, OSError, Exception):
            return str(response.content)

    # In Docs
    def add_tensor(self, table_name, key_field, key_string, tensor_field, tensor):
        url = "http://" + self.IP_ADDRESS_DB + "/db/%2Aadd_new_object_uniqueKey_json%2A"

        type_check = str(type(tensor))
        if "tensorflow" not in type_check:
            raise Exception("Was a expecting a tensor but got a " + type_check + " instead")

        querystring = {"token": self.DATABASE_TOKEN, "table_name": table_name, "key_field": key_field,
                       "key_string": key_string}

        tensor = tensor_to_str(tensor)
        json_data = json.dumps({tensor_field: tensor})
        payload = {"json_data": json_data}

        response = requests.post(url, data=payload, params=querystring)
        try:
            # Check if request succeeded
            if response.status_code == 200:
                return response.content
            else:
                return 'ERROR: Request did not success - Status ' + str(response.status_code)
        except (RuntimeError, TypeError, NameError, KeyError, ValueError, OSError, Exception):
            return str(response.content)

    # In Docs
    def get_matrix(self, table_name, search_field, search_string, matrix_field):
        url = "http://" + self.IP_ADDRESS_DB + "/db/%2Aget_object_data%2A"

        querystring = {"token": self.DATABASE_TOKEN, "table_name": table_name, "field_name": search_field,
                       "search_string": search_string}

        response = requests.request("GET", url, params=querystring)
        if response.status_code == 200:
            try:
                data = json.loads(response.content)
                data = data[0]
                data = {key: value for item in data for key, value in item.items()}
                matrix_str = data[matrix_field]
                if matrix_str[:6] == "PYTHON":
                    matrix_str = matrix_str.encode('ascii', 'ignore')
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
            except (RuntimeError, TypeError, NameError, ValueError, OSError, Exception):
                return response.content
        else:
            return 'ERROR: Request did not success - Status ' + str(response.status_code)

    # In Docs
    def get_tensor(self, table_name, search_field, search_string, tensor_field):
        url = "http://" + self.IP_ADDRESS_DB + "/db/%2Aget_object_data%2A"

        querystring = {"token": self.DATABASE_TOKEN, "table_name": table_name, "field_name": search_field,
                       "search_string": search_string}

        response = requests.request("GET", url, params=querystring)
        if response.status_code:
            try:
                data = json.loads(response.content)
                data = data[0]
                data = {key: value for item in data for key, value in item.items()}
                tensor_str = data[tensor_field]
                if "tensor" in tensor_str:
                    tensor = tensor_str.encode('ascii', 'ignore')
                    tensor = str_to_tensor(tensor)
                    return tensor
                else:
                    raise Exception("Called object is not a tensor")
            except KeyError:
                raise Exception("Tensor field DNE")
            except (RuntimeError, TypeError, NameError, ValueError, OSError, Exception):
                return response.content
        else:
            return 'ERROR: Request did not success - Status ' + str(response.status_code)

    # In Docs
    def get_object_count(self, table_name):
        data = self.get_all_objects_json(table_name)
        return len(data)

    # In Docs
    def get_status(self):
        url = "http://" + self.IP_ADDRESS_DB + "/db/%2Astatus%2A"
        querystring = {"token": self.DATABASE_TOKEN}

        response = requests.request("GET", url, params=querystring)
        try:
            # Check request status
            if response.status_code == 200:
                return response.content
            else:
                return 'ERROR: Request did not success - Status ' + str(response.status_code)
        except (RuntimeError, TypeError, NameError, ValueError, OSError, Exception):
            return response.content
