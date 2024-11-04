CHARACTER_OF_INTEREST = "chorus"

import os
# import pandas as pd
from lxml import etree

DIR = "tei"
NAMESPACES = {
    "tei": "http://www.tei-c.org/ns/1.0",
    "xml": "http://www.w3.org/XML/1998/namespace",
}


def to_urn(s: str):
    return f"urn:cts:greekLit:{s.replace('.xml', '')}"


FILES = []

for subdir in os.listdir(DIR):
    p = os.path.join(DIR, subdir)

    for f in os.listdir(p):
        filename = os.path.join(p, f)

        if os.path.isfile(filename):
            FILES.append((filename, to_urn(f)))

speakers = set()

def get_dramatist(urn: str):
    if "tlg0006" in urn: return "Euripides"

    if "tlg0011" in urn: return "Sophocles"

    if "tlg0085" in urn: return "Aeschylus"


def iter_lines(title, urn, tree, text_only=False):
    rows = []

    for l in tree.iterfind(".//tei:l", namespaces=NAMESPACES):
        if l.text is not None:
            n = l.xpath("./@n")
            speaker = l.xpath("../tei:speaker//text()", namespaces=NAMESPACES)

            if len(speaker) > 0:
                speaker = speaker[0].strip().replace(".", "")

                if speaker != "":

                    if text_only:
                        rows.append(l.text.strip())
                    else:
                        speakers.add(speaker)
                        row = {
                            "n": n[0],
                            "urn": urn,
                            "dramatist": get_dramatist(urn),
                            "title": title,
                            "speaker": speaker,
                            "text": l.text.strip(),
                        }

                        rows.append(row)

    return rows

# data = []

for f, urn in FILES:
    tree = etree.parse(f)
    title = tree.xpath("//tei:titleStmt/tei:title/text()", namespaces=NAMESPACES)[0]
    lines = iter_lines(title, urn, tree, text_only=True)

    plain_text_f = f.replace(".xml", ".txt").replace("tei", "data")

    with open(plain_text_f, 'w') as out:
        for line in lines:
            out.write(line + "\n")
#     data += lines

# df = pd.DataFrame(data)

# df.to_pickle('./greek-tragedy-by-line.pickle')