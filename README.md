# KO2Pathway

**KO2Pathway** is a command-line tool designed to map KEGG Orthology (KO) identifiers to KEGG pathways efficiently. The tool retrieves pathway information from KEGG and generates a summary of pathway descriptions with the associated KO counts. Additionally, KO2Pathway allows for excluding specific pathways based on custom-defined terms and supports caching of KO-to-pathway mappings to avoid repetitive queries to the KEGG API.

## Features
- **KO-to-Pathway Mapping:** Maps KO identifiers to KEGG pathways.
- **Pathway Filtering:** Exclude specific pathways using custom exclusion terms (e.g., disease-related pathways).
- **Cache Support:** Saves KO-to-pathway mappings to a file for re-use, reducing the need for repeated KEGG API queries.
- **Customizable:** Filter pathways using custom exclusion terms (optional).
- **Flexible Plotting:** Optionally generate a circular barplot to visualize the top 20 pathways by KO count.

## Requirements

- **Python 3.6+**
- **pandas**
- **requests**
- **matplotlib**
- **numpy**

You can install the dependencies with the following command:

```bash
pip install -r requirements.txt
````

Installation
To use KO2Pathway, clone the repository and install the required dependencies:

bash
Copy
Edit
git clone https://github.com/yourusername/KO2Pathway.git
cd KO2Pathway
pip install -r requirements.txt
Usage
Basic Command
The basic command requires the KO_clean.tsv file (which maps genes to KOs). You can optionally provide an exclude_terms.txt file to filter out specific pathways.

bash
Copy
Edit
python ko2pathway.py --ko_clean KO_clean.tsv --exclude_terms exclude_terms.txt
Command-Line Arguments

Argument	Description	Default Value
--ko_clean	Path to the KO_clean.tsv file (required).	N/A
--exclude_terms	Path to the optional exclude_terms.txt file to filter pathways.	None
--cache_file	Path to save the KO-to-pathway mapping cache.	ko_pathway_cache.json
--output_file	Path to save the pathway summary (TSV format).	kegg_pathway_summary.tsv
--plot	Whether to generate a circular barplot of the top 20 pathways.	False
Example Usage
Basic Mapping without Plotting:

bash
Copy
Edit
python ko2pathway.py --ko_clean KO_clean.tsv --exclude_terms exclude_terms.txt --output_file kegg_pathway_summary.tsv
This command will process the KO identifiers from KO_clean.tsv, filter out pathways listed in exclude_terms.txt, and generate the pathway summary in kegg_pathway_summary.tsv.

Basic Mapping with Plotting:

bash
Copy
Edit
python ko2pathway.py --ko_clean KO_clean.tsv --exclude_terms exclude_terms.txt --output_file kegg_pathway_summary.tsv --plot True
This will also generate a circular barplot of the top 20 pathways by KO count.

Using Cached Data for Faster Processing:

bash
Copy
Edit
python ko2pathway.py --ko_clean KO_clean.tsv --exclude_terms exclude_terms.txt --output_file kegg_pathway_summary.tsv --cache_file ko_pathway_cache.json
This command will use the cached KO-to-pathway mapping stored in ko_pathway_cache.json if available, speeding up the process by avoiding redundant API calls.

Input File Formats
KO_clean.tsv
The KO_clean.tsv file should have the following format:

python-repl
Copy
Edit
Gene_ID    ko:KXXXXXX
Gene_ID    ko:KYYYYYY
...
Where Gene_ID is the identifier for the gene, and ko:KXXXXXX represents the KEGG Orthology (KO) identifier(s). Multiple KOs can be separated by commas.

exclude_terms.txt
The exclude_terms.txt file contains a list of terms to exclude from the KEGG pathway descriptions. Each term should be on a new line, and the matching is case-insensitive.

Example exclude_terms.txt:

sql
Copy
Edit
disease
cancer
amyotrophic lateral sclerosis
shigellosis
human papillomavirus infection
epstein-barr virus infection
Output
The tool generates a summary of pathways associated with the KO identifiers in KO_clean.tsv, which is saved as a TSV file (kegg_pathway_summary.tsv by default). This summary includes:

pathway_id: The ID of the pathway (e.g., map00020).

pathway_description: A brief description of the pathway.

KO_count: The number of KOs mapped to the pathway.

Example Output
python-repl
Copy
Edit
pathway_id    pathway_description                          KO_count
map00020      Citrate cycle (TCA cycle)                    6
map00030      Pentose phosphate pathway                    11
map00040      Pentose and glucuronate interconversions     2
map00051      Fructose and mannose metabolism              12
map00052      Galactose metabolism                         10
...
If the --plot flag is used, a circular barplot is generated to visualize the top 20 pathways by KO count.

License
KO2Pathway is released under the MIT License.

Acknowledgments
KEGG for providing pathway and KO data.

The Python community for the excellent libraries used in this tool (pandas, requests, matplotlib, etc.).

For more information or help, please contact [your-email@example.com].

python
Copy
Edit

This is the complete **README** in markdown format, covering everything from installation to usage, including file formats and options. Let me know if you'd like to make any additional changes or if there's something else you want to add!















