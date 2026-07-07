from paddleocr import PPStructureV3

pipeline = PPStructureV3(
    use_doc_orientation_classify=False,
    use_doc_unwarping=True
)

output = pipeline.predict('input_samples/table_test.png')

for res in output:
    blocks = res['parsing_res_list']
    print(f"Total blocks found: {len(blocks)}")
    for block in blocks:
        print(f"label={block.label}, order_index={block.order_index}, content_length={len(block.content) if block.content else 0}")