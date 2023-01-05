import sqlite3 as sq



async def db_start():
    global db, cur

    db = sq.connect('new.db')
    cur = db.cursor()
    if db:
        print('Data base  connected ok!')
    db.execute('CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, first_name TEXT, number TEXT, description TEXT, name TEXT)')
    db.commit()

async def create_profile(user_id):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?, ?, ?, ?, ?)", (user_id, '', '', '', ''))
        db.commit()




async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE profile SET first_name = '{}', number = '{}', description = '{}', name = '{}' WHERE user_id == '{}'".format(
            data['first_name'], data['number'], data['description'], data['name'], user_id))
        db.commit()

async def get_all_products():

    profile = cur.execute("SELECT * FROM profile").fetchall()

    return profile


