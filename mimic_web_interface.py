#!/usr/bin/env python3
"""
MIMIC IV Patient Query Web Interface
Flask-based web interface for querying MIMIC IV patients
"""

from flask import Flask, render_template, request, jsonify
import json
from mimic_patient_query_system import MIMICQueryInterface
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global interface instance
interface = None

def init_interface():
    """Initialize the MIMIC interface"""
    global interface
    if interface is None:
        logger.info("Initializing MIMIC interface...")
        interface = MIMICQueryInterface()
        logger.info("MIMIC interface initialized!")

@app.route('/')
def index():
    """Main page"""
    init_interface()
    stats = interface.get_database_stats()
    return render_template('index.html', stats=stats)

@app.route('/api/search', methods=['POST'])
def api_search():
    """API endpoint for searching patients"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        patient_ids = data.get('patient_ids', None)
        categories = data.get('categories', None)
        max_results = data.get('max_results', 10)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        results = interface.search(query, patient_ids, categories, max_results)
        
        # Convert results to JSON-serializable format
        search_results = []
        for result in results:
            search_results.append({
                'patient_id': result.patient_id,
                'relevance_score': result.relevance_score,
                'matched_sections': result.matched_sections,
                'matched_keywords': result.matched_keywords,
                'context': result.context,
                'metadata': result.metadata
            })
        
        return jsonify({
            'results': search_results,
            'total_results': len(search_results),
            'query': query
        })
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/patient/<patient_id>')
def api_patient_info(patient_id):
    """API endpoint for getting patient information"""
    try:
        info = interface.get_patient_info(patient_id)
        if not info:
            return jsonify({'error': 'Patient not found'}), 404
        
        return jsonify(info)
        
    except Exception as e:
        logger.error(f"Patient info error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients')
def api_patients():
    """API endpoint for listing patients"""
    try:
        limit = request.args.get('limit', 20, type=int)
        patients = interface.list_patients(limit)
        return jsonify({'patients': patients, 'total': len(interface.indexer.patients)})
        
    except Exception as e:
        logger.error(f"Patients list error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def api_stats():
    """API endpoint for database statistics"""
    try:
        stats = interface.get_database_stats()
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory and HTML template
    import os
    os.makedirs('templates', exist_ok=True)
    
    # Create the HTML template
    html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MIMIC IV Patient Query System</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .search-section {
            background: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #34495e;
        }
        input[type="text"], select, textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            font-size: 14px;
        }
        button {
            background: #3498db;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin-right: 10px;
        }
        button:hover {
            background: #2980b9;
        }
        .results {
            margin-top: 30px;
        }
        .result-item {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .patient-id {
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
        }
        .score {
            background: #e74c3c;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
        }
        .metadata {
            color: #7f8c8d;
            font-size: 14px;
            margin-bottom: 10px;
        }
        .keywords {
            margin: 10px 0;
        }
        .keyword {
            background: #3498db;
            color: white;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 12px;
            margin-right: 5px;
            display: inline-block;
        }
        .context {
            background: white;
            padding: 15px;
            border-radius: 4px;
            border-left: 4px solid #3498db;
            margin-top: 10px;
            font-style: italic;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-number {
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }
        .stat-label {
            color: #7f8c8d;
            margin-top: 5px;
        }
        .loading {
            text-align: center;
            padding: 20px;
            color: #7f8c8d;
        }
        .error {
            background: #e74c3c;
            color: white;
            padding: 15px;
            border-radius: 4px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏥 MIMIC IV Patient Query System</h1>
        
        <div class="stats" id="stats">
            <div class="stat-card">
                <div class="stat-number">{{ stats.total_patients }}</div>
                <div class="stat-label">Total Patients</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.total_keywords }}</div>
                <div class="stat-label">Keywords</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.total_medical_terms }}</div>
                <div class="stat-label">Medical Terms</div>
            </div>
        </div>
        
        <div class="search-section">
            <h2>🔍 Search Patients</h2>
            <form id="searchForm">
                <div class="form-group">
                    <label for="query">Search Query:</label>
                    <input type="text" id="query" name="query" placeholder="e.g., coronary artery disease, diabetes, chest pain" required>
                </div>
                
                <div class="form-group">
                    <label for="patientIds">Specific Patient IDs (optional):</label>
                    <input type="text" id="patientIds" name="patientIds" placeholder="e.g., 10019957,10023771">
                    <small>Leave empty to search all patients</small>
                </div>
                
                <div class="form-group">
                    <label for="categories">Medical Categories (optional):</label>
                    <select id="categories" name="categories" multiple>
                        <option value="diagnoses">Diagnoses</option>
                        <option value="procedures">Procedures</option>
                        <option value="medications">Medications</option>
                        <option value="vitals">Vitals</option>
                        <option value="lab_values">Lab Values</option>
                        <option value="symptoms">Symptoms</option>
                    </select>
                    <small>Hold Ctrl/Cmd to select multiple categories</small>
                </div>
                
                <div class="form-group">
                    <label for="maxResults">Max Results:</label>
                    <input type="number" id="maxResults" name="maxResults" value="10" min="1" max="50">
                </div>
                
                <button type="submit">Search</button>
                <button type="button" onclick="clearResults()">Clear Results</button>
            </form>
        </div>
        
        <div id="results" class="results"></div>
    </div>

    <script>
        document.getElementById('searchForm').addEventListener('submit', function(e) {
            e.preventDefault();
            performSearch();
        });

        function performSearch() {
            const query = document.getElementById('query').value;
            const patientIds = document.getElementById('patientIds').value;
            const categories = Array.from(document.getElementById('categories').selectedOptions).map(option => option.value);
            const maxResults = document.getElementById('maxResults').value;
            
            if (!query.trim()) {
                alert('Please enter a search query');
                return;
            }
            
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '<div class="loading">Searching...</div>';
            
            const requestData = {
                query: query,
                max_results: parseInt(maxResults)
            };
            
            if (patientIds.trim()) {
                requestData.patient_ids = patientIds.split(',').map(id => id.trim());
            }
            
            if (categories.length > 0) {
                requestData.categories = categories;
            }
            
            fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    resultsDiv.innerHTML = `<div class="error">Error: ${data.error}</div>`;
                } else {
                    displayResults(data);
                }
            })
            .catch(error => {
                resultsDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
            });
        }

        function displayResults(data) {
            const resultsDiv = document.getElementById('results');
            
            if (data.results.length === 0) {
                resultsDiv.innerHTML = '<div class="error">No results found for your query.</div>';
                return;
            }
            
            let html = `<h2>Search Results for "${data.query}" (${data.total_results} results)</h2>`;
            
            data.results.forEach((result, index) => {
                html += `
                    <div class="result-item">
                        <div class="result-header">
                            <div class="patient-id">Patient ${result.patient_id}</div>
                            <div class="score">Score: ${result.relevance_score.toFixed(1)}</div>
                        </div>
                        <div class="metadata">
                            <strong>Service:</strong> ${result.metadata.service || 'Unknown'} | 
                            <strong>Chief Complaint:</strong> ${result.metadata.chief_complaint || 'Unknown'}
                        </div>
                        ${result.matched_keywords.length > 0 ? `
                            <div class="keywords">
                                <strong>Keywords:</strong> 
                                ${result.matched_keywords.slice(0, 10).map(keyword => 
                                    `<span class="keyword">${keyword}</span>`
                                ).join('')}
                            </div>
                        ` : ''}
                        ${result.context ? `
                            <div class="context">
                                <strong>Context:</strong> ${result.context}
                            </div>
                        ` : ''}
                    </div>
                `;
            });
            
            resultsDiv.innerHTML = html;
        }

        function clearResults() {
            document.getElementById('results').innerHTML = '';
            document.getElementById('query').value = '';
            document.getElementById('patientIds').value = '';
            document.getElementById('categories').selectedIndex = -1;
        }
    </script>
</body>
</html>'''
    
    with open('templates/index.html', 'w') as f:
        f.write(html_template)
    
    print("Starting MIMIC IV Patient Query Web Interface...")
    print("Open your browser and go to: http://localhost:8080")
    app.run(debug=True, host='0.0.0.0', port=8080)
