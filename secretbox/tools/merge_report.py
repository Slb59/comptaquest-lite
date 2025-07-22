from bs4 import BeautifulSoup

# Load the HTML files
with open("tests/htmlcov/integration_report.html", "r") as f1, open("tests/htmlcov/unit_report.html", "r") as f2:
    soup1 = BeautifulSoup(f1, "html.parser")
    soup2 = BeautifulSoup(f2, "html.parser")

# Find the section in the HTML where test results are stored and merge them
# This is a simplified example and will need to be adapted based on the actual HTML structure
results_section1 = soup1.find("div", id="test-results")
results_section2 = soup2.find("div", id="test-results")

# Append results from the second report to the first
if results_section1 and results_section2:
    for content in results_section2.find_all():
        results_section1.append(content)

# Save the merged HTML
with open("tests/htmlcov/merged_report.html", "w") as f:
    f.write(str(soup1))
