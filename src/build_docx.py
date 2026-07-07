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

def sort_blocks_with_bbox_fallback(blocks):
    """
    Blocks with a real order_index keep their relative order (this correctly
    handles multi-column layouts, which a pure y-coordinate sort would break).
    Blocks WITHOUT an order_index (headers, page numbers, sometimes tables)
    get inserted into the sequence based on their vertical (y) position,
    instead of being dumped at the end.
    """
    ordered = [b for b in blocks if b.order_index is not None]
    ordered.sort(key=lambda b: b.order_index)

    unordered = [b for b in blocks if b.order_index is None]

    # Insert each unordered block at the position matching its vertical location
    result = list(ordered)
    for u_block in unordered:
        u_y = u_block.bbox[1]  # top y-coordinate of the block
        insert_pos = len(result)
        for idx, o_block in enumerate(result):
            if o_block.order_index is not None and o_block.bbox[1] > u_y:
                insert_pos = idx
                break
        result.insert(insert_pos, u_block)

    return result

def build_docx(image_path, output_path):
    pipeline = PPStructureV3(
        use_doc_orientation_classify=False,
        use_doc_unwarping=True
    )

    output = pipeline.predict(image_path)

    doc = Document()

    for res in output:
        blocks = sort_blocks_with_bbox_fallback(res['parsing_res_list'])

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
    build_docx('input_samples/anna_karenina.png', 'output/anna_karenina_v2.docx')