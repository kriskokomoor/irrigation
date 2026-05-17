import logging

from .config import (
    IRRIGATION_DBHOST,
    IRRIGATION_DBNAME,
    IRRIGATION_DBPASSWORD,
    IRRIGATION_DBPORT,
    IRRIGATION_DBUSER,
    IRRIGATION_EVENT_LOG_TABLENAME,
    IRRIGATION_SCHEMANAME,
)


def get_conn():
    import psycopg2

    return psycopg2.connect(
        dbname=IRRIGATION_DBNAME,
        user=IRRIGATION_DBUSER,
        password=IRRIGATION_DBPASSWORD,
        host=IRRIGATION_DBHOST,
        port=IRRIGATION_DBPORT,
    )


def qualified_table_name(table_name: str) -> str:
    return f'{IRRIGATION_SCHEMANAME}."{table_name}"'


def create_log_table(cur, log_table: str):
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {log_table} (
            log_id BIGSERIAL PRIMARY KEY,
            event_id BIGINT,
            event_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            zone INTEGER,
            action TEXT,
            success BOOLEAN,
            http_status INTEGER,
            response_body TEXT,
            error_message TEXT
        );
    """)


def log_irrigation_event(
    zone_id: int,
    action: str,
    success: bool,
    response_body: str | None = None,
    error_message: str | None = None,
    event_id: int | None = None,
    http_status: int | None = None,
):
    missing_config = [
        name
        for name, value in (
            ("IRRIGATION_DBNAME", IRRIGATION_DBNAME),
            ("IRRIGATION_DBUSER", IRRIGATION_DBUSER),
            ("IRRIGATION_DBHOST", IRRIGATION_DBHOST),
        )
        if not value
    ]
    if missing_config:
        logging.warning(
            "Irrigation event log skipped; missing database config: %s",
            ", ".join(missing_config),
        )
        return

    try:
        log_table = qualified_table_name(IRRIGATION_EVENT_LOG_TABLENAME)
        with get_conn() as conn:
            with conn.cursor() as cur:
                create_log_table(cur, log_table)
                cur.execute(f"""
                    INSERT INTO {log_table} (
                        event_id, zone, action, success, http_status, response_body, error_message
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    event_id,
                    zone_id,
                    action,
                    success,
                    http_status,
                    response_body,
                    error_message,
                ))
            conn.commit()
    except Exception:
        logging.exception(
            "Failed to log irrigation event: zone=%s action=%s success=%s",
            zone_id,
            action,
            success,
        )
