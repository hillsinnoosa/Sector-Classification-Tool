import requests
from bs4 import BeautifulSoup
import streamlit as st

def classify_sector(website_url):
    try:
        # Fetch website content
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(website_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse website content
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True).lower()
        
        # Define sector keywords with weighted importance
        sectors = {
            "Civil": {
                "keywords": ["road construction", "earthmoving", "subdivisions", "infrastructure", "civil engineering", "bridges", "highways", "tunnels", "sewer systems"],
                "weight": 1.5
            },
            "Resources": {
                "keywords": ["mining", "oil and gas", "resource recovery", "recycling", "energy", "natural resources", "fossil fuels", "exploration", "refinery"],
                "weight": 2.0
            },
            "Landscape": {
                "keywords": ["landscaping", "parks", "gardens", "green spaces", "recreational areas", "environmental rehabilitation", "streetscapes"],
                "weight": 1.2
            },
            "Build": {
                "keywords": ["residential construction", "commercial buildings", "industrial parks", "office towers", "warehouses", "prefabrication", "modular construction", "high-rise apartments"],
                "weight": 1.8
            },
            "Manufacturing": {
                "keywords": ["production", "assembly", "fabrication", "manufacturing", "supply chain", "factory", "machinery", "processing"],
                "weight": 1.6
            }
        }
        
        # Check for sector matches using weighted scoring
        sector_scores = {sector: 0 for sector in sectors}
        
        for sector, data in sectors.items():
            for keyword in data["keywords"]:
                if keyword in text:
                    sector_scores[sector] += data["weight"]

        # Determine the best match
        best_match = max(sector_scores, key=sector_scores.get)
        best_score = sector_scores[best_match]

        if best_score > 0:
            return f"Suggested Sector: {best_match} (Score: {best_score:.2f})"
        else:
            return "No clear sector match found. Please review manually."

    except Exception as e:
        return f"Error fetching website: {str(e)}"

# Streamlit Web App
st.title("Company Sector Classification Tool")
st.write("Enter a company website below, and the tool will analyze its content to suggest a sector.")

website_url = st.text_input("Company Website URL", "")

if st.button("Classify Sector"):
    if website_url:
        result = classify_sector(website_url)
        st.write(result)
    else:
        st.write("Please enter a valid website URL.")
