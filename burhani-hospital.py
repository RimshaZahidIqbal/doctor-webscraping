import requests
from bs4 import BeautifulSoup
import re 
import os 
import json 

# URL of the main page
# main_url = "https://burhanihospital.org.pk/specialization/child-specialist/"

# main_url = "https://burhanihospital.org.pk/specialization/neurologist/"

main_url = "https://burhanihospital.org.pk/specialization/psychiatrist/"

# Request the main page
response = requests.get(main_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the doctor articles
doctors = soup.find_all('article', class_='docs-all')

# Initialize a list to store all doctor data
doctors_data = []

for doctor in doctors:
    # Extract basic information
    name = doctor.find('h2').text.strip()
    position = doctor.find('h3').text.strip()
    qualifications = doctor.find('p', class_='qualification').text.strip()
    
    # Extract the doctor's detail page URL
    detail_page_url = doctor.find('a')['href']
    
    # Request the doctor's detail page
    detail_response = requests.get(detail_page_url)
    detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
    
    # Extract timing information from the detail page
    timing_div = detail_soup.find('div', class_='wpb_text_column')
    timing_text = timing_div.get_text(separator="\n").strip()
    
    # Initialize an empty dictionary for the timings
    timings = {}
    
    # Process the timing information
    for line in timing_text.split("\n"):
        day_match = re.match(r"(\w+)\s*&amp;\s*(\w+)\s*:\s*(.+)", line)
        if day_match:
            # If multiple days are listed, split them and add to the dictionary
            days = [day_match.group(1), day_match.group(2)]
            timing = day_match.group(3).strip()
            for day in days:
                timings[day] = timing
        else:
            day_time = line.split(" : ")
            if len(day_time) == 2:
                day, time = day_time
                timings[day.strip()] = time.strip()
    # Create a dictionary for the doctor's information
    doctor_data = {
        "name": name,
        "image ": "",
        "position": position,
        "hospital": "Burhani Hospital",
        "qualifications": qualifications,
        "timings": timings,
        
    }
    
    # Add the doctor's information to the list
    doctors_data.append(doctor_data) 




if os.path.exists("doctors_info.json"):
    with open("doctors_info.json", 'r') as json_file:
        existing_data = json.load(json_file)
else:
    existing_data = []

# Append new data to existing data
existing_data.extend(doctors_data)

# Write updated data to the JSON file
with open("doctors_info.json", 'w') as json_file:
    json.dump(existing_data, json_file, indent=4)



