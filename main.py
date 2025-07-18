from datetime import datetime
from os import close, mkdir
from os.path import isfile, isdir
from typing import Any

import telebot

import JsonContext
from Database import Database
from ai import Assistant

# unused files
close(0)
close(1)
close(2)

if not isdir("context"):
    mkdir("context")

TOKEN=""

bot = telebot.TeleBot(TOKEN)

db = Database()

def insertData(name: str, table: int, persons: int, data: str) -> Exception | str:
    """Insert a new reserve, PLEASE ANALYSE THE DATABASE TO VERIFY IF THE TABLE IS COMPATIBLE WITH DATA (TIME).
        Args:
            name (str): The name of main person for reserve.
            table (int): The number of table to reserve (0-30).
            persons (int): Number of persons to reserve.
            data (str): The data of reserve in (year-month-day hour-minute-second).

        Returns (str): True success False or message Exception Error
    """

    try:
        db.insertData((name, table, persons, datetime.strptime(data, "%Y-%m-%d %H:%M:%S")))
        return "True"
    except Exception as e:
        return str(e)


def deleteData(id: int) -> Exception | str:
    """Delete a reserve, use Fetch to find the id of row to delete.
            Args:
                id (int): The id of reserve to remove.

            Returns (str): True success False or message Exception Error
        """
    try:
        db.deleteData(id)
        return "True"
    except Exception as e:
        return str(e)

def changeDate(id: int, data: str) -> Exception | str:
    """Change the date a reserve, use Fetch to find the id of row to change.
                Args:
                    id (int): The id of reserve to change.
                    data (str): The data of reserve in (year-month-day hour-minute-second).

                Returns (str): True success False or message Exception Error
            """
    try:
        db.changeDate(id, datetime.strptime(data, "%Y-%m-%d %H:%M:%S"))
        return "True"
    except Exception as e:
        return str(e)


def fetchRowUser(name: str, date: str) -> Exception | Any:
    """Fetch the reserve's.
                Args:
                    name (str): The name of reserve.
                    date (str): the data of reserve.

                Returns (str): SQL DATA or message Exception Error
            """
    try:
        return db.fetchRowUser(name, datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        return str(e)


def fetchRowTable(table: int, date: str) -> Exception | Any:
    """Fetch the reserve's.
                    Args:
                        table (int): The table of reserve.
                        date (str): the data of reserve.

                    Returns (str): SQL DATA or message Exception Error
                """
    try:
        return db.fetchRowUser(table, datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        return str(e)

def fetchAvalaibleTable(dateInit: str, dateEnd: str) -> Exception | Any:
    """Fetch the reserve's.
                    Args:
                        dateInit (str): The data of reserve - 3hour.
                        dateEnd (str): The data of reserve + 3hour.

                    Returns (str): SQL DATA or message Exception Error
                """
    try:
        return db.fetchAvalaibleTable(datetime.strptime(dateInit, "%Y-%m-%d %H:%M:%S"), datetime.strptime(dateEnd, "%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        return str(e)

maria = Assistant()
maria.addAllTool([insertData, deleteData, changeDate, fetchRowTable, fetchRowUser, fetchAvalaibleTable])

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    user_id = message.from_user.id
    user_input = message.text

    if not maria.user_exists(user_id):
        if isfile(f"context/{user_id}.json"):
            maria.putHistory(user_id, JsonContext.openHistory(user_id))
        else:
            JsonContext.createHistory(user_id)

    # 2. Envia o texto para o assistente
    assistant_response = maria.sendRequest(user_id, user_input)  # Isso deve retornar uma string

    # 3. Responde usando o objeto original da mensagem
    bot.reply_to(message, assistant_response)  # Envia diretamente a string

    JsonContext.putHistory(user_id, user_input, assistant_response)


bot.infinity_polling()