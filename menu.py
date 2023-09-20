"""
A menu - you need to add the database and fill in the functions. 
"""
import sqlite3

db = 'lab5_record_holder_db.db'

# Table creation if it doesn't exists
# Context manager for ease of automatically saving after statement execution


def create_table():
    with sqlite3.connect(db) as conn:

        conn.execute('DROP TABLE IF EXISTS chainsaws_juggling_record_holders')
        conn.execute(
            'CREATE TABLE IF NOT EXISTS chainsaws_juggling_record_holders (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name text UNIQUE, Country text, Number_of_catches int )')

    conn.close()


# Helper methods

# Rec. Holder Name
def users_record_holder_name():
    name = input('Name of Record Holder: ')
    return name

# Rec. Holder country


def users_record_holder_country():
    country = input('Record Holder\'s Country: ')
    return country

# Rec. Holder catches


def users_record_holder_catches():
    catches = int(input('Number of catches: '))
    return catches


def main():
    menu_text = """
    1. Display all records
    2. Search by name
    3. Add new record
    4. Edit existing record
    5. Delete record 
    6. Quit
    """
    # Call creating table after menu is displayed
    create_table()

    while True:
        print(menu_text)
        choice = input('Enter your choice: ')
        if choice == '1':
            display_all_records()
        elif choice == '2':
            search_by_name()
        elif choice == '3':
            add_new_record()
        elif choice == '4':
            edit_existing_record()
        elif choice == '5':
            delete_record()
        elif choice == '6':
            break
        else:
            print('Not a valid selection, please try again')


def display_all_records():
    # Display data from database
    # Connect to db to extract data
    conn = sqlite3.connect(db)

    # Selecting all rows from the record table
    record_results = conn.execute(
        'SELECT * FROM chainsaws_juggling_record_holders')

    # Message to let users know all the record holders here
    # Added break print statements for spacing before and after the lists
    print('Here are all the record holders: ')
    print()
    for row in record_results:
        print(row)

    print()

    conn.close()


def search_by_name():
    conn = sqlite3.connect(db)

    # Ask users who to look up
    user_name_search_req = users_record_holder_name()

    # parametrized query for users name search
    # Added wildcard search name containing users input name string
    results = conn.execute(
        'SELECT * FROM chainsaws_juggling_record_holders WHERE name like ?', ('%' + user_name_search_req + '%',))

    # store the name row in a variable
    record_holder_row = results.fetchone()

    # If the name is found, fetch it and display to users
    if record_holder_row:
        print('Here is your requested record holder: ')
        print(record_holder_row)

    # else, print a not found message if record holder not found
    else:
        print('Record holder not found in database')

    conn.close()


def add_new_record():

    # Users add record holder
    record_holder_name = users_record_holder_name()
    record_holder_country = users_record_holder_country()
    record_holder_catches = users_record_holder_catches()

# Try - catch for error handling
    try:
        # context manager to save the data to db
        with sqlite3.connect(db) as conn:
            conn.execute('INSERT INTO chainsaws_juggling_record_holders (name,Country,Number_of_catches) VALUES (?,?,?)',
                         (record_holder_name, record_holder_country, record_holder_catches))
        print('Record Holder added')

        conn.close()

    except Exception as e:
        print('Error adding record holder: ', e)


def edit_existing_record():
    # Getting record holder current id and getting new record catches from users
    record_holder_id = int(input('Please enter record holder id: '))
    new_record_catches = int(input('Number of Catches: '))

    try:
        with sqlite3.connect(db) as conn:

            # Updating record holder catches by searching and matching with the record holder's id
            conn.execute('UPDATE chainsaws_juggling_record_holders SET Number_of_catches = ? WHERE id = ?',
                         (new_record_catches, record_holder_id))

        print('Update successful')
        conn.close()

    except Exception as e:
        print('Error editing record holder: ', e)


def delete_record():

    # Search by name
    record_holder_name = users_record_holder_name()

    try:
        with sqlite3.connect(db) as conn:

            conn.execute(
                'DELETE FROM chainsaws_juggling_record_holders WHERE name = ?', (record_holder_name,))

            print('Delete successful')

        conn.close()

    except Exception as e:
        print('Error Deleting Record holder:', e)


if __name__ == '__main__':
    main()
