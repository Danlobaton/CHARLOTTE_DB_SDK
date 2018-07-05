# Charlotte DB SDK

### Setup
Go to the charlotte_DB_SDK_config.py and entern the IP address of the DB and the access token. The SDK won't workout without this step

### Functions

#### Getting data from DB

1. CHARLOTTE_DB_get_table_names()
   * params: None
   * return: A list of strings with all table names
2. CHARLOTTE_DB_get_table_fields(table_name)
   * params: table_name <string>
   * return: A list of strings with table fields
3. CHARLOTTE_DB_get_all_objects_json(table_name)
   * params: table_name <string>
   * returns: A list of python dicts. Each dict represents an object currently in the DB
4. CHARLOTTE_DB_get_object(table_name,search_field,search_string)
   * params: 
             - table_name <string>
             - search_field <string> : Table field to be searched in the DB
             - search_string <string> : String to be searched for in the specified field of the table
   * return: JSON in form of a <dict>
 5. 
  
### Writing Data to DB
 1. CHARLOTTE_DB_add_new_keyed_object(table_name, key_field, key_string, json_data)
     * params:
               - table_name <string>
               - key_field <string> : Field in the table to be used as a search field for the object later
               - key_string <string> : key string to be used in the key field
               - json_data <dict> : JSON containing the object data
      * return: `SUCCESS` if operation was successful else it returns an error message
      * example:  ```
                  table_name = "demo_table"
                  key_field = "field_1"
                  key_string = "mykey"
                  # Note that the key_field is not added in json_data
                  # Key_field and key_string will automatically become part of the object data
                  json_data = { "field_2" : "data", "field_3" : "data" }
                  CHARLOTTE_DB_add_new_keyed_object(table_name, key_field, key_string, json_data)
                  # returns "SUCCESS"
                  ```
### General DB management

 1. CHARLOTTE_DB_create_table(table_name, array_of_fields)
    * params:
              - table_name <string>
              - array_of_fields <list of strings> : Specifies the fields of the table
    * return: `SUCCESS` if operation was successful else it returns an error message 

