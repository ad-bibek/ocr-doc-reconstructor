from paddleocr import PPStructureV3

pipeline = PPStructureV3(
    use_doc_orientation_classify=False,
    use_doc_unwarping=True
)

output = pipeline.predict('input_samples/messy_cropped.jpg')

for res in output:
    blocks = res['parsing_res_list']
    first_block = blocks[0]
    print("Type:", type(first_block))
    print("Available attributes:", dir(first_block))
    print("---")
    # Try common alternatives
    for attr in ['block_order', 'order', 'reading_order', 'block_label', 'block_content', 'block_bbox']:
        try:
            print(f"{attr}: {getattr(first_block, attr)}")
        except AttributeError:
            print(f"{attr}: NOT FOUND")