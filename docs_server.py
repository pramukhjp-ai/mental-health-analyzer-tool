#!/usr/bin/env python3
"""
Mental Health Analyzer - Documentation Server
=============================================

A comprehensive documentation server for the Mental Health Analyzer project.
This server renders markdown documentation with syntax highlighting and serves
it in a beautiful web interface for easy browsing and learning.

Author: Mental Health Analyzer Team
Purpose: Educational documentation for students and developers
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import markdown
import os
import json
from markdown.extensions import codehilite, toc, tables, fenced_code
import pygments
from pygments.formatters import HtmlFormatter

app = Flask(__name__, template_folder='docs/templates')

# Documentation configuration
DOCS_DIR = 'docs'
STATIC_DOCS_DIR = 'docs/static'
TEMPLATES_DOCS_DIR = 'docs/templates'

# Markdown extensions for rich documentation
markdown_extensions = [
    'codehilite',
    'toc',
    'tables',
    'fenced_code',
    'attr_list',
    'def_list',
    'abbr',
    'footnotes',
    'admonition'
]

# Documentation navigation structure
DOCS_NAVIGATION = [
    {
        'title': 'Getting Started',
        'pages': [
            {'name': 'index', 'title': 'Overview', 'file': 'index.md'},
            {'name': 'quick-start', 'title': 'Quick Start Guide', 'file': 'quick-start.md'},
            {'name': 'tech-stack', 'title': 'Technology Stack', 'file': 'tech-stack.md'},
            {'name': 'architecture', 'title': 'System Architecture', 'file': 'architecture.md'}
        ]
    },
    {
        'title': 'Code Documentation',
        'pages': [
            {'name': 'backend-logic', 'title': 'Backend Logic Explained', 'file': 'backend-logic.md'},
            {'name': 'frontend-logic', 'title': 'Frontend Logic Explained', 'file': 'frontend-logic.md'},
            {'name': 'text-analysis', 'title': 'Text Analysis Module', 'file': 'text-analysis.md'},
            {'name': 'voice-analysis', 'title': 'Voice Analysis Module', 'file': 'voice-analysis.md'},
            {'name': 'facial-analysis', 'title': 'Facial Analysis Module', 'file': 'facial-analysis.md'}
        ]
    },
    {
        'title': 'API Reference',
        'pages': [
            {'name': 'api-overview', 'title': 'API Overview', 'file': 'api-overview.md'},
            {'name': 'api-endpoints', 'title': 'API Endpoints', 'file': 'api-endpoints.md'},
            {'name': 'data-models', 'title': 'Data Models', 'file': 'data-models.md'}
        ]
    },
    {
        'title': 'Learning Resources',
        'pages': [
            {'name': 'coding-best-practices', 'title': 'Coding Best Practices', 'file': 'coding-best-practices.md'},
            {'name': 'python-concepts', 'title': 'Python Concepts Used', 'file': 'python-concepts.md'},
            {'name': 'javascript-concepts', 'title': 'JavaScript Concepts Used', 'file': 'javascript-concepts.md'},
            {'name': 'ml-concepts', 'title': 'Machine Learning Concepts', 'file': 'ml-concepts.md'}
        ]
    },
    {
        'title': 'Development Guide',
        'pages': [
            {'name': 'setup-development', 'title': 'Development Setup', 'file': 'setup-development.md'},
            {'name': 'project-structure', 'title': 'Project Structure', 'file': 'project-structure.md'},
            {'name': 'extending-features', 'title': 'Extending Features', 'file': 'extending-features.md'},
            {'name': 'testing-guide', 'title': 'Testing Guide', 'file': 'testing-guide.md'}
        ]
    }
]

def get_all_pages():
    """Get all documentation pages in a flat list"""
    pages = []
    for section in DOCS_NAVIGATION:
        pages.extend(section['pages'])
    return pages

def load_markdown_file(filename):
    """Load and convert markdown file to HTML"""
    filepath = os.path.join(DOCS_DIR, filename)
    if not os.path.exists(filepath):
        return None, None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Convert markdown to HTML with extensions
    md = markdown.Markdown(extensions=markdown_extensions)
    html_content = md.convert(content)
    
    # Extract table of contents if available
    toc = getattr(md, 'toc', '')
    
    return html_content, toc

@app.route('/')
def index():
    """Documentation home page"""
    content, toc = load_markdown_file('index.md')
    if content is None:
        content = "<h1>Welcome to Mental Health Analyzer Documentation</h1><p>Documentation is being set up...</p>"
        toc = ""
    
    return render_template('docs_base.html', 
                         content=content,
                         toc=toc,
                         navigation=DOCS_NAVIGATION,
                         current_page='index',
                         page_title='Mental Health Analyzer Documentation')

@app.route('/docs/<page_name>')
def docs_page(page_name):
    """Serve individual documentation pages"""
    # Find the page in navigation
    current_page = None
    for section in DOCS_NAVIGATION:
        for page in section['pages']:
            if page['name'] == page_name:
                current_page = page
                break
        if current_page:
            break
    
    if not current_page:
        return "Page not found", 404
    
    content, toc = load_markdown_file(current_page['file'])
    if content is None:
        content = f"<h1>{current_page['title']}</h1><p>This page is under construction...</p>"
        toc = ""
    
    return render_template('docs_base.html',
                         content=content,
                         toc=toc,
                         navigation=DOCS_NAVIGATION,
                         current_page=page_name,
                         page_title=current_page['title'])

@app.route('/api/search')
def search_docs():
    """Search through documentation content"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    results = []
    for section in DOCS_NAVIGATION:
        for page in section['pages']:
            content, _ = load_markdown_file(page['file'])
            if content and query in content.lower():
                results.append({
                    'name': page['name'],
                    'title': page['title'],
                    'section': section['title'],
                    'url': f"/docs/{page['name']}"
                })
    
    return jsonify(results)

@app.route('/docs/static/<path:filename>')
def docs_static(filename):
    """Serve static files for documentation"""
    return send_from_directory(STATIC_DOCS_DIR, filename)

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('docs_base.html',
                         content="<h1>Page Not Found</h1><p>The requested documentation page could not be found.</p>",
                         toc="",
                         navigation=DOCS_NAVIGATION,
                         current_page='404',
                         page_title='Page Not Found'), 404

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(STATIC_DOCS_DIR, exist_ok=True)
    os.makedirs(TEMPLATES_DOCS_DIR, exist_ok=True)
    
    # Get port from environment or use default
    port = int(os.environ.get('DOCS_PORT', 8000))
    
    print(f"📚 Mental Health Analyzer Documentation starting on http://127.0.0.1:{port}")
    print("📖 Press Ctrl+C to stop the documentation server")
    
    app.run(debug=True, host='127.0.0.1', port=port) 