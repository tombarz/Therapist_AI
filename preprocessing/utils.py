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
print(remove_one_worded_counselor_answer([("i dont know","what i want"),("asdf","asdf a"),("asdf","a"),("bcd","a a"),("asd","asdfasdfasdfasdfasdf"),("fgh a","asdf"),("jkl","a")]))

import re


def extract_data_T_C(text):
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


def extract_data_T_C_colon(text):
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


# a single page
with pdfplumber.open(r'Transcript-of-Therapy-Session-by-Douglas-Bower.pdf') as pdf:
    first_page = pdf.pages[1]
    print(first_page.extract_text())
    print(extract_data_T_C_colon(remove_sograyim(first_page.extract_text())))

