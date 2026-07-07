from paddleocr import PPStructureV3

pipeline = PPStructureV3(
    use_doc_orientation_classify=False,
    use_doc_unwarping=True
)

output = pipeline.predict('input_samples/messy_cropped.jpg')

for res in output:
    ocr_res = res['overall_ocr_res']
    print("Available keys in overall_ocr_res:", list(ocr_res.keys()))
    print()
    for text, score in zip(ocr_res['rec_texts'], ocr_res['rec_scores']):
        print(f"[{score:.2f}] {text}")