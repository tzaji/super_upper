import mysql.connector
import logging
import sys

#  logging setup variables
LOGGING_LEVEL = logging.ERROR
LOGGING_FORMAT = "%(asctime)s:%(levelname)s:%(lineno)d:%(message)s"
LOGGING_FILE_NAME = "db_mysql.log"

#  sys standard output setup variables
SYS_STDOUT_FILE_NAME = "db_stdout.log"

#  MySQL connection setup variables
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123"

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
    initialize_commands = [f"CREATE DATABASE {db};", f"USE {db};"]
    for element in db_tables:
        for table_name, attribute_dict in element.items:
            temp = [f"CREATE TABLE {table_name} ("]
            for atr, atr_type in attribute_dict.items():
                temp.append(f"{atr} {atr_type}, ")
            temp.append(");")
            sql = "".join(temp)
            execute_sql_commands(initialize_commands + [sql])


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
