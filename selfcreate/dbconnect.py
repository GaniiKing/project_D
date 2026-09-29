
import os
import psycopg2
from typing import Any


def run_query(
    query: str,
    host: str = "localhost",
    database: str = "postgres",
    user: str = "postgres",
    password: str = "2660",
    port: int = 5432,
    readonly_only: bool = False,
) -> dict[str, Any] | None:

    if not query or not query.strip():
        print("Empty query.")
        return None

    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password or os.getenv("PG_PASSWORD", "2660"),
            port=port,
        )

        cursor = conn.cursor()

        # Execute the supplied SQL
        cursor.execute(query)

        # Return rows for SELECT or other queries with results
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            result = {
                "success": True,
                "type": "rows",
                "data": [
                    dict(zip(columns, row))
                    for row in rows
                ],
                "row_count": len(rows),
            }
        else:
            result = {
                "success": True,
                "type": "command",
                "message": "Query executed successfully.",
                "affected_rows": cursor.rowcount,
            }

        # Commit database changes
        conn.commit()
        return result

    except Exception as e:
        if conn:
            conn.rollback()

        print("Database error:", e)
        return {
            "success": False,
            "error": str(e),
        }

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


