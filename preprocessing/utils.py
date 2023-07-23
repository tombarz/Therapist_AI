import re
import pdfplumber
# This removes text written in (). usually it's a text that explains the situation and so it is not needed
def remove_sograyim(data):
  return re.sub(r'\([^)]*\)', '', data)
# We don't want to train the chat to return one worded answers. so we will connect 2 client sentences together and remove the counselor's answer if it is one word
# The data is already set to a list of tuples, tuple[0] == client sentence and tuple[1] == counselor's answer
def remove_one_worded_counselor_answer(data: list[tuple[str,str]]) -> list[tuple[str,str]]:
  ret_list = []
  client_text = ''
  bl = False
  for i in range(len(data)):
    if i == len(data) - 1 or len(data[i][1].split(" ")) > 1:
      if client_text != '':
        ret_list.append((client_text + data[i][0],data[i][1]))
      else:
        ret_list.append((data[i][0],data[i][1]))
    else:
      client_text += data[i][0] + " "
      bl = True
  return ret_list
#print(remove_one_worded_counselor_answer([("i dont know","what i want"),("asdf","asdf a"),("asdf","a"),("bcd","a a"),("asd","asdfasdfasdfasdfasdf"),("fgh a","asdf"),("jkl","a")]))

def extract_data_b_kind_1(text):
    # Regular expression patterns for T and C lines
    pattern_t = re.compile(r"(T\d+)([^T^C]*)", re.S)
    pattern_c = re.compile(r"(C\d+)([^T^C]*)", re.S)

    # Find all T and C lines
    t_lines = pattern_t.findall(text)
    c_lines = pattern_c.findall(text)

    # Remove extra spaces and new lines
    t_lines = [(t[0], re.sub(r'\s+', ' ', t[1].strip())) for t in t_lines]
    c_lines = [(c[0], re.sub(r'\s+', ' ', c[1].strip())) for c in c_lines]

    # Find minimum length to prevent index out of range
    min_length = min(len(t_lines), len(c_lines))

    # Pair T and C lines
    paired_lines = [(t_lines[i][1], c_lines[i][1]) for i in range(min_length)]

    return paired_lines


def extract_data_b_kind_2(text):
    # Regular expression patterns for T and C lines
    pattern_t = re.compile(r"(T\d+:)(.*?)(?=C\d+:)", re.S)
    pattern_c = re.compile(r"(C\d+:)(.*?)(?=T\d+:|$)", re.S)

    # Find all T and C lines
    t_lines = pattern_t.findall(text)
    c_lines = pattern_c.findall(text)

    # Remove extra spaces and new lines
    t_lines = [(t[0], re.sub(r'\s+', ' ', t[1].strip())) for t in t_lines]
    c_lines = [(c[0], re.sub(r'\s+', ' ', c[1].strip())) for c in c_lines]

    # Find minimum length to prevent index out of range
    min_length = min(len(t_lines), len(c_lines))

    # Pair T and C lines
    paired_lines = [(t_lines[i][1], c_lines[i][1]) for i in range(min_length)]

    return paired_lines
def extract_data_d_kind(text):
    # Regular expression patterns for C and H lines
    pattern_c = re.compile(r"(C:)(.*?)(?=H:|$)", re.S)
    pattern_h = re.compile(r"(H:)(.*?)(?=C:|$)", re.S)

    # Find all C and H lines
    c_lines = pattern_c.findall(text)
    h_lines = pattern_h.findall(text)

    # Remove extra spaces and new lines
    c_lines = [(c[0], re.sub(r'\s+', ' ', c[1].strip())) for c in c_lines]
    h_lines = [(h[0], re.sub(r'\s+', ' ', h[1].strip())) for h in h_lines]

    # Find minimum length to prevent index out of range
    min_length = min(len(c_lines), len(h_lines))

    # Pair C and H lines
    paired_lines = [(h_lines[i][1], c_lines[i][1]) for i in range(min_length)]

    return paired_lines
def extract_data_a_kind(text):
    # Regular expression patterns for C and H lines
    pattern_c = re.compile(r"(COUNSELOR:)(.*?)(?=PATIENT:|$)", re.S)
    pattern_h = re.compile(r"(PATIENT:)(.*?)(?=COUNSELOR:|$)", re.S)

    # Find all C and H lines
    c_lines = pattern_c.findall(text)
    h_lines = pattern_h.findall(text)

    # Remove extra spaces and new lines
    c_lines = [(c[0], re.sub(r'\s+', ' ', c[1].strip())) for c in c_lines]
    h_lines = [(h[0], re.sub(r'\s+', ' ', h[1].strip())) for h in h_lines]

    # Find minimum length to prevent index out of range
    min_length = min(len(c_lines), len(h_lines))

    # Pair C and H lines
    paired_lines = [(h_lines[i][1], c_lines[i][1]) for i in range(min_length)]

    return paired_lines
def remove_timestamps(text):
    # Regular expression pattern for timestamps
    pattern_timestamp = re.compile(r"\d+:\d\d:\d\d\.\d")

    # Remove timestamps
    cleaned_text = pattern_timestamp.sub('', text)

    return cleaned_text

# a single page
def read_page_from_pdf(file_path, page_number):

    with pdfplumber.open(file_path) as pdf:
        pdf_page = pdf.pages[page_number]
        return pdf_page.extract_text()

def read_pages_from_pdf(file_path):
    # for every page
    pdf_pages = []
    with pdfplumber.open(file_path) as pdf:
         for pages in pdf.pages:
            pdf_pages.append(pages.extract_text())
    return pdf_pages
#print(extract_data_d_kind(open('../raw_data/d_kind/1.txt','r').read()))
#print(open('../raw_data/d_kind/1.txt','r').read())
page_one = read_page_from_pdf('../raw_data/a_kind/1.pdf',0)
print(page_one)
print(remove_one_worded_counselor_answer(extract_data_a_kind(remove_sograyim(remove_timestamps(page_one)))))
