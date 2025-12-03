import os

import psycopg2 as sq


db = sq.connect(os.environ['DB_URL'])
cur = db.cursor()


async def db_start():
    cur.execute("""
            CREATE TABLE IF NOT EXISTS workouts (
        id SERIAL PRIMARY KEY,
        date TEXT NOT NULL,
        type TEXT NOT NULL
    );
        
    """)

    cur.execute("""
            CREATE TABLE IF NOT EXISTS exercises (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
    );

    """)

    cur.execute("""
            CREATE TABLE IF NOT EXISTS sets (
        id SERIAL PRIMARY KEY,
        workout_id INTEGER NOT NULL REFERENCES workouts(id),
        exercise_id INTEGER NOT NULL REFERENCES exercises(id),
        set_index INTEGER,
        weight REAL,
        reps INTEGER
    );

    """)

    cur.execute("""
            CREATE TABLE IF NOT EXISTS movies (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        grade REAL
    );

    """)

    db.commit()


async def add_train(date,train_type):
    cur.execute("INSERT INTO workouts (date, type) VALUES (%s, %s)",
                (date,train_type))
    db.commit()
    return cur.lastrowid


async def get_or_create_exercise(name):
    cur.execute("SELECT id FROM exercises WHERE name = %s", (name,))
    result = cur.fetchone()
    if result:
        return result[0]
    cur.execute("INSERT INTO exercises (name) VALUES (%s)", (name,))
    db.commit()
    return cur.lastrowid


async def add_set(workout_id, exercise_name, set_index, weight, reps):
    exercise_id = await get_or_create_exercise(exercise_name)
    cur.execute("""
        INSERT INTO sets (workout_id, exercise_id, set_index, weight, reps)
        VALUES (%s, %s, %s, %s, %s)
    """, (workout_id, exercise_id, set_index, weight, reps))
    db.commit()
    print('Подход добавлен')


async def save_movie(imdb_data,grade):
    print(imdb_data)
    title = imdb_data['Title']
    cur.execute("INSERT INTO movies (title,grade) VALUES (%s,%s)", (title,grade))
    db.commit()

