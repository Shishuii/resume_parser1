
# coding: utf-8

# In[1]:


from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys, getopt,logging,re
import pandas as pd
#converts pdf, returns its text content as a string
def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    text_list = text.split()

    return text
def find_name(string_to_search):
    index=string_to_search.find('\n')
    return string_to_search[:index]
def check_email(string_to_search):
    """
       Find first email address in the string_to_search
       :param string_to_search: A string to check for an email address in
       :type string_to_search: str
       :return: A string containing the first email address, or None if no email address is found.
       :rtype: str
       """
    try:
        regular_expression = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}", re.IGNORECASE)

        result = re.search(regular_expression, string_to_search)
        if result:
            result = result.group()
        return result
    except Exception, exception_instance:
        logging.error('Issue parsing email number: ' + string_to_search + str(exception_instance))
        return 'Email Address NOt Provided'


# In[2]:


def check_phone_number(string_to_search):

    try:
        regular_expression = re.compile(r"(\+)?(91)?( )?[789]\d{9}", re.IGNORECASE)
        result = re.search(regular_expression, string_to_search)
        if result:
            result = result.group()
            result = "".join(result)
        return result
    except Exception, exception_instance:
        logging.error('Issue parsing phone number: ' +  str(exception_instance))
        return None




# In[3]:


def check_por(string_to_search):
    full_string = string_to_search
    full_string = full_string.replace("\r", "\n")
    full_string = full_string.replace("\n", " ")
    full_string = re.sub(r"\(cid:\d{0,2}\)", " ", full_string)
    full_string = full_string.encode('ascii', errors='ignore')
    try:

        r =  [j for i,j in re.findall(r"(POSITIONS OF RESPONSIBILITY)\s*(.*?)\s*(?!\1)(?:TRAINING|PROJECTS|SKILLS|CONTACT DETAILS)",full_string)]

        return r[0]
    except Exception, exception_instance:
        #logging.error("")
        return ""


# In[4]:


check_l=['machine learning','python','java','php','data structures','algorithms','c programming','c++ programming','javascript','django','bootstrap','mathematics','css','html']
def check_comp(string_to_search):
    full_string = string_to_search
    full_string = full_string.replace("\r", "\n")
    full_string = full_string.replace("\n", " ")
    full_string = re.sub(r"\(cid:\d{0,2}\)", " ", full_string)
    full_string = full_string.encode('ascii', errors='ignore')
    try:

        r =  [j for i,j in re.findall(r"(.)\s*(.*?)\s*(?!\1)(?:Assessment)",full_string)]
        #print(r[0])
        l1 = r[0].split()
        #print(l1)
        l2 = " ".join(l1).split(":")
        tr=r[0].lower()
        l3=list()
        for i in check_l:

            p=tr.find(i)
            if p!=-1:
                l3.append(i)


        return ",".join(l3)
    except Exception, exception_instance:
        logging.error('Issue parsing comp: ' + full_string + str(exception_instance))
        return ""



# In[5]:


df=pd.DataFrame({'name':[],'email':[],'phone':[],'Position of Responsibility':[],'skill':[]})

df = df[['name','email','phone','Position of Responsibility','skill']]


# In[6]:



def main():
    #path="C:\Users\Ishou\python27\REsume_Parser"
    path1 = raw_input("Enter the path of input folder")
    arr=os.listdir(path1)
    files=[x for x in arr if x.endswith('.pdf')]

    i=0
    #print(files)
    for f in files:
        #print f
        l=list()
        text=convert(f)
        email=check_email(text)
        phone=check_phone_number(text)
        name=find_name(text)
        por = check_por(text)
        skill = check_comp(text)
        l.append(name)
        l.append(email)
        l.append(phone)
        l.append(por)
        l.append(skill)


        df.loc[i]=l
        i+=1



# In[7]:


main()
df.to_csv("result1.csv")


# In[8]:


print(df)
