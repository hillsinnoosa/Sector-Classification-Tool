import requests
from bs4 import BeautifulSoup
import re
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
        
        # Define sector keywords
        sectors = {
            "Civil": ["road construction", "earthmoving", "subdivisions", "infrastructure", "civil engineering"],
            "Resources": ["mining", "oil and gas", "resource recovery", "recycling", "energy", "natural resources"],
            "Landscape": ["landscaping", "parks", "gardens", "green spaces", "recreational areas"],
            "Build": ["residential construction", "commercial buildings", "industrial parks", "office towers", "warehouses"],
            "Manufacturing": ["production", "assembly", "fabrication", "manufacturing", "supply chain"],
        }
        
        # Check for sector matches
        sector_match = {}
        for sector, keywords in sectors.items():
            count = sum(1 for keyword in keywords if keyword in text)
            if count > 0:
                sector_match[sector] = count
        
        # Determine best match
        if sector_match:
            best_match = max(sector_match, key=sector_match.get)
            return f"Suggested Sector: {best_match} (Matched Keywords: {sector_match[best_match]})"
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
