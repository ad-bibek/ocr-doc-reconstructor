from paddleocr import PPStructureV3
from docx import Document
from docx.shared import Pt

def build_docx(image_path, output_path):
    pipeline = PPStructureV3(
        use_doc_orientation_classify=False,
        use_doc_unwarping=True
    )

    output = pipeline.predict(image_path)

    doc = Document()

    for res in output:
        blocks = [b for b in res['parsing_res_list'] if b.order_index is not None]
        blocks.sort(key=lambda b: b.order_index)

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
                doc.add_paragraph(f"[TABLE DETECTED - CONTENT: {content}]")
            else:
                p = doc.add_paragraph(content)
                p.style.font.size = Pt(11)

    doc.save(output_path)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    build_docx('input_samples/messy_cropped.jpg', 'output/messy_cropped.docx')