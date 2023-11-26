import sys
import mysql.connector
import constants
from datetime import datetime


# Are we going off Spotify ID or email?? When we decide, modify the SQL query as such
# First argument is a MySQL connection which can be obtained via:
# conn = mysql.connector.connect(user=constants.USERNAME, password=constants.PASSWORD, host=constants.HOST, database=constants.DATABASE)
# Remember to conn.close() when finished with the connection
def get_top_ids(conn, email):
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Execute the SQL query, one length tuple needs the comma (execute only takes tuples as second argument)
    cursor.execute("SELECT TOP_100_ID FROM USER_SONGS WHERE EMAIL = %s", (email,))

    # Grab the first one? (Maybe replace this with most recent)
    id_string = cursor.fetchone()[0]

    # Get the individual ids into a list
    song_ids = id_string.split('-')

    return song_ids

# First argument is a MySQL connection which can be obtained via:
# conn = mysql.connector.connect(user=constants.USERNAME, password=constants.PASSWORD, host=constants.HOST, database=constants.DATABASE)
# Remember to conn.close() when finished with the connection
def add_match_email(conn, email, spotify_id, result_ids):
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Preparing SQL query to INSERT a record into the database.
    insert_stmt = (
    "INSERT INTO USER_SONGS(EMAIL, SPOTIFY_ID, TOP_100_ID, LAST_RECEIVED, MATCH_EMAIL, MATCH_SPOTIFY_ID)"
    "VALUES (%s, %s, %s, %s, %s, %s)"
    )

    # Get the current time so we can keep track of when we last grabbed the user's top 100 songs
    # Format it for MySQL
    now = datetime.now()
    formatted_now = now.strftime('%Y-%m-%d %H:%M:%S')


    data = (email, spotify_id, result_ids, formatted_now, None, None)

    try:
        # Executing the SQL command
        cursor.execute(insert_stmt, data)
    
        # Commit your changes in the database
        conn.commit()
        return True

    except:
        # Rolling back in case of error
        conn.rollback()
        return False


# First argument is a MySQL connection which can be obtained via:
# conn = mysql.connector.connect(user=constants.USERNAME, password=constants.PASSWORD, host=constants.HOST, database=constants.DATABASE)
# Remember to conn.close() when finished with the connection
def update_match_email(conn, email, match_email):
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Execute SQL query
    cursor.execute("UPDATE USER_SONGS SET MATCH_EMAIL = %s WHERE EMAIL = %s", (match_email, email))

    # Commit changes
    conn.commit()

# First argument is a MySQL connection which can be obtained via:
# conn = mysql.connector.connect(user=constants.USERNAME, password=constants.PASSWORD, host=constants.HOST, database=constants.DATABASE)
# Third argument is a string of form "id-id-id..."
# Remember to conn.close() when finished with the connection
def update_user_songs(conn, email, top_ids):
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Execute SQL query
    cursor.execute("UPDATE USER_SONGS SET TOP_100_ID = %s WHERE EMAIL = %s", (top_ids, email))

    # Commit changes
    conn.commit()

# Argument centroids is a 5-list of centroids
# First argument is a MySQL connection which can be obtained via:
# conn = mysql.connector.connect(user=constants.USERNAME, password=constants.PASSWORD, host=constants.HOST, database=constants.DATABASE)
# Third argument is a string of form "id-id-id..."
# Remember to conn.close() when finished with the connection
def update_user_centroids(conn, email, centroids):
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Get user songs from DB
    top_ids = get_top_ids(conn, email)

    # ERIC CODE

    # Perhaps inefficient? But sets each field manually
    # Execute SQL queries
    cursor.execute("UPDATE USER_SONGS SET CENTROID_1 = %s WHERE EMAIL = %s", (centroids[0], email))
    cursor.execute("UPDATE USER_SONGS SET CENTROID_2 = %s WHERE EMAIL = %s", (centroids[1], email))
    cursor.execute("UPDATE USER_SONGS SET CENTROID_3 = %s WHERE EMAIL = %s", (centroids[2], email))
    cursor.execute("UPDATE USER_SONGS SET CENTROID_4 = %s WHERE EMAIL = %s", (centroids[3], email))
    cursor.execute("UPDATE USER_SONGS SET CENTROID_5 = %s WHERE EMAIL = %s", (centroids[4], email))

    # Commit changes
    conn.commit()

# Argument attributes is given from Spotify API
# First argument is a MySQL connection which can be obtained via:
# conn = mysql.connector.connect(user=constants.USERNAME, password=constants.PASSWORD, host=constants.HOST, database=constants.DATABASE)
# Remember to conn.close() when finished with the connection
def insert_track(conn, attributes):
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    """
    Order of columns in table: 
    TRACK_ID
    TRACK_NAME
    ARTIST_NAME
    ACOUSTICNESS
    DANCEABILITY
    DURATION
    ENERGY
    INSTRUMENTALNESS
    LIVENESS
    LOUDNESS
    MODE
    SPEECHINESS
    TEMPO
    TIME_SIGNATURE
    VALENCE
    POPULARITY
    """

    insert_stmt = (
    "INSERT INTO 221_PROJECT(TRACK_ID, TRACK_NAME, ARTIST_NAME, ACOUSTICNESS, DANCEABILITY, DURATION, ENERGY, INSTRUMENTALNESS, LIVENESS, LOUDNESS, MODE, SPEECHINESS, TEMPO, TIME_SIGNATURE, VALENCE, POPULARITY)"
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )

    data = (attributes['id'], attributes['track_name'], attributes['artist_name'], attributes['acousticness'], attributes['danceability'], attributes['duration'], attributes['energy'], attributes['instrumentalness'], attributes['liveness'], attributes['loudness'], attributes['mode'], attributes['speechiness'], attributes['tempo'], attributes['time_signature'], attributes['valence'], attributes['popularity'])

    try:
        # Executing the SQL command
        cursor.execute(insert_stmt, data)
    
        # Commit your changes in the database
        conn.commit()
        return True

    except:
        # Rolling back in case of error
        conn.rollback()
        return False


if __name__ == "__main__":
    flags = ['-get', '-add']
    if len(sys.argv) < 2 or sys.argv[1] not in flags:
        print ("Please give a input flag")
    elif len(sys.argv) > 2:
        flag = sys.argv[1]
        if flag == '-get':
            search_email = sys.argv[2]
            conn = mysql.connector.connect(user=constants.USERNAME, password=constants.PASSWORD, host=constants.HOST, database=constants.DATABASE)
            print(get_top_ids(conn, search_email))
            conn.close()
        if flag == '-add' and len(sys.argv) > 4:
            conn = mysql.connector.connect(user=constants.USERNAME, password=constants.PASSWORD, host=constants.HOST, database=constants.DATABASE)
            if (add_match_email(conn, email=sys.argv[2], spotify_id=sys.argv[3], result_ids=sys.argv[4])):
                print('success')
            else:
                print('failure')
            conn.close()
            