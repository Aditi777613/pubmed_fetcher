from typing import List, Dict
import requests
import xml.etree.ElementTree as ET
import re


class PubMedFetcher:
    def __init__(self, debug: bool = False) -> None:
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.debug = debug

    def fetch_paper_ids(self, query: str) -> List[str]:
        params: Dict[str, str] = {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": "20"
        }
        response = requests.get(f"{self.base_url}esearch.fcgi", params=params)
        response.raise_for_status()
        ids = response.json()['esearchresult']['idlist']
        if self.debug:
            print(f"Fetched IDs: {ids}")
        return ids

    def fetch_paper_details(self, ids: List[str]) -> str:
        ids_str = ",".join(ids)
        params: Dict[str, str] = {
            "db": "pubmed",
            "id": ids_str,
            "retmode": "xml"
        }
        response = requests.get(f"{self.base_url}efetch.fcgi", params=params)
        response.raise_for_status()
        return response.text

    def parse_and_filter(self, xml_data: str) -> List[Dict]:
        """
        Parses PubMed XML and extracts:
        - PubmedID
        - Title
        - Publication Date
        - Non-academic Author(s)
        - Company Affiliation(s)
        - Corresponding Author Email (if found)
        """
        root = ET.fromstring(xml_data)
        papers = []

        for article in root.findall('.//PubmedArticle'):
            pmid_elem = article.find('.//PMID')
            title_elem = article.find('.//ArticleTitle')
            date_elem = article.find('.//PubDate/Year')

            pmid = pmid_elem.text if pmid_elem is not None else ''
            title = title_elem.text if title_elem is not None else ''
            pub_date = date_elem.text if date_elem is not None else ''

            non_academic_authors = []
            company_affiliations = []
            corresponding_email = ''

            for author in article.findall('.//Author'):
                affiliation_elem = author.find('.//AffiliationInfo/Affiliation')
                if affiliation_elem is not None:
                    affiliation = affiliation_elem.text.lower()
                    if 'university' not in affiliation and 'college' not in affiliation and 'school' not in affiliation:
                        last_name = author.findtext('LastName', default='Unknown')
                        non_academic_authors.append(last_name)
                        company_affiliations.append(affiliation)

                        # Extract email with regex if present
                        emails = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", affiliation)
                        if emails:
                            corresponding_email = emails[0]

            papers.append({
                'PubmedID': pmid,
                'Title': title,
                'Publication Date': pub_date,
                'Non-academic Author(s)': '; '.join(non_academic_authors),
                'Company Affiliation(s)': '; '.join(company_affiliations),
                'Corresponding Author Email': corresponding_email
            })

        return papers
