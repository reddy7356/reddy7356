# How to Add Case Reports to Your Medical RAG System

This guide explains how to add multiple medical case reports to your Haystack RAG system.

## Quick Start

### Method 1: Using the Helper Script (Recommended)

1. **Run the helper script:**
   ```bash
   python add_case_report.py
   ```

2. **Follow the prompts:**
   - Choose option 1 to add a new case report
   - Enter the path to your case report file
   - Enter a name for the case report (or press Enter to use the filename)

3. **The script will:**
   - Copy your case report to the `case_reports/` directory
   - Update the configuration file automatically
   - Verify the file was added successfully

### Method 2: Manual Configuration

1. **Copy your case report to the case_reports directory:**
   ```bash
   mkdir -p case_reports
   cp /path/to/your/case/report.txt case_reports/
   ```

2. **Edit the configuration file:**
   ```bash
   nano case_reports_config.json
   ```

3. **Add your case report to the JSON:**
   ```json
   {
     "Case Trial 1": "/Users/saiofocalallc/clinical insight bot/Case Trial.txt",
     "Your Case Name": "case_reports/your_case_report.txt"
   }
   ```

## File Requirements

### Supported Formats
- **Text files** (.txt) - Most common
- **Plain text content** - No special formatting required

### Encoding Support
The system automatically handles different file encodings:
- UTF-8
- Latin-1
- CP1252
- ISO-8859-1

### Content Guidelines
- **Medical case reports** in plain text format
- **Paragraphs separated by double line breaks** for optimal chunking
- **Standard medical terminology** for better retrieval

## Testing Your Setup

### 1. Check Configuration
```bash
python add_case_report.py
# Choose option 2 to list existing case reports
```

### 2. Test Multi-Case System
```bash
python multi_case_rag.py
```

### 3. Query Specific Questions
```bash
python query_multiple_cases.py "What types of complications are mentioned across the cases?"
```

## Example Workflow

### Adding Your First Additional Case Report

1. **Prepare your case report file** (e.g., `my_case_report.txt`)

2. **Add it to the system:**
   ```bash
   python add_case_report.py
   # Enter: 1
   # Enter: /path/to/my_case_report.txt
   # Enter: My Medical Case
   # Enter: 3 (to exit)
   ```

3. **Test the system:**
   ```bash
   python multi_case_rag.py
   ```

4. **Query across all cases:**
   ```bash
   python query_multiple_cases.py "What treatments were used across all cases?"
   ```

## Configuration File Structure

The `case_reports_config.json` file contains:
```json
{
  "Case Name 1": "/full/path/to/case1.txt",
  "Case Name 2": "case_reports/case2.txt",
  "Case Name 3": "/another/path/case3.txt"
}
```

## Troubleshooting

### Common Issues

1. **File not found error:**
   - Check the file path is correct
   - Ensure the file exists and is readable

2. **Encoding errors:**
   - The system automatically tries multiple encodings
   - If all fail, check your file format

3. **Configuration not updated:**
   - Run `python add_case_report.py` again
   - Check the `case_reports_config.json` file manually

### Verification Steps

1. **Check file exists:**
   ```bash
   ls -la case_reports/
   ```

2. **Check configuration:**
   ```bash
   cat case_reports_config.json
   ```

3. **Test loading:**
   ```bash
   python multi_case_rag.py
   ```

## Advanced Usage

### Querying Specific Cases

You can modify the configuration to query only specific cases:

```python
# In your script
specific_cases = {
    "Case Trial 1": "/Users/saiofocalallc/clinical insight bot/Case Trial.txt"
}
answer = query_multiple_cases(question, specific_cases)
```

### Batch Adding Multiple Cases

For adding many case reports at once:

```bash
# Create a script to add multiple files
for file in /path/to/case/reports/*.txt; do
    echo "1" | python add_case_report.py
    echo "$file"
    echo "Case $(basename $file .txt)"
    echo "3"
done
```

## Best Practices

1. **Use descriptive case names** for easy identification
2. **Keep case reports in a dedicated directory** for organization
3. **Regularly backup your configuration file**
4. **Test the system** after adding new cases
5. **Use consistent file naming** conventions

## Support

If you encounter issues:
1. Check the file paths and permissions
2. Verify the file format and encoding
3. Test with a simple case report first
4. Review the error messages for specific guidance
