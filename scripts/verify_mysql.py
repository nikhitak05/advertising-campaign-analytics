"""Run existing SQL, import twice, and verify live MySQL against independent CSV totals.
Requires a configured local account; creates project objects but never drops tables.
"""
import csv
from collections import defaultdict
from decimal import Decimal
import json
import os
from pathlib import Path
import subprocess
import sys
import mysql.connector
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
MEASURES = ['impressions','clicks','conversions','cost','revenue','sale_amount']
RATIOS = {'ctr':('clicks','impressions'), 'conversion_rate':('conversions','clicks'),
          'cpc':('cost','clicks'), 'cpa':('cost','conversions'), 'roas':('revenue','cost')}

def expected(rows):
    result = {c:sum((Decimal(r[c]) for r in rows),Decimal(0)) for c in MEASURES}
    result.update({c:result[n]/result[d] if result[d] else None for c,(n,d) in RATIOS.items()})
    result['profit_loss'] = result['revenue']-result['cost']
    return result

def compare(actual, wanted):
    for key,value in wanted.items():
        got = actual[key]
        if value is None:
            if got is not None: raise ValueError(f'{key}: expected NULL')
        elif got is None or abs(Decimal(str(got))-value)>Decimal('0.000000001'):
            raise ValueError(f'{key}: database/CSV mismatch')

def run_file(cursor, name):
    # These four repository files contain only line comments and simple statements.
    text = '\n'.join(line.split('--',1)[0] for line in (ROOT/'sql'/name).read_text().splitlines())
    results = []
    for statement in text.split(';'):
        if statement.strip():
            cursor.execute(statement)
            if cursor.with_rows:
                results.append(cursor.fetchall())
    return results

def main():
    load_dotenv(ROOT/'.env')
    required = ['MYSQL_USER','MYSQL_PASSWORD']
    if any(not os.getenv(k) or os.getenv(k)=='replace_me' for k in required):
        raise SystemExit('Configure MYSQL_USER and MYSQL_PASSWORD privately in .env; see reports/mysql_setup.md')
    if os.getenv('MYSQL_DATABASE','advertising_analytics')!='advertising_analytics':
        raise SystemExit('MYSQL_DATABASE must be advertising_analytics')
    connection = mysql.connector.connect(host=os.getenv('MYSQL_HOST','127.0.0.1'),
        port=int(os.getenv('MYSQL_PORT','3306')),user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],connection_timeout=5,autocommit=True)
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT VERSION() AS version')
        version = cursor.fetchone()['version']
        run_file(cursor,'01_create_tables.sql')
        for _ in range(2):
            subprocess.run([sys.executable,str(ROOT/'scripts/import_mysql.py')],check=True,cwd=ROOT)
        run_file(cursor,'04_reporting_views.sql')
        validation = run_file(cursor,'02_data_validation.sql')
        if validation[0] != [{'records':190,'ad_groups':40,'months':5}]:
            raise ValueError('Database cardinality mismatch')
        wanted_months = {'2021-07-01':38,'2021-08-01':38,'2021-09-01':38,'2021-10-01':37,'2021-11-01':39}
        if {str(r['reporting_month']):r['records'] for r in validation[1]} != wanted_months:
            raise ValueError('Monthly counts mismatch')
        if any(validation[i] for i in (2,3,4)):
            raise ValueError('SQL validation returned exception rows')
        analysis = run_file(cursor,'03_kpi_analysis.sql')
        with (ROOT/'data/processed/advertising_campaigns_clean.csv').open() as stream:
            rows = list(csv.DictReader(stream))
        totals = expected(rows)
        compare(analysis[0][0],totals)
        for key in MEASURES: compare(validation[-1][0],{key:totals[key]})
        for key,view in [('reporting_month','vw_monthly_kpis'),('ad_group','vw_ad_group_kpis')]:
            grouped = defaultdict(list)
            for row in rows: grouped[row[key]].append(row)
            cursor.execute(f'SELECT * FROM {view}')
            actual = cursor.fetchall()
            if len(actual)!=len(grouped):raise ValueError(f'{view}: row count mismatch')
            for record in actual:
                source = grouped[str(record[key])]
                compare(record,expected(source))
                if record['record_count']!=len(source):raise ValueError('View record count mismatch')
        cursor.execute('SELECT COUNT(*) AS n FROM vw_campaign_month')
        if cursor.fetchone()['n']!=190:raise ValueError('Detail view cardinality mismatch')
        cursor.execute('SELECT COUNT(*) AS n FROM campaign_performance WHERE cpa IS NULL')
        if cursor.fetchone()['n']!=7:raise ValueError('CPA NULL count mismatch')
        report = {'status':'PASS','server_version':version,'records':190,
            'import_runs':2,'validation_exception_rows':0,'summary_rows_compared':45,
            'analysis_result_sets':len(analysis),'totals':totals,
            'validation_results':validation,'analysis_results':analysis}
        (ROOT/'reports/mysql_validation.json').write_text(json.dumps(report,default=str,indent=2)+'\n')
        print('PASS: live imports, all SQL files, views, and independent KPI comparisons. Evidence: reports/mysql_validation.json')
    finally:
        connection.close()

if __name__=='__main__':
    main()
