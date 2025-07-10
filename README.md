# 📚 PubMed Fetcher CLI

A simple Python command-line tool to fetch PubMed articles matching a query, parse XML results, identify non-academic authors and company affiliations, extract corresponding emails, and save the output to CSV.

---

## 📌 Requirements

✅ Fetch paper IDs using `esearch`  
✅ Fetch paper details in XML using `efetch`  
✅ Parse XML to extract:
   - PubmedID
   - Title
   - Publication Date
   - Non-academic Author(s) (exclude affiliations with “university”, “college”, “school”)
   - Company Affiliation(s)
   - Corresponding Author Email (using regex)

✅ Export results to CSV  
✅ Command-line interface using [Typer](https://typer.tiangolo.com/)  
✅ Package management with [Poetry](https://python-poetry.org/)  
✅ Static type checking with [Mypy](http://mypy-lang.org/)

---

## ⚙️ Tech Stack

- **Python 3.13+**
- Poetry — dependency & virtual environment management
- Typer — CLI framework
- Pandas — CSV output
- Mypy — static typing
- NCBI E-utilities — PubMed API

---

## 🗂️ Project Structure

pubmed_fetcher/
├── init.py
├── cli.py # Typer CLI entrypoint
├── fetcher.py # Core: fetch IDs, fetch XML, parse & filter
pyproject.toml # Poetry config
poetry.lock # Locked dependencies
README.md

---

## 🚀 How to Run

### 1️⃣ Clone this repo
```bash
git clone https://github.com/Aditi777613/pubmed_fetcher.git
cd pubmed_fetcher

2️⃣ Install dependencies with Poetry
poetry install

3️⃣ Run the CLI
poetry run get-papers-list "YOUR_QUERY" --debug --file results.csv

---

Example:
poetry run get-papers-list "cancer therapy" --debug --file results.csv
✅ --debug → shows fetched PubMed IDs
✅ --file → saves output to results.csv; if omitted, prints to console

📄 Example Output CSV
PubmedID |  Title                                                |	Publication Date |	Non-academic Author(s) | Company Affiliation(s) |	Corresponding Author Email
---------|-------------------------------------------------------|------------------- |-------------------- -----|--------------- --------|-----------------------------
40635045 | A novel MIR100HG transcript enhances tumorigenesis... |	2025	           | Smith	                 |    ABC Pharma Inc.	   |     smith@abcpharma.com

---

✅ Type Checking
poetry run mypy pubmed_fetcher/

---

💡 Extensions
More robust non-academic filters (e.g., corp, inc, biotech)

Smarter email extraction regex

Additional output formats (JSON, Excel)

Unit tests for XML parsing

📝 License
This repository contains my coding assignment submission for the PubMed fetcher. Use, adapt, improve!

🙌 Thanks for reviewing!
Run → Fetch → Parse → Filter → Ship! 🚀✨
