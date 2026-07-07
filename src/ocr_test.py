from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=True,      # fixes curved/warped page text
    use_textline_orientation=False
)

result = ocr.predict('input_samples/messy_cropped.jpg')

for res in result:
    for text, score in zip(res['rec_texts'], res['rec_scores']):
        print(f"[{score:.2f}] {text}")