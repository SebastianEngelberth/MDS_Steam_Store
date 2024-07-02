import pandas as pd
import oracledb as odb
import string
import random
import numpy as np
from datetime import datetime, timedelta

developers = None
publishers = None
categories = None
genres = None
tags = None

user = "system"
host = "localhost"
port = 1521
sid = ""
userpwd = ""
dns_string = odb.makedsn(host, port, sid)
connection = odb.connect(user=user, password=userpwd, dsn=dns_string)


def load_csv_to_dataframe(filename):
    try:
        dataframe = pd.read_csv(filename)
        print("Data loaded successfully.")
        return dataframe
    except Exception as e:
        print(f"An error occurred while loading the data: {e}")
        return None


def preprocess_dataframe(dataframe):
    for column in dataframe.columns:
        if dataframe[column].dtype == float or dataframe[column].dtype == int:
            dataframe[column].fillna(0, inplace=True)
        elif dataframe[column].dtype == 'object':  # Assuming 'object' dtype as strings
            dataframe[column].fillna('', inplace=True)
            dataframe[column] = dataframe[column].apply(lambda x: x.replace("'", ""))
        elif dataframe[column].dtype == 'datetime64[ns]':
            dataframe[column].fillna(pd.Timestamp('1900-01-01'), inplace=True)
    print(dataframe.columns)
    dataframe = dataframe.drop(
        columns=['english', 'platforms', 'achievements', 'average_playtime', 'median_playtime',
                 'owners'])
    return dataframe


def get_dicts(dataframe):
    developers_set = set()
    dev_df = dataframe["developer"]

    for developers_i in dev_df:
        devs = [dev.strip() for dev in developers_i.split(';')]
        developers_set.update(devs)

    global developers
    developers = {dev: idx + 1 for idx, dev in enumerate(sorted(developers_set))}

    publishers_set = set()
    pub_df = dataframe["publisher"]

    for publishers_i in pub_df:
        pubs = [pub.strip() for pub in publishers_i.split(';')]
        publishers_set.update(pubs)

    global publishers
    publishers = {dev: idx + 1 for idx, dev in enumerate(sorted(publishers_set))}

    categories_set = set()
    cat_df = dataframe["categories"]

    for categories_i in cat_df:
        cats = [cat.strip() for cat in categories_i.split(';')]
        categories_set.update(cats)

    global categories
    categories = {dev: idx + 1 for idx, dev in enumerate(sorted(categories_set))}

    genres_set = set()
    gen_df = dataframe["genres"]

    for genres_i in gen_df:
        gens = [gen.strip() for gen in genres_i.split(';')]
        genres_set.update(gens)

    global genres
    genres = {dev: idx + 1 for idx, dev in enumerate(sorted(genres_set))}

    tags_set = set()
    tag_df = dataframe["steamspy_tags"]

    for tags_i in tag_df:
        tags_j = [tag.strip() for tag in tags_i.split(';')]
        tags_set.update(tags_j)

    global tags
    tags = {dev: idx + 1 for idx, dev in enumerate(sorted(tags_set))}


def get_dev_relationships(filename, dataframe):
    global developers
    dataframe = dataframe[['appid', 'developer']]
    cnt = 0

    try:
        with open(filename, 'w', encoding="utf-8") as file:
            file.write("BEGIN\n")
            for index, row in dataframe.iterrows():
                devs = [i.strip() for i in str(row['developer']).split(';')]
                dev_ids = []
                for i in devs:
                    dev_ids.append(developers.get(i))

                for i in dev_ids:
                    file.write(
                        f" INSERT INTO develops (developer_id, videogame_id) VALUES ({i}, {row['appid']});\n"
                    )
                    cnt += 1
                    if cnt >= 500:
                        cnt = 0
                        file.write(" COMMIT;\n")
                        file.write("END;\n")
                        file.write("BEGIN")
            file.write(" COMMIT;\n")
            file.write("END;\n")
        print(f"SQL insert statements written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing SQL inserts: {e}")


def get_genre_relationships(filename, dataframe):
    global genres
    dataframe = dataframe[['appid', 'genres']]
    cnt = 0

    try:
        with open(filename, 'w', encoding="utf-8") as file:
            file.write("BEGIN\n")
            for index, row in dataframe.iterrows():
                devs = [i.strip() for i in str(row['genres']).split(';')]
                dev_ids = []
                for i in devs:
                    dev_ids.append(genres.get(i))

                for i in dev_ids:
                    file.write(
                        f" INSERT INTO belongs_to_gen (genre_id, videogame_id) VALUES ({i}, {row['appid']});\n"
                    )
                    cnt += 1
                    if cnt >= 500:
                        cnt = 0
                        file.write(" COMMIT;\n")
                        file.write("END;\n")
                        file.write("BEGIN")
            file.write(" COMMIT;\n")
            file.write("END;\n")
        print(f"SQL insert statements written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing SQL inserts: {e}")


def get_tag_relationships(filename, dataframe):
    global tags
    dataframe = dataframe[['appid', 'steamspy_tags']]
    cnt = 0

    try:
        with open(filename, 'w', encoding="utf-8") as file:
            file.write("BEGIN\n")
            for index, row in dataframe.iterrows():
                devs = [i.strip() for i in str(row['steamspy_tags']).split(';')]
                dev_ids = []
                for i in devs:
                    dev_ids.append(tags.get(i))

                for i in dev_ids:
                    file.write(
                        f" INSERT INTO tagged_with (tag_id, videogame_id) VALUES ({i}, {row['appid']});\n"
                    )
                    cnt += 1
                    if cnt >= 500:
                        cnt = 0
                        file.write(" COMMIT;\n")
                        file.write("END;\n")
                        file.write("BEGIN")
            file.write(" COMMIT;\n")
            file.write("END;\n")
        print(f"SQL insert statements written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing SQL inserts: {e}")


def get_cat_relationships(filename, dataframe):
    global categories
    dataframe = dataframe[['appid', 'categories']]
    cnt = 0

    try:
        with open(filename, 'w', encoding="utf-8") as file:
            file.write("BEGIN\n")
            for index, row in dataframe.iterrows():
                devs = [i.strip() for i in str(row['categories']).split(';')]
                dev_ids = []
                for i in devs:
                    dev_ids.append(categories.get(i))

                for i in dev_ids:
                    file.write(
                        f" INSERT INTO belongs_to_cat (category_id, videogame_id) VALUES ({i}, {row['appid']});\n"
                    )
                    cnt += 1
                    if cnt >= 500:
                        cnt = 0
                        file.write(" COMMIT;\n")
                        file.write("END;\n")
                        file.write("BEGIN")
            file.write(" COMMIT;\n")
            file.write("END;\n")
        print(f"SQL insert statements written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing SQL inserts: {e}")


def get_pub_relationships(filename, dataframe):
    global publishers
    dataframe = dataframe[['appid', 'publisher']]
    cnt = 0

    try:
        with open(filename, 'w', encoding="utf-8") as file:
            file.write("BEGIN\n")
            for index, row in dataframe.iterrows():
                devs = [i.strip() for i in str(row['publisher']).split(';')]
                dev_ids = []
                for i in devs:
                    dev_ids.append(publishers.get(i))

                for i in dev_ids:
                    file.write(
                        f" INSERT INTO publishes (publisher_id, videogame_id) VALUES ({i}, {row['appid']});\n"
                    )
                    cnt += 1
                    if cnt >= 500:
                        cnt = 0
                        file.write(" COMMIT;\n")
                        file.write("END;\n")
                        file.write("BEGIN")
            file.write(" COMMIT;\n")
            file.write("END;\n")
        print(f"SQL insert statements written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing SQL inserts: {e}")


def write_videogame_inserts(dataframe, filename):
    cnt = 0

    with open(filename, 'w', encoding="utf-8") as file:
        file.write("BEGIN\n")
        for index, row in dataframe.iterrows():
            file.write(
                f" INSERT INTO videogame (videogame_id, name, release_date, required_age, price, positive_ratings, "
                f"negative_ratings) VALUES ({int(row['appid'])}, \'{str(row['name'])}\', TO_DATE(\'{str(row['release_date'])}\', 'YYYY-MM-DD'), {int(row['required_age'])}, {float(row['price'])}, {int(row['positive_ratings'])}, {int(row['negative_ratings'])});\n")
            cnt += 1
            if cnt >= 500:
                cnt = 0
                file.write(" COMMIT;\n")
                file.write("END;\n")
                file.write("BEGIN\n")
        file.write("END;\n")
    print(f"SQL insert statements written")


def write_developer_inserts(filename):
    cnt = 0

    try:
        with open(filename, 'w', encoding="utf-8") as file:
            file.write("BEGIN\n")
            for developer_name, developer_id in developers.items():
                # Ensure the developer name is correctly escaped for SQL insertion
                # developer_name_escaped = developer_name.replace("'", "''")
                file.write(
                    f" INSERT INTO developer (developer_id, name) VALUES ({developer_id}, \'{developer_name}\');\n"
                )
                cnt += 1
                if cnt >= 500:
                    cnt = 0
                    file.write(" COMMIT;\n")
                    file.write("END;\n")
                    file.write("BEGIN")
            file.write(" COMMIT;\n")
            file.write("END;\n")
        print(f"SQL insert statements written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing SQL inserts: {e}")


def write_publisher_inserts(filename):
    cnt = 0

    try:
        with open(filename, 'w', encoding="utf-8") as file:
            file.write("BEGIN\n")
            for publisher_name, publisher_id in publishers.items():
                file.write(
                    f" INSERT INTO publisher (publisher_id, name) VALUES ({publisher_id}, \'{publisher_name}\');\n"
                )
                cnt += 1
                if cnt >= 500:
                    cnt = 0
                    file.write(" COMMIT;\n")
                    file.write("END;\n")
                    file.write("BEGIN")
            file.write(" COMMIT;\n")
            file.write("END;\n")
        print(f"SQL insert statements written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing SQL inserts: {e}")


def write_category_inserts(filename):
    try:
        with open(filename, 'w', encoding="utf-8") as file:
            file.write("BEGIN\n")
            for category_name, category_id in categories.items():
                file.write(
                    f" INSERT INTO category (category_id, name) VALUES ({category_id}, \'{category_name}\');\n"
                )
            file.write("END;\n")
        print(f"SQL insert statements written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing SQL inserts: {e}")


def write_genre_inserts(filename):
    try:
        with open(filename, 'w', encoding="utf-8") as file:
            file.write("BEGIN\n")
            for genre_name, genre_id in genres.items():
                file.write(
                    f" INSERT INTO genre (genre_id, name) VALUES ({genre_id}, \'{genre_name}\');\n"
                )
            file.write("END;\n")
        print(f"SQL insert statements written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing SQL inserts: {e}")


def write_tag_inserts(filename):
    try:
        with open(filename, 'w', encoding="utf-8") as file:
            file.write("BEGIN\n")
            for tag_name, tag_id in tags.items():
                file.write(
                    f" INSERT INTO tag (tag_id, name) VALUES ({tag_id}, \'{tag_name}\');\n"
                )
            file.write("END;\n")
        print(f"SQL insert statements written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing SQL inserts: {e}")


def find_duplicate_lines(filename):
    line_count = {}
    duplicates = {}

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            # Normalize lines to compare them fairly, strip leading/trailing whitespace
            normalized_line = line.strip()
            if normalized_line in line_count:
                line_count[normalized_line] += 1
            else:
                line_count[normalized_line] = 1

    # Identify duplicates
    for line, count in line_count.items():
        if count > 1:
            duplicates[line] = count

    return duplicates


def generate_random_username(max_length=30):
    # Characters to include in the username
    characters = string.ascii_letters + string.digits + "_"

    # Ensure the username is at least 1 character and does not exceed the max_length
    username_length = random.randint(1, max_length)

    # Generate the random username
    username = ''.join(random.choice(characters) for _ in range(username_length))

    return username


def generate_random_email(max_length=30):
    # Characters to include in the email username part
    characters = string.ascii_letters + string.digits + "_."

    # Define some common email domains and suffixes
    domains = ['gmail', 'yahoo', 'hotmail', 'outlook', 'example']
    suffixes = ['com', 'net', 'org', 'edu', 'io']

    # Randomly choose a domain and a suffix
    domain = random.choice(domains)
    suffix = random.choice(suffixes)

    # Calculate maximum username length (account for '@', domain, '.', and suffix)
    max_username_length = max_length - (len(domain) + len(suffix) + 2)

    # Generate the random username part of the email
    username_length = random.randint(1, max_username_length)
    username = ''.join(random.choice(characters) for _ in range(username_length))

    # Construct the full email address
    email = f"{username}@{domain}.{suffix}"

    return email


def create_random_dataframe():
    # Define the number of initial rows (slightly more to account for duplicates removal)
    num_rows = 110000

    # Generate random integers between 0 and 49999
    data = {
        'Column1': np.random.randint(0, 50000, size=num_rows),
        'Column2': np.random.randint(0, 50000, size=num_rows)
    }

    # Create the DataFrame
    dataframe = pd.DataFrame(data)

    # Remove duplicate rows
    dataframe.drop_duplicates(inplace=True)

    # If more than 100000 rows remain after dropping duplicates, trim the excess
    if len(dataframe) > 100000:
        dataframe = dataframe.iloc[:100000]

    return dataframe


def create_user_data(filename):
    cnt = 0
    try:
        with open(filename, 'w', encoding="utf-8") as file:
            file.write("BEGIN\n")
            for i in range(50000):
                file.write(
                    f" INSERT INTO \"USER\" (user_id, username, email, age, password) VALUES ({i}, \'{generate_random_username()}\', \'{generate_random_email()}\', {random.randint(16, 80)}, \'{'password123'}\');\n"
                )
                cnt += 1
                if cnt >= 500:
                    cnt = 0
                    file.write(" COMMIT;\n")
                    file.write("END;\n")
                    file.write("BEGIN")
            file.write(" COMMIT;\n")
            file.write("END;\n")
        print(f"SQL insert statements written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing SQL inserts: {e}")


def create_friend_data(filename):
    data = create_random_dataframe()
    cnt = 0
    try:
        with open(filename, 'w', encoding="utf-8") as file:
            file.write("BEGIN\n")
            for index, row in data.iterrows():
                file.write(
                    f" INSERT INTO friends_with (user1_id, user2_id) VALUES ({row['Column1']}, {row['Column2']});\n"
                )
                cnt += 1
                if cnt >= 500:
                    cnt = 0
                    file.write(" COMMIT;\n")
                    file.write("END;\n")
                    file.write("BEGIN")
            file.write(" COMMIT;\n")
            file.write("END;\n")
        print(f"SQL insert statements written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing SQL inserts: {e}")


def generate_owner_data(input_df):
    # Check if the 'appid' column exists in the input DataFrame
    if 'appid' not in input_df.columns:
        raise ValueError("Input DataFrame must contain an 'appid' column")

    input_df.drop(input_df.tail(20000).index, inplace=True)

    # Constants for the date range (2012 to current date)
    start_date = datetime(2012, 1, 1)
    end_date = datetime.now()

    # Number of days between start_date and end_date
    days_between_dates = (end_date - start_date).days

    # Generate 200,000 random user_ids, purchase_dates, and playtimes
    user_ids = np.random.normal(25000, 2000, size=200000).astype(int)
    user_ids = np.maximum(user_ids, 0)
    user_ids = np.minimum(user_ids, 50000)
    purchase_dates = [start_date + timedelta(days=np.random.randint(days_between_dates)) for _ in range(200000)]
    playtimes = np.random.normal(3000, 10, 200000).astype(int)
    playtimes = np.maximum(playtimes, 0)


    videogame_ids = np.array(input_df['appid'])
    random_props = np.random.rand(len(videogame_ids))
    probabilities = random_props / random_props.sum()
    selected_ids = np.random.choice(videogame_ids, size=200000, p=probabilities)

    # Create the DataFrame
    output_df = pd.DataFrame({
        'user_id': user_ids,
        'videogame_id': selected_ids,
        'purchase_date': purchase_dates,
        'playtime': playtimes
    })

    output_df['purchase_date'] = output_df['purchase_date'].dt.strftime('%Y-%m-%d')

    return output_df


def create_owns_data(dataframe, filename):
    data = generate_owner_data(dataframe)
    cnt = 0
    try:
        with open(filename, 'w', encoding="utf-8") as file:
            file.write("BEGIN\n")
            for index, row in data.iterrows():
                file.write(
                    f" INSERT INTO owns (user_id, videogame_id, purchase_date, playtime) VALUES ({row['user_id']}, {row['videogame_id']}, TO_DATE(\'{str(row['purchase_date'])}\', 'YYYY-MM-DD'), {row['playtime']});\n"
                )
                cnt += 1
                if cnt >= 500:
                    cnt = 0
                    file.write(" COMMIT;\n")
                    file.write("END;\n")
                    file.write("BEGIN")
            file.write(" COMMIT;\n")
            file.write("END;\n")
        print(f"SQL insert statements written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing SQL inserts: {e}")


csv_filename = 'E:/Studium/Master/2_Semester/MDS/data/steam.csv'
videogame_filename = 'E:/Studium/Master/2_Semester/MDS/Oracle SQL/videogame_data.sql'
developer_filename = 'E:/Studium/Master/2_Semester/MDS/Oracle SQL/developer_data.sql'
publisher_filename = 'E:/Studium/Master/2_Semester/MDS/Oracle SQL/publisher_data.sql'
category_filename = 'E:/Studium/Master/2_Semester/MDS/Oracle SQL/category_data.sql'
genre_filename = 'E:/Studium/Master/2_Semester/MDS/Oracle SQL/genre_data.sql'
tag_filename = 'E:/Studium/Master/2_Semester/MDS/Oracle SQL/tag_data.sql'

dev_rela = 'E:/Studium/Master/2_Semester/MDS/Oracle SQL/dev_rela_data.sql'
pub_rela = 'E:/Studium/Master/2_Semester/MDS/Oracle SQL/pub_rela_data.sql'
genre_rela = 'E:/Studium/Master/2_Semester/MDS/Oracle SQL/genre_rela_data.sql'
category_rela = 'E:/Studium/Master/2_Semester/MDS/Oracle SQL/cat_rela_data.sql'
tag_rela = 'E:/Studium/Master/2_Semester/MDS/Oracle SQL/tag_rela_data.sql'

user_filename = 'E:/Studium/Master/2_Semester/MDS/Oracle SQL/user_data.sql'
friend_filename = 'E:/Studium/Master/2_Semester/MDS/Oracle SQL/friend_data.sql'
owns_filename = 'E:/Studium/Master/2_Semester/MDS/Oracle SQL/owns_data.sql'
owns2_filename = 'E:/Studium/Master/2_Semester/MDS/Oracle_SQL/owns2_data.sql'

# Load the CSV into a DataFrame
df = load_csv_to_dataframe(csv_filename)

if df is not None:
    df = preprocess_dataframe(df)
    get_dicts(df)
    write_videogame_inserts(df, videogame_filename)
    write_developer_inserts(developer_filename)
    write_publisher_inserts(publisher_filename)
    write_category_inserts(category_filename)
    write_genre_inserts(genre_filename)
    get_dev_relationships(dev_rela, df)
    get_genre_relationships(genre_rela, df)
    get_cat_relationships(category_rela, df)
    get_pub_relationships(pub_rela, df)
    create_user_data(user_filename)
    create_friend_data(friend_filename)
    create_owns_data(df, owns2_filename)
    write_tag_inserts(tag_filename)
    get_tag_relationships(tag_rela, df)
