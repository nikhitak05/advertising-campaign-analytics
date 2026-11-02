import sys
from pathlib import Path
import unittest
import pandas as pd
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from reporting import load_validated, aggregate, metrics, MEASURES

class ReportingTests(unittest.TestCase):
    def test_source_and_export_reconciliation(self):
        df = load_validated()
        for key, count in [('reporting_month',5),('ad_group',40)]:
            result = aggregate(df,key)
            self.assertEqual(len(result),count)
            np.testing.assert_allclose(result[MEASURES].sum(), df[MEASURES].sum())
        self.assertEqual(df.cpa.isna().sum(),7)

    def test_weighted_ratios_and_zero_denominators(self):
        df = pd.DataFrame({'group':['a','a','b'],'impressions':[10,1000,0],
            'clicks':[5,10,0],'conversions':[1,0,0],'cost':[10,20,0],
            'revenue':[20,0,0],'sale_amount':[100,0,0]})
        result = aggregate(df,'group').set_index('group')
        self.assertAlmostEqual(result.loc['a','ctr'],15/1010)
        self.assertEqual(result.loc['a','cpa'],30)
        self.assertTrue(result.loc['b',['ctr','conversion_rate','cpc','cpa','roas']].isna().all())
        self.assertEqual(result.loc['b','profit_loss'],0)


class InvalidInputTests(unittest.TestCase):
    def test_invalid_cleaned_values_are_rejected(self):
        from unittest.mock import patch
        import reporting
        original = pd.read_csv(reporting.ROOT / 'data/processed/advertising_campaigns_clean.csv')
        cases = [('impressions',-1),('clicks',-1),('conversions',-1),
                 ('cost',-1),('revenue',-1),('revenue',np.nan),('cost',np.inf),
                 ('ad_group',None),('ad_group',' '),('impressions',1.5),
                 ('clicks',10**9),('reporting_month','2021-07-02'),
                 ('reporting_month','not-a-date'),('ctr',np.nan)]
        for col,value in cases:
            with self.subTest(column=col,value=value):
                bad = original.copy()
                bad[col] = bad[col].astype(object)
                bad.loc[0,col] = value
                with patch.object(reporting.pd,'read_csv',return_value=bad):
                    with self.assertRaises((AssertionError,ValueError,TypeError)):
                        reporting.load_validated()
        bad=original.copy();bad.iloc[1]=bad.iloc[0]
        with patch.object(reporting.pd,'read_csv',return_value=bad):
            with self.assertRaises(AssertionError):reporting.load_validated()

if __name__ == '__main__':
    unittest.main()
