# Data Cleaning Recipe
# Cleans and normalizes OCR output

def clean_ocr_blocks(blocks):
    # Placeholder: implement text normalization, remove noise, handle tables
    cleaned = []
    for block in blocks:
        # Example: remove empty lines, normalize whitespace
        if 'Text' in block and block['Text'].strip():
            cleaned.append(block['Text'].strip())
    return cleaned

def run_cleaning(ocr_results):
    cleaned_results = []
    for result in ocr_results:
        cleaned_text = clean_ocr_blocks(result['blocks'])
        cleaned_results.append({'s3_key': result['s3_key'], 'cleaned_text': cleaned_text})
    return cleaned_results

# Example usage:
# cleaned = run_cleaning(ocr_results)
# print(cleaned) 