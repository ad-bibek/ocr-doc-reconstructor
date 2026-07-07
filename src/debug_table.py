from paddleocr import PPStructureV3

pipeline = PPStructureV3(
    use_doc_orientation_classify=False,
    use_doc_unwarping=True
)

output = pipeline.predict('input_samples/table_test.png')

for res in output:
    blocks = res['parsing_res_list']
    for block in blocks:
        print(f"Label: {block.label}")
        if block.label == 'table':
            print("Available attributes:", dir(block))
            print("Content:", block.content)
            print("---")