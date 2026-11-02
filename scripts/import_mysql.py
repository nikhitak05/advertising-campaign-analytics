"""Transactional, idempotent import. Never deletes unrelated database rows."""
import argparse
from decimal import Decimal
import os
from reporting import ROOT, load_validated


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    df = load_validated()
    if args.dry_run:
        print(f'Validated {len(df)} rows; no database connection attempted.')
        return
    import pandas as pd
    import mysql.connector
    from dotenv import load_dotenv
    load_dotenv(ROOT / '.env')
    db = os.getenv('MYSQL_DATABASE','advertising_analytics')
    if db != 'advertising_analytics':
        raise ValueError('MYSQL_DATABASE must be advertising_analytics to match SQL scripts')
    connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST','127.0.0.1'),
        port=int(os.getenv('MYSQL_PORT','3306')),user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],database=db, autocommit=False)
    try:
        cursor = connection.cursor()
        cursor.execute("SET SESSION sql_mode = 'STRICT_ALL_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'")
        columns = list(df.columns)
        numeric = [c for c in columns if c not in ('ad_group','month','reporting_month')]
        rows = []
        for row in df.to_dict('records'):
            rows.append(tuple(None if pd.isna(row[c]) else
                pd.Timestamp(row[c]).date() if c=='reporting_month' else
                Decimal(str(row[c])) if c in numeric else row[c] for c in columns))
        names = ','.join(f'`{c}`' for c in columns)
        updates = ','.join(f'`{c}`=VALUES(`{c}`)' for c in columns if c not in ('ad_group','reporting_month'))
        cursor.executemany(f'INSERT INTO campaign_performance ({names}) VALUES ({",".join(["%s"]*len(columns))}) ON DUPLICATE KEY UPDATE {updates}', rows)
        if cursor.fetchwarnings():
            raise ValueError('MySQL emitted warnings; rolling back import')
        cursor.execute(f'SELECT {names} FROM campaign_performance ORDER BY reporting_month,ad_group')
        actual = cursor.fetchall()
        if len(actual) != len(rows):
            raise ValueError('Database row count differs; unrelated rows were not deleted')
        for got, expected in zip(actual, rows):
            for c, a, b in zip(columns, got, expected):
                if a is None or b is None:
                    assert a is None and b is None, c
                elif c in numeric:
                    assert abs(Decimal(str(a))-b) <= Decimal('0.000000001'), c
                else:
                    assert a == b, c
        connection.commit()
        print('Committed and verified all 190 rows, every column, against cleaned CSV.')
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

if __name__ == '__main__':
    main()
