import dataiku
import json
from datetime import datetime
import logging
from typing import Dict, List, Any

class DataLineageTracker:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.lineage_store = dataiku.Dataset("data_lineage")
        
    def track_dataset_creation(self, dataset_name: str, source_datasets: List[str], 
                             transformation_type: str, parameters: Dict[str, Any]):
        """Track the creation of a new dataset"""
        lineage_record = {
            'dataset_name': dataset_name,
            'source_datasets': source_datasets,
            'transformation_type': transformation_type,
            'parameters': parameters,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0'  # Can be made dynamic based on versioning system
        }
        
        self._save_lineage_record(lineage_record)
        return lineage_record
    
    def track_dataset_modification(self, dataset_name: str, modification_type: str,
                                 changes: Dict[str, Any]):
        """Track modifications to an existing dataset"""
        modification_record = {
            'dataset_name': dataset_name,
            'modification_type': modification_type,
            'changes': changes,
            'timestamp': datetime.now().isoformat()
        }
        
        self._save_lineage_record(modification_record)
        return modification_record
    
    def get_dataset_lineage(self, dataset_name: str) -> List[Dict[str, Any]]:
        """Retrieve the lineage history for a dataset"""
        df = self.lineage_store.get_dataframe()
        return df[df['dataset_name'] == dataset_name].to_dict('records')
    
    def get_upstream_dependencies(self, dataset_name: str) -> List[str]:
        """Get all upstream dependencies for a dataset"""
        lineage = self.get_dataset_lineage(dataset_name)
        dependencies = set()
        
        for record in lineage:
            if 'source_datasets' in record:
                dependencies.update(record['source_datasets'])
        
        return list(dependencies)
    
    def get_downstream_dependencies(self, dataset_name: str) -> List[str]:
        """Get all downstream dependencies for a dataset"""
        df = self.lineage_store.get_dataframe()
        downstream = set()
        
        for _, row in df.iterrows():
            if 'source_datasets' in row and dataset_name in row['source_datasets']:
                downstream.add(row['dataset_name'])
        
        return list(downstream)
    
    def _save_lineage_record(self, record: Dict[str, Any]):
        """Save a lineage record to the lineage store"""
        try:
            current_data = self.lineage_store.get_dataframe()
            new_record = pd.DataFrame([record])
            updated_data = pd.concat([current_data, new_record], ignore_index=True)
            self.lineage_store.write_with_schema(updated_data)
        except Exception as e:
            self.logger.error(f"Error saving lineage record: {str(e)}")
            raise

def main():
    # Example usage
    lineage_tracker = DataLineageTracker()
    
    # Track dataset creation
    lineage_tracker.track_dataset_creation(
        dataset_name="processed_transactions",
        source_datasets=["raw_transactions", "customer_data"],
        transformation_type="join",
        parameters={
            "join_type": "left",
            "join_columns": ["customer_id"]
        }
    )
    
    # Track dataset modification
    lineage_tracker.track_dataset_modification(
        dataset_name="processed_transactions",
        modification_type="column_addition",
        changes={
            "new_columns": ["risk_score", "fraud_probability"],
            "calculation_method": "ml_model_prediction"
        }
    )
    
    # Get lineage information
    lineage = lineage_tracker.get_dataset_lineage("processed_transactions")
    upstream = lineage_tracker.get_upstream_dependencies("processed_transactions")
    downstream = lineage_tracker.get_downstream_dependencies("processed_transactions")
    
    logging.info(f"Lineage: {lineage}")
    logging.info(f"Upstream dependencies: {upstream}")
    logging.info(f"Downstream dependencies: {downstream}")

if __name__ == "__main__":
    main() 