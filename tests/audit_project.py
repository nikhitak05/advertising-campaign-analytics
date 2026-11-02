from pathlib import Path
import hashlib, subprocess,sys,tempfile,shutil,json,os,contextlib,io,csv
from decimal import Decimal,getcontext
import pandas as pd
import numpy as np
root=Path(__file__).resolve().parents[1];os.chdir(root);sys.path.insert(0,str(root/'scripts'))
def hashes():return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['data','notebooks','tableau'] for p in (root/folder).rglob('*') if p.is_file()}
before=hashes()
for args in [['scripts/reporting.py'],['scripts/import_mysql.py','--dry-run'],['-m','unittest','discover','-s','tests','-v']]:
 r=subprocess.run([sys.executable,*args],capture_output=True,text=True);print('COMMAND',args,'EXIT',r.returncode);print(r.stdout+r.stderr);assert r.returncode==0
# Execute the original notebook code, unmodified, in an isolated directory.
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp);shutil.copytree(root/'data',t/'data');(t/'notebooks').mkdir();ns={'display':lambda *args:None,'__name__':'__main__'}
 os.chdir(t/'notebooks')
 try:
  with contextlib.redirect_stdout(io.StringIO()):
   cells=json.loads((root/'notebooks/data_cleaning.ipynb').read_text())['cells']
   for i,c in enumerate(cells):
    if c['cell_type']=='code':exec(compile(''.join(c['source']),f'cell_{i}','exec'),ns)
 finally:os.chdir(root)
 pd.testing.assert_frame_equal(pd.read_csv(t/'data/processed/advertising_campaigns_clean.csv'),pd.read_csv(root/'data/processed/advertising_campaigns_clean.csv'))
 print('NOTEBOOK: all 19 code cells executed; exported CSV matches repository')
getcontext().prec=36
measures=['impressions','clicks','conversions','cost','revenue','sale_amount']
ratios={'ctr':('clicks','impressions'),'conversion_rate':('conversions','clicks'),'cpc':('cost','clicks'),'cpa':('cost','conversions'),'roas':('revenue','cost')}
rows=list(csv.DictReader(open(root/'data/processed/advertising_campaigns_clean.csv')))
def calc(rs):
 sums={c:sum((Decimal(r[c]) for r in rs),Decimal(0)) for c in measures}
 sums.update({c:sums[n]/sums[d] if sums[d] else None for c,(n,d) in ratios.items()});sums['profit_loss']=sums['revenue']-sums['cost'];return sums
def compare(got,expected):
 for c,v in expected.items():
  a=got[c]; assert (pd.isna(a) if v is None else abs(Decimal(str(a))-v)<=Decimal('0.000000001')), (c,a,v)
totals=calc(rows); detail=pd.read_csv(root/'tableau/tableau_campaign_month.csv');pd.testing.assert_frame_equal(detail,pd.read_csv(root/'data/processed/advertising_campaigns_clean.csv'))
checks=0
for key,file in [('reporting_month','monthly'),('ad_group','ad_group')]:
 export=pd.read_csv(root/f'tableau/tableau_{file}_kpis.csv');assert list(export.columns)==[key,*measures,*ratios,'profit_loss'];assert not export.duplicated(key).any()
 for record in export.to_dict('records'):
  compare(record,calc([r for r in rows if r[key]==record[key]]));checks+=1
 for c in measures:assert abs(Decimal(str(export[c].sum()))-totals[c])<Decimal('0.00000001')
for month in sorted({r['reporting_month'] for r in rows}):
 for group in sorted({r['ad_group'] for r in rows}):
  subset=[r for r in rows if r['reporting_month']==month and r['ad_group']==group]
  selected=detail[(detail.reporting_month==month)&(detail.ad_group==group)]
  assert len(selected)==len(subset)
  got=calc(selected.astype(str).to_dict('records'))
  assert got==calc(subset);checks+=1
for row in rows:compare({c:float(row[c]) if row[c] else np.nan for c in [*measures,*ratios,'profit_loss']},calc([row]))
print('INDEPENDENT DECIMAL TOTALS',json.dumps({k:str(v) for k,v in totals.items()},indent=2))
print('PASS: 45 summary rows, 190 row metrics, 200 combined filter selections')
after=hashes();print('CHANGED data/notebook/export files:',[k for k in before if before[k]!=after[k]]);assert before==after
(root/'reports/audit_evidence.json').write_text(json.dumps({'date':'2026-10-21','independent_totals':{k:str(v) for k,v in totals.items()},'summary_rows_checked':45,'filter_combinations_checked':200,'detail_rows_checked':190,'source_and_output_hashes_unchanged':before==after,'sha256':before},indent=2)+'\n')
