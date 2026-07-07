from paddleocr import PPStructureV3

pipeline = PPStructureV3(
    use_doc_orientation_classify=False,
    use_doc_unwarping=True
)

output = pipeline.predict('input_samples/test_multipage.pdf')

page_count = 0
for res in output:
    page_count += 1
    print(f"--- Page {page_count} ---")
    print(f"page_index: {res.get('page_index', 'N/A')}")
    blocks = res['parsing_res_list']
    print(f"Blocks found: {len(blocks)}")

print(f"\nTotal pages processed: {page_count}")