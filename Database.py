from sqlite3 import connect

class Database:

    database = None
    cursor = None

    def __init__(self):
        self.database = connect("reservas.db", check_same_thread=False)
        self.cursor = self.database.cursor()

    def insertData(self, row):
        self.cursor.execute("INSERT INTO reservas(nome_cliente, mesa, quantidade_pessoas, data) VALUES (?,?,?,?)", row)
        self.database.commit()

    def deleteData(self, id):
        self.cursor.execute("DELETE FROM reservas where id = ?", (id, ))
        self.database.commit()

    def changeDate(self, id, date):
        self.cursor.execute("UPDATE reservas set data = ? WHERE id = ?", (date, id))
        self.database.commit()

    def fetchRowUser(self, name, date):
        return self.cursor.execute("SELECT * FROM reservas WHERE nome_cliente = ? AND data = ?", (name, date)).fetchone()

    def fetchRowTable(self, table, date):
        return self.cursor.execute("SELECT * FROM reservas WHERE mesa = ? AND data = ?", (table, date)).fetchone()

    def fetchAvalaibleTable(self, dateInit, dateEnd):
        return 31-self.cursor.execute("SELECT COUNT(mesa) from reservas WHERE data BETWEEN ? AND ?", (dateInit, dateEnd)).fetchone()[0]