import json
import xml.etree.ElementTree as ET
import argparse
import os

import last_modified_by_git

def generate_sitemap(json_file, output_file="sitemap.xml"):
    """Generates a sitemap.xml from a JSON file"""

    if not os.path.exists(json_file):
        print(f"❌ Error: File '{json_file}' not found.")
        return

    with open(json_file, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    # Create the root element with the correct namespace
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for key, entry in json_data.items():  # Iterate over dictionary values

        if not isinstance(entry, dict):  # Ensure it's a dictionary
            continue

        if not entry.get("sitemap_include", True):  # Skip entries where sitemap_include is False
            continue

        url_elem = ET.SubElement(urlset, "url")

        # Ensure `loc` exists, prepend a domain if necessary
        loc_value = entry.get("loc", "/")  # Default to root if missing
        ET.SubElement(url_elem, "loc").text = loc_value

        # Optional fields
        if "priority" in entry:
            ET.SubElement(url_elem, "priority").text = str(entry["priority"])

        # Fixing changefreq key (handling "changefre" typo)
        changefreq_value = entry.get("changefreq") # Support both
        if changefreq_value:
            ET.SubElement(url_elem, "changefreq").text = changefreq_value
        
        last_modified = last_modified_by_git.get_last_modified_time("../Client" + entry.get("srcFile") + ".tsx")
        if last_modified:
            ET.SubElement(url_elem, "lastmod").text = last_modified


    # Convert to XML and write to file
    tree = ET.ElementTree(urlset)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

    print(f"✅ Sitemap successfully generated: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate sitemap from a JSON file.")
    parser.add_argument("json_file", help="Path to the input JSON file")
    parser.add_argument("--output", default="sitemap.xml", help="Output XML file")
    args = parser.parse_args()



    generate_sitemap(args.json_file, args.output)
