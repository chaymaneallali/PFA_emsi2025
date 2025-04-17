# import pandas as pd
# from sqlalchemy import create_engine
# from sqlalchemy.exc import SQLAlchemyError

# DB_CONFIG = {
#     "host": "localhost",
#     "database": "Mymovie",
#     "user": "postgres",
#     "password": "Wben2003",
#     "port": "5432"
# }

# MOVIES_CSV = "movies_with_posters.csv"

# def import_movies():
#     engine = create_engine(
#         f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
#         f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
#     )

#     try:
#         # Read CSV and rename columns
#         movies_df = pd.read_csv(MOVIES_CSV)
#         movies_df = movies_df.rename(columns={"movieId": "movie_id"})  # Fix column name

#         # Clean genres (if needed)
#         movies_df['genres'] = movies_df['genres'].str.strip("[]'").str.replace("', '", ", ")

#         # Insert data
#         movies_df.to_sql(
#             name='movies',
#             con=engine,
#             if_exists='append',
#             index=False,
#             method='multi'
#         )
#         print(f"Inserted {len(movies_df)} movies successfully!")

#     except SQLAlchemyError as e:
#         print(f"Database Error: {str(e)}")
#     except Exception as e:
#         print(f"General Error: {str(e)}")
#     finally:
#         engine.dispose()

# if __name__ == "__main__":
#     import_movies()

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Database configuration (update if needed)
DB_CONFIG = {
    "host": "localhost",
    "database": "Mymovie",
    "user": "postgres",
    "password": "Wben2003",
    "port": "5432"
}

# Use the new CSV file with the full details.
MOVIES_CSV = r"C:\Users\walid\OneDrive\Bureau\New_Pfa\movie-recommender\data\movies_full_clean.csv"

def import_movies():
    engine = create_engine(
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )

    try:
        movies_df = pd.read_csv(MOVIES_CSV)
        movies_df = movies_df.rename(columns={"movieId": "movie_id"})  # Adjust if needed
        
        # (Optional) Clean genres column if needed.
        movies_df['genres'] = movies_df['genres'].str.strip("[]'").str.replace("', '", ", ")

        # Replace the existing table data
        movies_df.to_sql(
            name='movies',
            con=engine,
            if_exists='replace',  # This replaces the table with new data.
            index=False,
            method='multi'
        )
        print(f"Inserted {len(movies_df)} movies successfully!")
    
    except SQLAlchemyError as e:
        print(f"Database Error: {str(e)}")
    except Exception as e:
        print(f"General Error: {str(e)}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    import_movies()

