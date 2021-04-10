import sqlite3
import argparse
from sqlite3 import Error


def create_connection(db_name):
    """ create a database connection to a database that resides
        in the memory
    """
    connection = None
    try:
        connection = sqlite3.connect(f'./{db_name}')
        return connection
    except Error as e:
        print(e)
        return connection


def create_tables(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :return:
    """
    table_measures = """
    create table if not exists measures (
        measure_id INTEGER PRIMARY KEY,
        measure_name TEXT UNIQUE
    )
    """

    table_ingredients = """
    create table if not exists ingredients (
        ingredient_id INTEGER PRIMARY KEY,
        ingredient_name TEXT NOT NULL UNIQUE
    )
    """

    table_meals = """
    create table if not exists meals (
        meal_id INTEGER PRIMARY KEY,
        meal_name TEXT NOT NULL UNIQUE
    )
    """

    table_recipes = """
    create table if not exists recipes ( 
        recipe_id INTEGER PRIMARY KEY,
        recipe_name TEXT NOT NULL,
        recipe_description TEXT
    )
    """

    table_serve = """
    create table if not exists serve ( 
        serve_id INTEGER PRIMARY KEY,
        recipe_id INTEGER NOT NULL,
        meal_id INTEGER NOT NULL,
        FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id),
        FOREIGN KEY(meal_id) REFERENCES meals(meal_id)
   )
    """

    table_quantity = """
    create table if not exists quantity (
        quantity_id INTEGER PRIMARY KEY,
        quantity INTEGER NOT NULL,
        recipe_id INTEGER NOT NULL,
        measure_id INTEGER NOT NULL,
        ingredient_id INTEGER NOT NULL,
        FOREIGN KEY(measure_id) REFERENCES measures(measure_id),
        FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id),
        FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id)
    )
    """

    try:
        c = conn.cursor()
        c.execute("""PRAGMA foreign_keys = ON""")
        table_list = [
            table_measures,
            table_ingredients,
            table_meals,
            table_recipes,
            table_serve,
            table_quantity
        ]
        for table in table_list:
            c.execute(table)
    except Error as e:
        print(e)


def insert_into_ingredients(conn, elements):
    cursor = conn.cursor()
    res = cursor.execute("""SELECT * FROM ingredients""").fetchone()
    if res:
       return True
    try:
        stmt = "insert into ingredients (ingredient_id, ingredient_name) values (?, ?)"
        values = [*map(lambda el: (None, el), elements)]
        cursor.executemany(stmt, values)
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False


def insert_into_measures(conn, elements):
    cursor = conn.cursor()
    res = cursor.execute("""SELECT * FROM measures""").fetchone()
    if res:
        return True
    try:
        cursor = conn.cursor()
        stmt = "insert into measures  (measure_id , measure_name ) values (?, ?)"
        values = [*map(lambda el: (None, el), elements)]
        cursor.executemany(stmt, values)
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False


def insert_into_meals(conn, elements):
    cursor = conn.cursor()
    res = cursor.execute("""SELECT * FROM meals""").fetchone()
    if res:
        return True
    try:
        cursor = conn.cursor()
        stmt = "insert into meals(meal_id, meal_name) values (?, ?)"
        values = [*map(lambda el: (None, el), elements)]
        cursor.executemany(stmt, values)
        conn.commit()
        return cursor
    except Error as e:
        print(e)
        return False


def insert_into_serve(conn, last_id):
    try:
        avail_meals = conn.execute("""SELECT * FROM meals""").fetchall()
        print('  '.join([f"{n}) {meal}" for n, meal in avail_meals]))
        dish_serve = tuple(map(int, input('Enter proposed meals separated by a space: ').split(' ')))
        stmt_recipe = "insert into serve(meal_id, recipe_id) values (?, ?)"
        for meal_id in dish_serve:
            conn.execute(stmt_recipe, (meal_id, last_id))
            conn.commit()
        insert_into_quantity(conn, last_id)
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False


def insert_into_quantity(conn, last_recipe_id):
    stmt_quantity = "insert into quantity(quantity, recipe_id, measure_id, ingredient_id) values (?, ?, ?, ?)"
    while True:
        try:
            string = input('Input quantity of ingredient <press enter to stop>: ')
            if string.strip() == '':
                break
            if len(string.split()) == 2:
                q, i = string.split(' ')
                m = ''
            elif len(string.split()) == 3:
                q, m, i = string.split(' ')
            else:
                break
            try:
                measure = conn.execute("SELECT measure_id FROM measures WHERE measure_name = (?)", [m]).fetchone()
                assert measure, "The measure is not conclusive!"
                ingredient = conn.execute("SELECT ingredient_id FROM ingredients WHERE ingredient_name LIKE ?", ['%'+i+'%']).fetchall()
                assert ingredient and len(ingredient) == 1, "The ingredient is not conclusive!"
                measure_id, ingredient_id = measure[0], ingredient[0][0]
                conn.execute(stmt_quantity, (int(q), int(last_recipe_id), int(measure_id), int(ingredient_id)))
                conn.commit()
            except Error as e:
                print(e)
            except AssertionError as e:
                print(e)
                continue
        except Error as e:
            print(e)
            return False


def insert_recipe(conn):
    stmt = "insert into recipes (recipe_name , recipe_description ) values (?, ?)"
    print('Pass the empty recipe name to exit.')
    recipe = input('Recipe name: ').strip()
    if recipe.strip() == '':
        return False
    else:
        recipe_desc = input('Recipe description: ')
        try:
            last_id = conn.execute(stmt, (recipe, recipe_desc)).lastrowid
            conn.commit()
            insert_into_serve(conn, last_id)
            return True
        except Error as e:
            print(e)
            return False


def select_recipe_by_ingredients_meals(conn, ingredients, meals):
    t_ingredients = tuple(ingredients.split(','))
    t_meals = tuple(meals.split(','))
    cur = conn.cursor()
    recipe_stmt = f"""
    SELECT r.recipe_id, recipe_name
    FROM (SELECT * FROM ingredients WHERE ingredient_name IN ({','.join('?'*len(t_ingredients))})) i
    INNER JOIN quantity q
    ON i.ingredient_id = q.ingredient_id
    INNER JOIN recipes r
    ON q.recipe_id = r.recipe_id
    INNER JOIN serve s
    ON s.recipe_id = r.recipe_id
    INNER JOIN (SELECT * FROM meals WHERE meal_name IN ({','.join('?'*len(t_meals))})) m
    ON m.meal_id = s.meal_id
    GROUP BY r.recipe_id 
    HAVING COUNT(DISTINCT i.ingredient_id) = ?
    """
    res = cur.execute(recipe_stmt, (*t_ingredients, *t_meals, len(t_ingredients))).fetchall()
    if not res:
        print('no such recipes')
    else:
        output = ', '.join([el[1] for el in res])
        print(output)


def main(conn, arg_ingredients, arg_meals):
    data = {
        "meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")
    }
    _ = insert_into_ingredients(conn, data['ingredients'])
    _ = insert_into_measures(conn, data['measures'])
    _ = insert_into_meals(conn, data['meals'])
    if arg_ingredients or arg_meals:
        select_recipe_by_ingredients_meals(conn, arg_ingredients, arg_meals)
    else:
        while True:
            rec = insert_recipe(conn)
            if not rec:
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Database for recipes.")
    parser.add_argument('database', metavar='db', type=str, nargs='?', help="Database name", default='food_blog.db')
    parser.add_argument('--ingredients', type=str, nargs='?', help="Ingredients list", default=None, required=False)
    parser.add_argument('--meals', type=str, nargs='?', help="Meals list", default=None, required=False)
    argv = parser.parse_args()
    init_conn = create_connection(argv.database)
    list_ingredients = argv.ingredients if argv.ingredients else ''
    list_meals = argv.meals if argv.meals else ''
    create_tables(init_conn)
    main(init_conn, list_ingredients, list_meals)
    init_conn.close()
