from django.db import models
import sqlite3

# Create your models here.

class BotDB:

    def __init__(self, db_file):
        """Инициализация соединения с БД"""
        self.connect = sqlite3.connect(db_file)
        self.cursor = self.connect.cursor()

    