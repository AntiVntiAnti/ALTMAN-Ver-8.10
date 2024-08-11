import tracker_config as tkc
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import os
import shutil
from typing import List, Union
from logger_setup import logger

user_dir = os.path.expanduser('~')
db_path = os.path.join(os.getcwd(), tkc.DB_NAME)  # Database Name
target_db_path = os.path.join(user_dir, tkc.DB_NAME)  # Database Name


def initialize_database() -> None:
    """
    Initializes the database by creating a new database file or copying an existing one.

    If the target database file doesn't exist, it checks if the source database file exists.
    If the source database file exists, it copies it to the target location.
    If the source database file doesn't exist, it creates a new database file using the 'QSQLITE' driver.

    Returns:
        None

    Raises:
        Exception: If there is an error creating or copying the database file.
    """
    try:
        if not os.path.exists(target_db_path):
            if os.path.exists(db_path):
                shutil.copy(db_path, target_db_path)
            else:
                db: QSqlDatabase = QSqlDatabase.addDatabase('QSQLITE')
                db.setDatabaseName(target_db_path)
                if not db.open():
                    logger.error("Error: Unable to create database")
                db.close()
    except Exception as e:
        logger.error("Error: Unable to create database", str(e))


class DataManager:
    
    def __init__(self,
                 db_name: str = target_db_path) -> None:
        """
        Initializes the DataManager object and opens the database connection.

        Args:
            db_name (str): The path to the SQLite database file.

        Raises:
            Exception: If there is an error opening the database.

        """
        try:
            self.db: QSqlDatabase = QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(db_name)
            
            if not self.db.open():
                logger.error("Error: Unable to open database")
            logger.info("DB INITIALIZING")
            self.query: QSqlQuery = QSqlQuery()
            self.setup_tables()
        except Exception as e:
            logger.error(f"Error: Unable to open database {e}", exc_info=True)
    
    def setup_tables(self) -> None:
        """
        Sets up the necessary tables in the database.

        This method calls the setup_beck_table() and setup_altman_table() methods to create the required tables in the database.
        """
        self.setup_altman_table()
        
    def setup_altman_table(self) -> None:
        """
        Sets up the 'altman_refined_table' in the database if it doesn't already exist.

        This method creates a table named 'altman_refined_table' in the database with the following columns:
        - id: INTEGER (Primary Key, Autoincrement)
        - altman_date: TEXT
        - altman_time: TEXT
        - altman_question: INTEGER
        - altman_question_2: INTEGER
        - altman_question_3: INTEGER
        - altman_question_4: INTEGER
        - altman_question_5: INTEGER
        - altmans_summary: INTEGER

        If the table already exists, this method does nothing.

        Returns:
            None
        """
        if not self.query.exec(f"""
                        CREATE TABLE IF NOT EXISTS altman_refined_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        altman_date TEXT,
                        altman_time TEXT,
                        altman_question INTEGER,
                        altman_question_2 INTEGER,
                        altman_question_3 INTEGER,
                        altman_question_4 INTEGER,
                        altman_question_5 INTEGER,
                        altmans_summary INTEGER
                        )"""):
            logger.error(f"Error creating table: altman_refined_table",
                         self.query.lastError().text())
    
    def insert_into_altman_table(self,
                                 altman_date: str,
                                 altman_time: str,
                                 altman_question: int,
                                 altman_question_2: int,
                                 altman_question_3: int,
                                 altman_question_4: int,
                                 altman_question_5: int,
                                 altmans_summary: int
                                 ) -> None:
        """
        Inserts data into the altman_refined_table.

        Args:
            altman_date (str): The date of the mental_mental record.
            altman_time (str): The date of the mental_mental record.
            sleep (str): The time of the mental_mental record.
            speech (int): The value of the mood slider.
            activity (int): The value of the mania slider.
            cheer (int): The value of the depression slider.
            confidence (int): The value of the mixed risk slider.
            altmans_summary (int): the summary of all things and all things summary'd

        Returns:
            None

        Raises:
            ValueError: If the number of bind values does not match the number of placeholders in the SQL query.
            Exception: If there is an error during data insertion.

        """
        sql: str = f"""INSERT INTO altman_refined_table(
            altman_date,
            altman_time,
            altman_question,
            altman_question_2,
            altman_question_3,
            altman_question_4,
            altman_question_5,
            altmans_summary
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        bind_values: List[Union[str, int]] = [altman_date, altman_time, altman_question,
                                              altman_question_2, altman_question_3, altman_question_4,
                                              altman_question_5, altmans_summary]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"""Mismatch: altman_refined_table Expected {sql.count('?')}
                        bind values, got {len(bind_values)}.""")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: altman_refined_table - {self.query.lastError().text()}")
        except ValueError as e:
            logger.error(f"ValueError altman_refined_table: {e}")
        except Exception as e:
            logger.error(f"Error during data insertion: altman_refined_table {e}", exc_info=True)

def close_database(self) -> None:
    """
    Closes the database connection if it is open.

    This method checks if the database connection is open and closes it if it is.
    If the connection is already closed or an error occurs while closing the
    connection, an exception is logged.

    Raises:
        None

    Returns:
        None
    """
    try:
        logger.info("if database is open")
        if self.db.isOpen():
            logger.info("the database is closed successfully")
            self.db.close()
    except Exception as e:
        logger.exception(f"Error closing database: {e}")
