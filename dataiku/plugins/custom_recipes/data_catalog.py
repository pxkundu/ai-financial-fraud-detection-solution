import dataiku
import pandas as pd
from datetime import datetime
import logging
from typing import Dict, List, Any, Optional

class DataCatalog:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.catalog_store = dataiku.Dataset("data_catalog")
        
    def register_dataset(self, dataset_name: str, description: str, 
                        owner: str, tags: List[str], schema: Dict[str, Any],
                        sensitivity_level: str = "public"):
        """Register a new dataset in the catalog"""
        catalog_entry = {
            'dataset_name': dataset_name,
            'description': description,
            'owner': owner,
            'tags': tags,
            'schema': schema,
            'sensitivity_level': sensitivity_level,
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        
        self._save_catalog_entry(catalog_entry)
        return catalog_entry
    
    def update_dataset_metadata(self, dataset_name: str, 
                              updates: Dict[str, Any]):
        """Update metadata for an existing dataset"""
        current_entry = self._get_dataset_entry(dataset_name)
        if current_entry is None:
            raise ValueError(f"Dataset {dataset_name} not found in catalog")
        
        current_entry.update(updates)
        current_entry['last_updated'] = datetime.now().isoformat()
        
        self._save_catalog_entry(current_entry)
        return current_entry
    
    def get_dataset_metadata(self, dataset_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve metadata for a dataset"""
        return self._get_dataset_entry(dataset_name)
    
    def search_datasets(self, query: str, tags: List[str] = None,
                       sensitivity_level: str = None) -> List[Dict[str, Any]]:
        """Search for datasets based on various criteria"""
        df = self.catalog_store.get_dataframe()
        
        # Apply filters
        if tags:
            df = df[df['tags'].apply(lambda x: all(tag in x for tag in tags))]
        if sensitivity_level:
            df = df[df['sensitivity_level'] == sensitivity_level]
        
        # Text search
        if query:
            mask = (
                df['dataset_name'].str.contains(query, case=False) |
                df['description'].str.contains(query, case=False)
            )
            df = df[mask]
        
        return df.to_dict('records')
    
    def get_dataset_schema(self, dataset_name: str) -> Optional[Dict[str, Any]]:
        """Get the schema for a specific dataset"""
        entry = self._get_dataset_entry(dataset_name)
        return entry.get('schema') if entry else None
    
    def _get_dataset_entry(self, dataset_name: str) -> Optional[Dict[str, Any]]:
        """Get a single dataset entry from the catalog"""
        df = self.catalog_store.get_dataframe()
        matches = df[df['dataset_name'] == dataset_name]
        return matches.iloc[0].to_dict() if not matches.empty else None
    
    def _save_catalog_entry(self, entry: Dict[str, Any]):
        """Save or update a catalog entry"""
        try:
            current_data = self.catalog_store.get_dataframe()
            
            # Check if entry exists
            mask = current_data['dataset_name'] == entry['dataset_name']
            if mask.any():
                # Update existing entry
                current_data.loc[mask] = pd.Series(entry)
            else:
                # Add new entry
                new_entry = pd.DataFrame([entry])
                current_data = pd.concat([current_data, new_entry], ignore_index=True)
            
            self.catalog_store.write_with_schema(current_data)
        except Exception as e:
            self.logger.error(f"Error saving catalog entry: {str(e)}")
            raise

def main():
    # Example usage
    catalog = DataCatalog()
    
    # Register a new dataset
    catalog.register_dataset(
        dataset_name="fraud_transactions",
        description="Dataset containing fraudulent transaction records",
        owner="fraud_team",
        tags=["fraud", "transactions", "risk"],
        schema={
            "columns": [
                {"name": "transaction_id", "type": "string"},
                {"name": "amount", "type": "float"},
                {"name": "timestamp", "type": "datetime"}
            ]
        },
        sensitivity_level="confidential"
    )
    
    # Update dataset metadata
    catalog.update_dataset_metadata(
        dataset_name="fraud_transactions",
        updates={
            "description": "Updated description for fraud transactions dataset",
            "tags": ["fraud", "transactions", "risk", "ml_training"]
        }
    )
    
    # Search for datasets
    results = catalog.search_datasets(
        query="fraud",
        tags=["risk"],
        sensitivity_level="confidential"
    )
    
    # Get dataset schema
    schema = catalog.get_dataset_schema("fraud_transactions")
    
    logging.info(f"Search results: {results}")
    logging.info(f"Schema: {schema}")

if __name__ == "__main__":
    main() 