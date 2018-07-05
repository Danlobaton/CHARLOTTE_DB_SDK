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
