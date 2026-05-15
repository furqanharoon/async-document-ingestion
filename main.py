from tasks import process_document

result = process_document.delay("../documents/small_size_pdfs/file1.pdf")
print ('\n Result :\n', result)
