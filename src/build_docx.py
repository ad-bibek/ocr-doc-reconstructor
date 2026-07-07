from paddleocr import PPStructureV3
from docx import Document
from docx.shared import Pt
from bs4 import BeautifulSoup

def add_html_table_to_doc(doc, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    rows = soup.find_all('tr')
    if not rows:
        return

    max_cols = max(len(row.find_all(['td', 'th'])) for row in rows)

    table = doc.add_table(rows=len(rows), cols=max_cols)
    table.style = 'Table Grid'

    for i, row in enumerate(rows):
        cells = row.find_all(['td', 'th'])
        for j, cell in enumerate(cells):
            if j < max_cols:
                table.cell(i, j).text = cell.get_text(strip=True)

def build_docx(image_path, output_path):
    pipeline = PPStructureV3(
        use_doc_orientation_classify=False,
        use_doc_unwarping=True
    )

    output = pipeline.predict(image_path)

    doc = Document()

    for res in output:
        blocks = res['parsing_res_list']
        blocks = sorted(blocks, key=lambda b: (b.order_index is None, b.order_index))

        for block in blocks:
            label = block.label
            content = block.content.strip() if block.content else ""

            if not content:
                continue

            if label == 'paragraph_title':
                doc.add_heading(content, level=1)
            elif label == 'doc_title':
                doc.add_heading(content, level=0)
            elif label == 'table':
                add_html_table_to_doc(doc, content)
                doc.add_paragraph("")
            else:
                p = doc.add_paragraph(content)
                p.style.font.size = Pt(11)

    doc.save(output_path)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    build_docx('input_samples/table_test.png', 'output/table_test.docx')