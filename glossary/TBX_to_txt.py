import xml.etree.ElementTree as ET
import argparse
import csv

def parse_tbx(file_path, source_lang='en', target_lang='es'):
    tree = ET.parse(file_path)
    root = tree.getroot()
    ns = {'tbx': 'urn:iso:std:iso:30042:ed-2'}  # TBX-Basic v2 default namespace

    # Try to handle both namespaced and non-namespaced tags
    def get_tag(tag):
        return f"{{{ns['tbx']}}}{tag}" if root.tag.startswith('{') else tag

    entries = []

    for term_entry in root.findall(f".//{get_tag('termEntry')}"):
        terms = {}
        for lang_set in term_entry.findall(get_tag('langSet')):
            lang = lang_set.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
            term_elem = lang_set.find(f"./{get_tag('tig')}/{get_tag('term')}")
            if lang and term_elem is not None:
                terms[lang] = term_elem.text
        if source_lang in terms and target_lang in terms:
            entries.append((terms[source_lang], terms[target_lang]))
    
    return entries

def save_to_tsv(entries, output_file):
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['Source Term', 'Target Term'])  # Header
        for row in entries:
            writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(description='Convert TBX to TSV')
    parser.add_argument('input', help='Input TBX file')
    parser.add_argument('output', help='Output TSV file')
    parser.add_argument('--source-lang', default='en', help='Source language code (default: en)')
    parser.add_argument('--target-lang', default='es', help='Target language code (default: es)')
    args = parser.parse_args()

    entries = parse_tbx(args.input, args.source_lang, args.target_lang)
    save_to_tsv(entries, args.output)
    print(f"Converted {len(entries)} entries to {args.output}")

if __name__ == '__main__':
    main()
