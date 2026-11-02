"""Validate the existing export, reproduce notebook logic, and export weighted KPIs."""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MEASURES = ['impressions', 'clicks', 'conversions', 'cost', 'revenue', 'sale_amount']
RATIOS = {'ctr': ('clicks', 'impressions'), 'conversion_rate': ('conversions', 'clicks'),
          'cpc': ('cost', 'clicks'), 'cpa': ('cost', 'conversions'), 'roas': ('revenue', 'cost')}

def metrics(frame):
    result = frame.copy()
    for name, (num, den) in RATIOS.items():
        result[name] = result[num] / result[den].replace(0, np.nan)
    result['profit_loss'] = result.revenue - result.cost
    return result

def load_validated():
    df = pd.read_csv(ROOT / 'data/processed/advertising_campaigns_clean.csv')
    assert len(df) == 190 and df.ad_group.nunique() == 40
    assert not df.duplicated(['ad_group', 'reporting_month']).any()
    assert df.ad_group.str.strip().ne('').all()
    assert df[MEASURES].notna().all().all()
    assert np.isfinite(df[MEASURES]).all().all()
    assert (df[['impressions','clicks','conversions','cost','revenue']] >= 0).all().all()
    for c in ['impressions','clicks','conversions']:
        assert (df[c] % 1 == 0).all()
    assert (df.clicks <= df.impressions).all()
    dates = pd.to_datetime(df.reporting_month, format='%Y-%m-%d')
    assert (dates.dt.day == 1).all()
    assert (dates.dt.strftime('%B') == df.month).all()
    expected = {'2021-07-01':38,'2021-08-01':38,'2021-09-01':38,'2021-10-01':37,'2021-11-01':39}
    assert df.groupby('reporting_month').size().to_dict() == expected
    recomputed = metrics(df)
    for c in [*RATIOS, 'profit_loss']:
        np.testing.assert_allclose(df[c], recomputed[c], atol=1e-10, rtol=1e-10, equal_nan=True)
    raw = pd.read_csv(ROOT / 'data/raw/final_shop_6modata.csv')
    raw.columns = raw.columns.str.strip().str.lower().str.replace(' ', '_')
    raw = raw.rename(columns={'ctr':'source_ctr','conv_rate':'source_conversion_rate',
                              'cpc':'source_cpc','p&l':'source_profit_loss'})
    raw['reporting_month'] = pd.to_datetime(raw.month + ' 2021', format='%B %Y').dt.strftime('%Y-%m-%d')
    reconstructed = metrics(raw)[df.columns].sort_values(['reporting_month','ad_group']).reset_index(drop=True)
    pd.testing.assert_frame_equal(df, reconstructed, check_dtype=False, atol=1e-10, rtol=1e-10)
    return df

def aggregate(df, key):
    return metrics(df.groupby(key, as_index=False)[MEASURES].sum())

def main():
    df = load_validated()
    out = ROOT / 'tableau'
    out.mkdir(exist_ok=True)
    df.to_csv(out / 'tableau_campaign_month.csv', index=False)
    monthly = aggregate(df, 'reporting_month')
    groups = aggregate(df, 'ad_group')
    monthly.to_csv(out / 'tableau_monthly_kpis.csv', index=False)
    groups.to_csv(out / 'tableau_ad_group_kpis.csv', index=False)
    total = metrics(pd.DataFrame([df[MEASURES].sum()])).iloc[0].to_dict()
    report = {'status':'PASS: local CSV and notebook-logic parity; MySQL not executed',
              'records':len(df),'ad_groups':int(df.ad_group.nunique()),
              'monthly_records':df.groupby('reporting_month').size().to_dict(),
              'totals':total,'undefined_ratios':df[list(RATIOS)].isna().sum().to_dict(),
              'source_max_absolute_differences':{s:float((df[s]-df[t]).abs().max()) for s,t in
              [('source_ctr','ctr'),('source_conversion_rate','conversion_rate'),('source_cpc','cpc'),('source_profit_loss','profit_loss')]}}
    (ROOT / 'reports/validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
