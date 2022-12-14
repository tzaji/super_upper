import mysql.connector
import logging
import sys

#  logging setup variables
LOGGING_LEVEL = logging.ERROR
LOGGING_FORMAT = "%(asctime)s:%(levelname)s:%(lineno)d:%(message)s"
LOGGING_FILE_NAME = "../db_mysql.log"

#  sys standard output setup variables
SYS_STDOUT_FILE_NAME = "db_stdout.log"

#  MySQL connection setup variables
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"

#  default database name
DATABASE = "rami_levy"

"""if activate, the 3 rows below would print system standard output into chosen log file: SYS_STDOUT_FILE_NAME.
    note: if the below is activated you should activate the last 2 rows of this code as well."""
# restore_point = sys.stdout
# sys.stdout = open(SYS_STDOUT_FILE_NAME, "a")
# sys.stdout.reconfigure(encoding="utf-8")

logging.basicConfig(filename=LOGGING_FILE_NAME, level=LOGGING_LEVEL, format=LOGGING_FORMAT)


def execute_sql_commands(commands: list, hst=MYSQL_HOST, usr=MYSQL_USER, pswrd=MYSQL_PASSWORD):
    """
    this function receives sql commands (i.e. strings) and executes them one by one.
    """
    mydb = mysql.connector.connect(host=hst, user=usr, password=pswrd)
    total_commands = len(commands)
    with mydb.cursor() as cursor:
        for i in range(total_commands):
            try:
                cursor.execute(commands[i])
                logging.info(f"'{commands[i]}' (i.e. {i} out of {total_commands} commands) was successfully executed.")
            except Exception as e:
                logging.error(f"Error: '{commands[i]}' (i.e. {i} out of {total_commands} commands) was not "
                              f"executed due to the following:\n{e}.")


def sql_commands_to_create_database(db_tables: list, db=DATABASE):
    """
    this functions receives tables information (of a database) as a list of dictionaries in the following format:
            [{table_name: {attribute_name: INT PRIMARY KEY AUTOINCREMENT,
                           attribute_name: INT FOREIGN KEY REFERENCES <table_name> (<attribute_name>),
                           attribute_name: DATETIME NOT NULL,
                           attribute_name: FLOAT,
                           attribute_name: VARCHAR
                          }
              },
             ... ]

    it creates list of sql commands to initiate the given tables, and then call the 'execute_sql_commands' function to
    execute these sql commands.

    note: by default this function will send a 'CREATE DATABASE' command, however in case the database exists the
    'execute_sql_commands' would announce it in the logging file as an error but will continue executing the rest of
    the sql commands.
    """
    create_command = [f"CREATE DATABASE {db};"]
    use_command = [f"USE {db};"]
    execute_sql_commands(create_command)
    for element in db_tables:
        execute_sql_commands(use_command + [element])


def updating_db_tables(dict_list: list, db=DATABASE):
    """
    receive table dictionary from the following form:
        [{table_name: {attribute: value, attribute: value}}, ...]
    the function prepare sql command and then call the 'execute_sql_commands' function to execute these sql commands.
    """
    initialize_commands = [f"USE {db};"]
    for table_db in dict_list:
        for table_name, atr_dict in table_db.items():
            sql = f"INSERT INTO {table_name} ({', '.join(atr_dict.keys())}) VALUES ({', '.join(atr_dict.values())});"
            execute_sql_commands(initialize_commands + [sql])
            logging.info(f"updating_db_tables: {sql} command was successfully sent to be executed.")


# sys.stdout = restore_point
# print('sys.stdout was successfully restored to console')

# sections_table = """
#                  CREATE TABLE sections(
#                          id INT NOT NULL AUTO_INCREMENT,
#                          name VARCHAR(255),
#                          url VARCHAR(255),
#                          PRIMARY KEY(id)
#                  );
#                  """
#
# sub_sections_table = """
#                      CREATE TABLE sub_sections(
#                      id INT NOT NULL AUTO_INCREMENT,
#                      name VARCHAR(255),
#                      url VARCHAR(255),
#                      section_id INT,
#                      PRIMARY KEY(id),
#                      FOREIGN KEY (section_id) REFERENCES sections(id)
#                      );
#                      """
#
# products_table = """
#                  CREATE TABLE products(
#                          id INT NOT NULL AUTO_INCREMENT,
#                          item INT,
#                          barcode INT,
#                          name VARCHAR(255),
#                          sub_section_id INT,
#                          PRIMARY KEY(id),
#                          FOREIGN KEY (sub_section_id) REFERENCES sub_sections(id)
#                  );
#                  """
#
# price_records_table = """
#                       CREATE TABLE price_records(
#                       id INT NOT NULL AUTO_INCREMENT,
#                       product_id INT,
#                       price float,
#                       record_time int,
#                       PRIMARY KEY(id),
#                       FOREIGN KEY (product_id) REFERENCES products(id)
#                       );
#                       """
#
# nutritional_values_table = """
#                            CREATE TABLE nutritional_values(
#                            id INT NOT NULL AUTO_INCREMENT,
#                            product_id INT,
#                            item INT,
#                            barcode int,
#                            name VARCHAR(255),
#                            nutritional_facts INT,
#                            PRIMARY KEY(id),
#                            FOREIGN KEY (product_id) REFERENCES products(id)
#                            );
#                            """
#
# nutritional_facts_table = """
#                           CREATE TABLE nutritional_facts(
#                           id INT NOT NULL AUTO_INCREMENT,
#                           nutritional_facts_en VARCHAR(255),
#                           nutritional_facts_he VARCHAR(255),
#                           PRIMARY KEY(id)
#                           );
#                           """
#
#
#
# # tables_queries = [sections_table,
# #                   sub_sections_table,
# #                   products_table,
# #                   price_records_table,
# #                   nutritional_facts_table,
# #                   nutritional_values_table
# #                   ]
#
# foreign_keys_queries = [foreign_keys_alter_nutritional_values_table,
#                         foreign_keys_alter_nutritional_facts_table
#                         ]

# sql_commands_to_create_database(tables_queries)
