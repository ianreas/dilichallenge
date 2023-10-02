from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import re
import spacy

def extract_text_from_page(page_number):
    text = ""
    
    for page_layout in extract_pages('Offering-Memorandum-The-Knol-Apartments.pdf'):
        if page_layout.pageid == page_number:
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    text += element.get_text()
            break  # stop processing once the desired page is found and processed

    return text


def findMatchWithPattern(text, pattern):
    match = re.search(pattern, text, re.DOTALL)

    if match:
        property_name = match.group(1).strip()  # Use strip() to remove any leading or trailing whitespace
        return property_name
    else:
        print("Property name not found!")


def extract_table_info(pdf_path, pattern, target_page):
    for page_num, page_layout in enumerate(extract_pages(pdf_path), start=1):
        if page_num != target_page:
            continue
        
        # Store each text block with its x-coordinate and y-coordinate
        text_blocks = []
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                # Get the x-coordinate (x0) and y-coordinate (y0) of the text block
                x0, y0 = element.bbox[0], element.bbox[1]
                text = element.get_text().strip()
                text_blocks.append(((x0, y0), text))

        # Sort text blocks based on y-coordinate first (to identify rows) and then x-coordinate (for left-to-right order)
        sorted_blocks = sorted(text_blocks, key=lambda x: (-x[0][1], x[0][0]))

        # Combine the sorted text
        full_text = ' '.join([text for _, text in sorted_blocks])

        # Use regex to find the Total Units value
        match = re.search(pattern, full_text)
        if match:
            return match.group(1)

#property name



#print(findMatchWithPattern(extract_text_from_page(28), r'Knol Apartments\s+(\d+)\s+(\d+)\s+\$\d+,\d+\s+\$\d+\.\d+\s+(\d+)\s+([\d.]+%)'))

lines = extract_text_from_page(28).split('\n')
index = lines.index('Knol Apartments')
occupancy_percentage = lines[index + 7]  # 7 lines down from 'Knol Apartments'

#print(occupancy_percentage)

#print(extract_text_from_page(28))


def extract_table_info_data_occupancy(pdf_path, target_page):
    for page_num, page_layout in enumerate(extract_pages(pdf_path), start=1):
        if page_num != target_page:
            continue
        
        # Store each text block with its x-coordinate and y-coordinate
        text_blocks = []
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                # Get the x-coordinate (x0) and y-coordinate (y0) of the text block
                x0, y0 = element.bbox[0], element.bbox[1]
                text = element.get_text().strip()
                text_blocks.append(((x0, y0), text))

        # Sort text blocks based on y-coordinate first (to identify rows) and then x-coordinate (for left-to-right order)
        sorted_blocks = sorted(text_blocks, key=lambda x: (-x[0][1], x[0][0]))

        # Combine the sorted text
        full_text = ' '.join([text for _, text in sorted_blocks])
        
        # Split the string by spaces
        parts = full_text.split()

        # Find the index of 'Knol Apartments' in the split parts
        index = parts.index('Knol')
        # Access the 6th string after 'Knol Apartments'
        if index != -1 and len(parts) > index + 7: # To ensure there's no index error
            occupancy_percentage = parts[index + 7]
            return occupancy_percentage
        else:
            print("Knol Apartments not found or data not complete.")

def extract_table_info_zip(pdf_path, target_page):
    for page_num, page_layout in enumerate(extract_pages(pdf_path), start=1):
        if page_num != target_page:
            continue
        
        # Store each text block with its x-coordinate and y-coordinate
        text_blocks = []
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                # Get the x-coordinate (x0) and y-coordinate (y0) of the text block
                x0, y0 = element.bbox[0], element.bbox[1]
                text = element.get_text().strip()
                text_blocks.append(((x0, y0), text))

        # Sort text blocks based on y-coordinate first (to identify rows) and then x-coordinate (for left-to-right order)
        sorted_blocks = sorted(text_blocks, key=lambda x: (-x[0][1], x[0][0]))

        # Combine the sorted text
        full_text = ' '.join([text for _, text in sorted_blocks])

        match = re.search(r'\b[A-Z]{2}\s(\d{5})\b', full_text)
        if match:
            zip_code = match.group(1)
            return zip_code
        else:
            print("ZIP code not found.")


#print(extract_text_from_page(37))


print("Property Name: " + findMatchWithPattern(extract_text_from_page(1), r'FOR THE ACQUISITION OF:\s*([^|]+)'))
print("Purchase Price: " + findMatchWithPattern(extract_text_from_page(10), r'Purchase Price / Acquisition Cost[^\$]*([\$\d,]+)'))
print("Number of Units: " + extract_table_info('Offering-Memorandum-The-Knol-Apartments.pdf', r"Total Units\s*(\d+)", 10))
print("Total Rentable Sq. Feet: " + extract_table_info('Offering-Memorandum-The-Knol-Apartments.pdf',r"Total\s*Rentable\s*Square\s*Feet\s*([\d,]+)\s*SF", 10))
print("Average Unit Sq. Feet: " + extract_table_info('Offering-Memorandum-The-Knol-Apartments.pdf', r"Average Square Feet/Unit\s*(\d+)", 10))



    
print("Price Per Unit: " + findMatchWithPattern(extract_text_from_page(17), r"\$/Unit\s*(\$\d{1,3}(?:,\d{3})*)"))

print("Average Monthly Rent: $" + findMatchWithPattern(extract_text_from_page(17), r"Total/Average\s*(?:\d+[,.]?\d*\s*){3}(\d{1,3}(?:,\d{3})*)"))

print("Average Rent / Sq. Ft: $" + findMatchWithPattern(extract_text_from_page(17), r"Total/Average\s*(?:\d+[,.]?\d*\s*){4}([\d.]+)"))

print("Occupancy Rate: " + extract_table_info_data_occupancy('Offering-Memorandum-The-Knol-Apartments.pdf', 28))



nlp = spacy.load("en_core_web_sm") #python -m spacy download en_core_web_sm

doc = nlp(extract_text_from_page(37))

#Extract and print named entities, labels, and their positions in the text
print("Sponsor: " + doc.ents[0].text)

#print("Average Unit Sq. Feet: " + extract_table_info('Offering-Memorandum-The-Knol-Apartments.pdf', r"Property Address\s*(\d+)", 10))






    


print("Zip code: " + extract_table_info_zip("Offering-Memorandum-The-Knol-Apartments.pdf", 10))



