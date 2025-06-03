import dataiku
import pandas as pd
import numpy as np
from datetime import datetime
import logging

class DataQualityCheck:
    def __init__(self, dataset_name):
        self.dataset = dataiku.Dataset(dataset_name)
        self.logger = logging.getLogger(__name__)
        
    def check_completeness(self, threshold=0.95):
        """Check for missing values in the dataset"""
        df = self.dataset.get_dataframe()
        completeness = {}
        
        for column in df.columns:
            missing_ratio = df[column].isnull().mean()
            completeness[column] = {
                'missing_ratio': missing_ratio,
                'status': 'PASS' if missing_ratio < (1 - threshold) else 'FAIL'
            }
        
        return completeness
    
    def check_consistency(self, rules):
        """Check data consistency based on defined rules"""
        df = self.dataset.get_dataframe()
        consistency = {}
        
        for rule in rules:
            column = rule['column']
            condition = rule['condition']
            result = eval(f"df['{column}'].{condition}")
            consistency[column] = {
                'violations': (~result).sum(),
                'status': 'PASS' if (~result).sum() == 0 else 'FAIL'
            }
        
        return consistency
    
    def check_accuracy(self, reference_data, key_columns):
        """Check data accuracy against reference data"""
        df = self.dataset.get_dataframe()
        ref_df = reference_data.get_dataframe()
        
        accuracy = {}
        for column in key_columns:
            matches = df[column].isin(ref_df[column]).mean()
            accuracy[column] = {
                'match_ratio': matches,
                'status': 'PASS' if matches > 0.95 else 'FAIL'
            }
        
        return accuracy
    
    def check_freshness(self, timestamp_column, max_age_hours=24):
        """Check data freshness based on timestamp"""
        df = self.dataset.get_dataframe()
        current_time = datetime.now()
        
        if timestamp_column in df.columns:
            latest_timestamp = pd.to_datetime(df[timestamp_column]).max()
            age_hours = (current_time - latest_timestamp).total_seconds() / 3600
            
            return {
                'age_hours': age_hours,
                'status': 'PASS' if age_hours <= max_age_hours else 'FAIL'
            }
        
        return {'status': 'ERROR', 'message': 'Timestamp column not found'}
    
    def run_all_checks(self, rules, reference_data=None, key_columns=None):
        """Run all data quality checks"""
        results = {
            'completeness': self.check_completeness(),
            'consistency': self.check_consistency(rules),
            'timestamp': datetime.now().isoformat()
        }
        
        if reference_data and key_columns:
            results['accuracy'] = self.check_accuracy(reference_data, key_columns)
        
        return results

def main():
    # Example usage
    dq_checker = DataQualityCheck('transactions')
    
    rules = [
        {'column': 'amount', 'condition': '>= 0'},
        {'column': 'transaction_date', 'condition': '<= pd.Timestamp.now()'}
    ]
    
    results = dq_checker.run_all_checks(rules)
    
    # Log results
    logging.info(f"Data Quality Check Results: {results}")
    
    return results

if __name__ == "__main__":
    main() 