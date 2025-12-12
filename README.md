# JS Files Refactoring Suggester 🐍

A Python tool that analyzes JS components and suggests refactoring improvements using AI.

## Features

- **🔍 File Discovery**: Recursively finds JS files (`.js`, `.jsx`, `.ts`, `.tsx`)
- **🤖 AI-Powered Analysis**: Uses Ollama AI to analyze code and suggest improvements
- **🌐 Web Interface**: Flask-based web UI for easy file upload and analysis
- **📝 CLI Tool**: Command-line interface for batch file analysis
- **🚫 Smart Filtering**: Automatically ignores `node_modules`, test directories, etc.
- **🔒 Secure Uploads**: Validates file types and securely handles uploads

## Project Structure

```
├── flaskr/
│   ├── __init__.py          # Flask web application
│   ├── analyze.py           # AI analysis module
│   └── find_files.py        # File discovery module
├── templates/               # HTML templates
│   ├── file_upload.html
│   └── analysis.html
├── .env                    # Environment variables
└── README.md
```

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd JS-Files-Refactoring-Suggester
   ```

2. **Create and activate virtual environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install flask ollama python-dotenv
   ```

4. **Set up environment variables** in `.env`:
   ```env
   OLLAMA_API_KEY=your_api_key_here
   ```

## Usage

### Web Interface (Recommended)

1. **Start the Flask server**:

   ```bash
   export FLASK_APP=flaskr
   export FLASK_DEBUG=1
   flask run
   ```

2. **Open `http://127.0.0.1:5000`** in your browser
3. **Upload a JS file** (`.js`, `.jsx`, `.ts`, `.tsx`)
4. **View AI-generated refactoring suggestions**

### Command Line Interface

**Find JS files**:

```bash
python flaskr/find_files.py /path/to/project
python flaskr/find_files.py -e .js .jsx        # Custom extensions
python flaskr/find_files.py -ignored dist .git # Custom ignored dirs
```

**Analyze a specific file with AI**:

```bash
python flaskr/analyze.py /path/to/project
```

The tool will list found files and prompt you to choose one for AI analysis.

## File Analysis Features

The AI analysis looks for:

- Performance improvements
- Readability enhancements
- Code organization
- Best practice violations
- Potential bugs and anti-patterns

## Supported File Types

- `.js` - JavaScript files
- `.jsx` - React JSX files
- `.ts` - TypeScript files
- `.tsx` - React TypeScript files

## Configuration

### Command Line Arguments (find_files.py)

| Argument                | Short      | Description                | Default                                      |
| ----------------------- | ---------- | -------------------------- | -------------------------------------------- |
| `path`                  |            | Directory to scan          | Current directory                            |
| `--extensions`          | `-e`       | File extensions to include | `.tsx` `.jsx`                                |
| `--ignored_directories` | `-ignored` | Directories to ignore      | `node_modules`, `__tests__`, `dist`, `build` |

### Environment Variables

| Variable         | Description         | Required |
| ---------------- | ------------------- | -------- |
| `OLLAMA_API_KEY` | Your Ollama API key | Yes      |

## Example Output

```
Found 5 React files in /project/src

1: /project/src/components/Button.tsx
2: /project/src/components/Header.jsx
3: /project/src/pages/Home.tsx
4: /project/src/pages/About.jsx
5: /project/src/utils/helpers.js

>>>> Which file would you like to analyze with AI? Choose one between 1 and 5:
```

After selection, the AI provides detailed refactoring suggestions.

## Code Structure

### `flaskr/__init__.py` - Flask Web Application

```python
# Handles file uploads, validates file types, processes uploads
# Creates temporary files for security, calls AI analysis
# Renders results in HTML templates
```

### `flaskr/analyze.py` - AI Analysis Module

```python
# Connects to Ollama API for AI-powered code analysis
# Supports streaming responses for real-time feedback
# Handles multiple response formats from Ollama API
# Can run as standalone CLI tool for batch analysis
```

### `flaskr/find_files.py` - File Discovery Module

```python
# Recursively searches directories for JS files
# Filters out ignored directories (node_modules, tests, etc.)
# Configurable file extensions and ignored directories
# Can be used independently as a file finder tool
```

## Development

This is a learning project focused on:

- Python web development with Flask
- AI integration for code analysis
- Building practical developer tools
- File system operations and CLI tools

## Common Issues & Solutions

### ModuleNotFoundError

```bash
# If you get "No module named 'ollama'"
pip install ollama

# If imports fail when running scripts directly
python -m flaskr.analyze  # Instead of python analyze.py
```

### Flask Import Errors

```bash
# Make sure you're in the virtual environment
source .venv/bin/activate

# Set Flask environment variables
export FLASK_APP=flaskr
export FLASK_DEBUG=1
```

### File Upload Issues

- Ensure uploaded files are valid JS files (`.js`, `.jsx`, `.ts`, `.tsx`)
- Check file size (large files may timeout)
- Verify Ollama API key is set in `.env`
