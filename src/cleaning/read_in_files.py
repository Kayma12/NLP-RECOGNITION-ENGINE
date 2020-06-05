import textract


# The following function takes a file and/or file path, either with doc or
# docx extension, and returns the text representation of it, i.e. a txt file.

def read_in_doc_docx_file(file):
    text_file_repr = textract.process(file)
    text_file_repr = text_file_repr.decode('utf-8')
    return text_file_repr
