import re
import pdfplumber
import csv

# This removes text written in (). usually it's a text that explains the situation and so it is not needed
def remove_sograyim(data):
  data = re.sub(r'\[[^\]]*\]', '', data)
  return re.sub(r'\([^)]*\)', '', data)
# We don't want to train the chat to return one worded answers. so we will connect 2 client sentences together and remove the counselor's answer if it is one word
# The data is already set to a list of tuples, tuple[0] == client sentence and tuple[1] == counselor's answer
def remove_one_worded_counselor_answer(data: list[tuple[str,str]]) -> list[tuple[str,str]]:
  ret_list = []
  client_text = ''
  for i in range(len(data)):
    if i == len(data) - 1 or len(data[i][1].split(" ")) > 1:
      if client_text != '':
        ret_list.append((client_text + data[i][0],data[i][1]))
        client_text = ''
      else:
        ret_list.append((data[i][0],data[i][1]))
    else:
      client_text += data[i][0] + " "
  return ret_list

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
  
def extract_client_therapist_dialogue(lines):
    chats = {}
    for line in lines[1:]:
        if line[0] not in chats.keys():
            client_therapist_dialogue = []
            chats[line[0]] = client_therapist_dialogue
            client_answer = None
            id = int(line[0]) - 1
            if id > 0 and id != 75:
                chats[str(id)] = remove_one_worded_counselor_answer(chats[str(id)])
        if line[6] == 'client':
            client_answer = line[8]
        elif line[6] == 'therapist' and client_answer:
            therapist_answer = line[8]
            chats[line[0]].append((remove_sograyim(client_answer), remove_sograyim(therapist_answer), line[1]))
            client_answer = None
    return chats

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
# page_one = read_page_from_pdf('../raw_data/a_kind/1.pdf',0)
# print(page_one)
# print(remove_one_worded_counselor_answer(extract_data_a_kind(remove_sograyim(remove_timestamps(page_one)))))
  

def read_csv_file(file_path):
    lines = []
    with open(file_path, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            lines.append(row)
    return extract_client_therapist_dialogue(lines)
  
print(read_csv_file("./raw_data/AnnoMI-simple.csv"))
