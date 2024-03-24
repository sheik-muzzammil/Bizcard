import streamlit as st
st.set_page_config(page_title="BizCardX: Extracting Business Card Data with OCR", layout="wide")
page_bg_img= """
<style>
[data-testid="stAppViewContainer"]
{
text-align: center;
background-color: #cfd3ce;
}
[data-testid="stHeader"]
{
background-color: #ef3939;
}
[data-testid="stSidebar"]
{
text-decoration-color: #e84d4c;
background-color: #e48f76;

}

</style>
"""

import pandas as pd
import easyocr

import numpy as np
import streamlit_option_menu as option_menu
from PIL import Image
import cv2
import re
import googletrans
from googletrans import Translator
import pymongo
client=pymongo.MongoClient('mongodb://sheikmuzzammil:khamilabanu@ac-0zbysir-shard-00-00.6t66exf.mongodb.net:27017,ac-0zbysir-shard-00-01.6t66exf.mongodb.net:27017,ac-0zbysir-shard-00-02.6t66exf.mongodb.net:27017/?ssl=true&replicaSet=atlas-8wvq96-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client['BizcardX']
col_en= db['en_cards']

col_other = db['other_cards']

dict1={"Name":[], "company":[], "address":[], "website":[], "phone_no":[], "mail_id":[]}


st.title('BizCardX: Extracting Business Card Data with OCR')

st.markdown(page_bg_img, unsafe_allow_html=True)


with st.sidebar:
    selected_page = st.selectbox('EXTRACT TEXT FROM IMAGE', ('Bizcard', 'Others', 'Manage Data', 'Contact Details'))


def extracted_data1(output):
  temp=[]
  for i in range(0,len(output)):
    temp.append(output[i][1])
  return temp


def extracted_data1(output):
  temp=[]
  for i in range(0,len(output)):
    temp.append(output[i][1])
  return temp

def extracted_data(output):
  data=[]
  for i in range(0,len(output)):
    data.append(output[i][1])
  temp = " ".join(data)
  try:
    # Mail id pattern
    email_pattern = re.compile(r'''(
        [a-zA-Z0-9]+
        @
        [a-zA-z0-9]+
        \.[a-zA-Z]{2,10}
        )''', re.VERBOSE)
    mail_id = ''
    for i in email_pattern.findall(temp):
      mail_id += i
      temp = temp.replace(i, '')
    print(mail_id)
  except:
    mail_id = ""
    # phone no
  try:
    phoneNumber_pattern = re.compile(r'\+*\d{2,3}-\d{3,10}-\d{3,10}')
    phone_no = ''
    for numbers in phoneNumber_pattern.findall(temp):
      phone_no = phone_no + ' ' + numbers
      temp = temp.replace(numbers, '')
    print(phone_no)
  except:
    phone_no = ""

  try:
    address_pattern = re.compile(r'\d{2,4}.+\d{6}')
    address = ''
    for addr in address_pattern.findall(temp):
      address += addr
      temp = temp.replace(addr, '')
    print(address)
  except:
    address = ""

  try:
    website_pattern = re.compile(r'www.?[\w.]+', re.IGNORECASE)
    website = ''
    for lin in website_pattern.findall(temp):
      website += lin
      temp = temp.replace(lin, '')
    print(website)
  except:
    website = ""

  try:
    lst = []
    for i in data:
      if i in temp:
        lst.append(i)
      else:
        continue
    Name = lst[0]
    company = lst[1]
  except:
    Name = ""
    company = ""
  return Name, company, address, website, phone_no, mail_id


if selected_page =='Bizcard':
  st.subheader("Extracting Business Card Data")
  st.write("This application helps you to extract data from image and download extracted informations in the table form. ")


  uploaded_file = st.file_uploader('Choose an Image File ', type=['png','jpeg','jpg'])
  lang_lst = pd.read_excel('C:/Users/91962/Downloads/ocr_languages.xlsx')
  languages = lang_lst.loc[:, "Language"]
  selected1 = st.multiselect("Choose the language to translate", languages)

  res = []
  for i in range(0, len(selected1)):
    tmp = lang_lst.loc[lang_lst['Language'] == selected1[i], "code"]
    for i in tmp:
      res.append(i)

  if len(res) > 1:
    if st.button("Extract and Store"):
      c1, c2, c3 = st.columns([1, 1, 1])
      try:
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
        with c2:
          st.image(image)
      except:
        pass
      if uploaded_file is not None:
        reader = easyocr.Reader(res)
        ex_data = reader.readtext(image, paragraph=True)
        data = extracted_data1(ex_data)
        st.write(data)
        x = " ".join(data)
        sam_dict = {"data": x}
        col_other.insert_one(sam_dict)

  else:
    c1, c2, c3 = st.columns([1, 1, 1])
    try:
      image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
      with c2:
        st.image(image)
    except:
      pass
    if st.button("Extract and Store"):
      if uploaded_file is not None:
        reader = easyocr.Reader(res)
        ex_data = reader.readtext(image, paragraph=True)

        Name, company, address, website, phone_no, mail_id = extracted_data(ex_data)
        dict1["Name"].append(Name)
        dict1["company"].append(company)
        dict1["address"].append(address)
        dict1["website"].append(website)
        dict1["phone_no"].append(phone_no)
        dict1["mail_id"].append(mail_id)
        col_en.insert_one(dict1)
        df = pd.DataFrame(dict1)
        st.dataframe(df)

if selected_page== "Others":
      st.subheader("Extracting text from image")
      st.text("This app helps you to extract data from image and download extracted informations in the table form. ")

      uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
      lang_lst=pd.read_excel('C:/Users/91962/Downloads/ocr_languages.xlsx')
      languages=lang_lst.loc[:,"Language"]
      selected1=st.multiselect("Choose the language of file",languages)

      res=[]
      for i in range(0,len(selected1)):
        tmp=lang_lst.loc[lang_lst['Language'] == selected1[i],"code"]
        for i in tmp:
          res.append(i)


      if st.button("Extract and Store"):
        c1,c2,c3=st.columns([1,1,1])
        try:
          image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
          with c2:
            st.image(image)
        except:
          pass
        if uploaded_file is not None:
          reader = easyocr.Reader(res)
          ex_data = reader.readtext(image, paragraph=True)
          data1=[]
          for i in range(0,len(ex_data)):
            data1.append(ex_data[i][1])
            temp1 = " ".join(data1)

          st.markdown(
            '__<p style="font-family:sans-serif; font-size: 20px;">Extracted text </p>__',
            unsafe_allow_html=True)
          st.write(temp1)


          st.markdown(
            '__<p style="font-family:sans-serif; font-size: 20px;">Translated text in English</p>__',
            unsafe_allow_html=True)

          translator=Translator()
          detected=translator.detect(temp1)
          translated=translator.translate(temp1)
          st.write(translated.text)
          txt=translated.text
          c1,c2,c3=st.columns([1,1,1])
          with c2:
            st.download_button('Download ', txt, "text file" )


if selected_page== "Manage Data":
      st.subheader("Extracted Documents")
      tab1, tab2= st.tabs(["English Cards", "Other Cards"])
      with tab1:
        en_cards_lst = []
        for ele in col_en.find({}):
          en_cards_lst.append(ele["Name"][0])
        select_doc = st.selectbox("Select card detail", en_cards_lst, key="en_select_doc")  # Unique key assigned
        #print(select_doc)
        # x="Amit kumar CEO & FOUNDER"
        if select_doc:
          en_card_detail={}
          for rec in col_en.find({}):
            if rec["Name"][0] ==select_doc:
              en_card_detail["Name"]=rec["Name"][0]
              en_card_detail["company"]=rec["company"][0]
              en_card_detail["address"]=rec["address"][0]
              en_card_detail["website"]=rec["website"][0]
              en_card_detail["phone_no"]=rec["phone_no"][0]
              en_card_detail["mail_id"]=rec["mail_id"][0]
          en_card_df=pd.Series(en_card_detail)
          column1,column2=st.columns([1,1])
          with column1:
            st.write(en_card_df)
            if st.button("Delete",key="1"):
              for rec in col_en.find({}):
                if rec["Name"][0] ==select_doc:
                  col_en.delete_one(rec)
                  st.write("Document deleted")
          with column2:
            Name=st.text_input("Name:")
            company=st.text_input("Company:")
            address=st.text_input("Address:")
            website=st.text_input("Website:")
            phone_num=st.text_input("Phone_no:")
            mail_id=st.text_input("Mail_id:")

            if st.button("Update"):
              for record in col_en.find({}):
                print(record)
                y=record["_id"]
                x=record["Name"][0]
                if x == select_doc:
                  col_en.delete_one(record)
                  d={"Name":[Name],"company":[company],"address":[address],"website":[website],"phone_no":[phone_num],"mail_id":[mail_id]}
                  col_en.insert_one(d)

      with tab2:
        other_cards_lst = []
        for ele in col_other.find({}):
          other_cards_lst.append(ele["data"])
        select_doc = st.selectbox("Select card detail", other_cards_lst, key="other_select_doc")
        if st.button("Delete",key="2"):
          for rec in col_other.find({}):
            if rec["data"] ==select_doc:
              col_other.delete_one(rec)
              st.write("Document deleted")

if selected_page == "Contact Details":
    st.subheader("Contact Details")
    st.write(">>BizCardX: Extracting Business Card Data")
    st.write(">>Created by: Sheik Muzzammil. A")
    st.write('>>Email_ID: sheikmuzzammil4416@gmail.com')
    st.write(">>Linkedin page: https://www.linkedin.com/in/sheik-muzzammil-06641225a/")

















