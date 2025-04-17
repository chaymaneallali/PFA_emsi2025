import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

DB_CONFIG = {
    "host": "localhost",
    "database": "Mymovie",
    "user": "postgres",
    "password": "Wben2003",
    "port": "5432"
}

RATINGS_CSV = "ratings.csv"
TAGS_CSV = "tags.csv"

def import_ratings_tags():
    engine = create_engine(
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )

    try:
        
        ratings_df = pd.read_csv(RATINGS_CSV)

        
        ratings_df = ratings_df.rename(columns={
            "userId": "user_id",
            "movieId": "movie_id"
        })

        ratings_df["timestamp"] = pd.to_datetime(ratings_df["timestamp"], unit='s')

        ratings_df.to_sql(
            name='ratings',
            con=engine,
            if_exists='append',
            index=False,
            method='multi'
        )
        print(f"Inserted {len(ratings_df)} ratings!")

        tags_df = pd.read_csv(TAGS_CSV)

        tags_df = tags_df.rename(columns={
            "userId": "user_id",
            "movieId": "movie_id"
        })

        tags_df["timestamp"] = pd.to_datetime(tags_df["timestamp"], unit='s')

        tags_df.to_sql(
            name='tags',
            con=engine,
            if_exists='append',
            index=False,
            method='multi'
        )
        print(f"Inserted {len(tags_df)} tags!")

    except SQLAlchemyError as e:
        print(f"Database Error: {str(e)}")
    except Exception as e:
        print(f"General Error: {str(e)}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    import_ratings_tags()