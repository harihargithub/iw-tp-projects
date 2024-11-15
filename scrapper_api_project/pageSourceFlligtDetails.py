# pageSourceFlligtDetails.py

from bs4 import BeautifulSoup

# Load the page source from the file
with open(
    "C:\\Users\\nhari\\OneDrive\\Documents\\iw tp projects\\scrapper_api_project\\pageSource.txt",
    "r",
    encoding="utf-8",
) as file:
    page_source = file.read()

# Parse the HTML
soup = BeautifulSoup(page_source, "html.parser")

# Example: Extract all div elements with a different class (update this based on your inspection)
flight_sections = soup.select("div.some-other-class")  # Update this selector

# Debug print to check if flight_sections is populated
print(f"Number of flight sections found: {len(flight_sections)}")

# Write the extracted parts to a file
output_path = "C:\\Users\\nhari\\OneDrive\\Documents\\iw tp projects\\scrapper_api_project\\pageSourceFlligtDetails.txt"
with open(output_path, "w", encoding="utf-8") as file:
    for flight_section in flight_sections:
        file.write(flight_section.prettify())
        file.write("\n\n")  # Add some spacing between sections
