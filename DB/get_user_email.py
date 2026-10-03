import sqlite3
from DB.conn import get_connection
from fastapi import HTTPException,status

def get_user_db(identifier: str):
    try:
        db_conn = get_connection()
        cursor = db_conn.cursor()
        identifier_clean = identifier.strip().lower()
        query = "SELECT * FROM users WHERE LOWER(email) = ?"
        cursor.execute(query, (identifier_clean,))
        row = cursor.fetchone()
        if row is not None:
            return {
                "user": dict(row),
                "status": status.HTTP_200_OK,
                "message": "user found"
            }
        else:
            return {
                "user": None,
                "status": status.HTTP_404_NOT_FOUND,
                "message": "user not found"
            }

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        if db_conn:
            db_conn.close()


