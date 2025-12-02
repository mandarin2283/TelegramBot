import sqlite3 as sq


db = sq.connect('stats.db')
cur = db.cursor()


async def db_start():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_id INTEGER NOT NULL,
            exercise_id INTEGER NOT NULL,
            set_index INTEGER,
            weight REAL,
            reps INTEGER,
            FOREIGN KEY (workout_id) REFERENCES workouts(id),
            FOREIGN KEY (exercise_id) REFERENCES exercises(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        grade FLOAT
        )
    """)

    db.commit()


async def add_train(date,train_type):
    cur.execute("INSERT INTO workouts (date, type) VALUES (?, ?)",
                (date,train_type))
    db.commit()
    return cur.lastrowid


async def get_or_create_exercise(name):
    cur.execute("SELECT id FROM exercises WHERE name = ?", (name,))
    result = cur.fetchone()
    if result:
        return result[0]
    cur.execute("INSERT INTO exercises (name) VALUES (?)", (name,))
    db.commit()
    return cur.lastrowid


async def add_set(workout_id, exercise_name, set_index, weight, reps):
    exercise_id = await get_or_create_exercise(exercise_name)
    cur.execute("""
        INSERT INTO sets (workout_id, exercise_id, set_index, weight, reps)
        VALUES (?, ?, ?, ?, ?)
    """, (workout_id, exercise_id, set_index, weight, reps))
    db.commit()
    print('Подход добавлен')


async def save_movie(imdb_data,grade):
    print(imdb_data)
    title = imdb_data['Title']
    cur.execute("INSERT INTO movies (title,grade) VALUES (?,?)", (title,grade))
    db.commit()

