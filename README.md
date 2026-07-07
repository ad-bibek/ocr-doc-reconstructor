\# OCR Document Reconstructor



Converts scanned or photographed document images into structured `.docx` files — preserving headings, paragraphs, and tables instead of producing a flat text dump.



Built in a 1-week sprint using PaddleOCR + PP-StructureV3 for layout-aware OCR, with a Streamlit UI for drag-drop conversion.



\## Demo



Upload an image → the pipeline detects text, classifies it into titles/paragraphs/tables → reconstructs it as a real Word document with proper formatting.



\## Stack



\- \*\*PaddleOCR / PP-StructureV3\*\* — text detection, recognition, and layout analysis

\- \*\*python-docx\*\* — Word document generation

\- \*\*BeautifulSoup\*\* — parsing table HTML output into Word tables

\- \*\*Streamlit\*\* — drag-drop web interface



\## Setup



```bash

conda create -n ocr-project python=3.11 -y

conda activate ocr-project

pip install -r requirements.txt

streamlit run app.py

```



\*\*Note on GPU:\*\* PaddlePaddle GPU wheels don't yet officially support Blackwell architecture GPUs (RTX 50-series, compute capability sm\_120) as of mid-2026. This project runs on CPU-mode PaddlePaddle as a result — functional but slower per image. See `paddlepaddle-sm120-wheels` community builds if GPU acceleration is needed.



\## What this pipeline actually solves



Basic OCR tools output a flat blob of text with no structure. This pipeline instead:

1\. Detects text regions and recognizes characters (PP-OCRv5)

2\. Classifies regions into titles, paragraphs, tables, and page numbers (PP-StructureV3 layout analysis)

3\. Reconstructs the document with correct Word styles (Heading 1, Normal paragraphs, real grid tables) in the correct reading order



\## Known limitations (found through testing, not assumed)



\- \*\*Curved/warped pages\*\*: Text near a book's spine or fold can fail detection entirely unless `use\_doc\_unwarping=True` is enabled — confirmed by testing the same image with and without this flag.

\- \*\*Background clutter\*\*: If the input image includes background objects (desk, hands, other items), the OCR will read text from them as if it were part of the document. Crop to the document boundary before processing for clean results.

\- \*\*Low-resolution dense tables\*\*: Small-font financial/numeric tables at low resolution produce unreliable character recognition, even though the row/column \*structure\* is captured correctly.

\- \*\*Elements without reading-order data\*\* (page headers, running titles, page numbers): PP-StructureV3 sometimes doesn't assign these an `order\_index`. This pipeline places them at the end of the document rather than dropping them, but this means a header can end up at the bottom instead of the top. A more complete fix would use each block's bounding box (y-coordinate) as a fallback sort key.

\- \*\*Two-page spreads with sidebar call-out boxes\*\*: Complex textbook-style layouts (colored info boxes running alongside main body text) can produce a reading order that doesn't cleanly match human reading flow.



\## Project structure
ocr-doc-reconstructor/

├── app.py                  # Streamlit UI

├── src/

│   ├── ocr\_test.py          # Baseline OCR testing script

│   ├── build\_docx.py        # Core image-to-docx pipeline

│   └── preprocess.py        # OpenCV preprocessing experiments

├── input\_samples/           # Test images

├── output/                  # Generated docx/json outputs

└── requirements.txt


