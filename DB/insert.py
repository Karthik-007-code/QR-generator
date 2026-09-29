import sqlite3
from DB.conn import get_connection
from fastapi import HTTPException

def insertion(user):
    try:
        db_conn = get_connection()
        cursor = db_conn.cursor()
        cursor.execute(
            "INSERT INTO users(fullname, email, password) VALUES (?,?,?)",
            (user.fullname, user.email, user.password)
        )
        db_conn.commit()
        db_conn.close()
        return {
            "message": "successfully inserted",
            "status": "200"
        }

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")