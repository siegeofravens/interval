import sys
import mysql.connector
import constants


# Are we going off Spotify ID or email?? When we decide, modify the SQL query as such
# First argument is a MySQL connection which can be obtained via:
# conn = mysql.connector.connect(user=constants.USERNAME, password=constants.PASSWORD, host=constants.HOST, database=constants.DATABASE)
# Remember to conn.close() when finished with the connection
def get_top_ids(conn, spotify_id):
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Execute the SQL query, one length tuple needs the comma (execute only takes tuples as second argument)
    cursor.execute("SELECT TOP_100_ID FROM USER_SONGS WHERE SPOTIFY_ID = %s", (spotify_id,))

    # Grab the first one? (Maybe replace this with most recent)
    id_string = cursor.fetchone()[0]

    # Get the individual ids into a list
    song_ids = id_string.split('-')

    return song_ids

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



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Please input Spotify ID argument")
    else:
        result_list = get_top_ids(sys.argv[1])
        for result in result_list:
            print(result)