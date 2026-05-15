import fitz

def extract_text_from_pdf(file_path):
  # open file:
  # parse pdf 
  # append text to some json or keep appending text to a variable and return the variable at the end.
  document = fitz.open(file_path)
  full_text = ""
  for page in document:
    full_text += page.get_text()
  
  return full_text