import sqlite3
from datetime import date

from ..validations import validate_date
from ..settings import DATABASE_URL


def list_expenses(args):
   with sqlite3.connect(DATABASE_URL) as conn:
      cur = conn.cursor()
      list_expenses_query = """SELECT * FROM expenses"""
      
      try:
         cur.execute(list_expenses_query)
         results = cur.fetchall()

         for row in results:
            print(row)
      except sqlite3.OperationalError as e:
         print(f'the following error has ocurred: {e}')
      finally:
         cur.close()
         

def create_expense(args):
   validate_date(args.date)
   today = date.today().isoformat()
   is_divided = 1 if args.div else 0
   
   with sqlite3.connect(DATABASE_URL) as con:
       cur = con.cursor()
       
       create_expenses_table_query = """
       CREATE TABLE if not exists expenses(
          id INTEGER PRIMARY KEY AUTOINCREMENT, 
          value INTEGER NOT NULL,
          user TEXT NOT NULL,
          category TEXT NOT NULL,
          description TEXT, 
          is_divided INTEGER NOT NULL, 
          date TEXT,
          created TEXT,
          updated TEXT
          )
       """
       
       insert_into_expenses_query = f"""
       INSERT INTO expenses(
          value, 
          user,
          category,
          description, 
          is_divided, 
          date, 
          created,
          updated) VALUES(
             {args.value}, 
             '{args.user}',
             '{args.category}',
             '{args.description}', 
             {is_divided}, 
             '{args.date}',
             '{today}',
             '{today}'
             )"""
       
       cur.execute(create_expenses_table_query)
       cur.execute(insert_into_expenses_query) 
       con.commit()
       cur.close()
       
       print('The expense was registered successfully...')