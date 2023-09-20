import sqlite3 
from datetime import date

from ..expenses.run_expenses import create_expense, list_expenses
from ..settings import DATABASE_URL


class Args:
    pass

def test_create_expense():
    today = date.today().isoformat()
    args = Args()
    
    #the asignment must have the same order as the insertion
    args.value = 5000
    args.user = 'Carlos'
    args.category = 'food'
    args.description = 'I just bought rice buddy'
    args.div = 1
    args.date = '2023-09-20'
        
    with sqlite3.connect(DATABASE_URL) as con:
        cur = con.cursor()
        
        cur.execute("DROP TABLE IF EXISTS expenses;")
        con.commit()
        
        create_expense(args)
        
        check_if_table_exists_query = """SELECT name FROM sqlite_master WHERE type='table' AND name='expenses';"""
        cur.execute(check_if_table_exists_query)
        table_exists = cur.fetchone()
        assert table_exists is not None
        
        select_query = """SELECT * FROM expenses;"""    
        cur.execute(select_query)
        expense_register = cur.fetchone()
        
        today = date.today().isoformat()
        args.created = today
        args.updatd = today
        
        expected_result = (value for value in vars(args).values() )
        
        assert expense_register[1:] == tuple(expected_result)
        
        cur.execute("DROP TABLE expenses;")
        con.commit()
        cur.close()

if __name__ == '__main__':
    test_create_expense()