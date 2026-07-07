import streamlit as st
from paddleocr import PPStructureV3
from docx import Document
from docx.shared import Pt
from bs4 import BeautifulSoup
import tempfile
import os

st.set_page_config(page_title="OCR Doc Reconstructor")
st.title("Image to DOCX Converter")
st.write("Upload a document image and get back a structured Word file.")

@st.cache_resource
def load_pipeline():
    return PPStructureV3(use_doc_orientation_classify=False, use_doc_unwarping=True)

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

def build_docx(image_path, output_path, pipeline):
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

uploaded_file = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded image", width='stretch')

    if st.button("Convert to DOCX"):
        with st.spinner("Processing... this may take a moment"):
            pipeline = load_pipeline()

            with tempfile.TemporaryDirectory() as tmpdir:
                input_path = os.path.join(tmpdir, uploaded_file.name)
                with open(input_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())

                output_path = os.path.join(tmpdir, "output.docx")
                build_docx(input_path, output_path, pipeline)

                with open(output_path, 'rb') as f:
                    docx_bytes = f.read()

        st.success("Done!")
        st.download_button(
            label="Download DOCX",
            data=docx_bytes,
            file_name="converted_document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )