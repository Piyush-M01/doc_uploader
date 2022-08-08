import streamlit as st
import pandas as pd
import docx2txt
from summa import keywords
from PIL import Image

class doc_uploader:

    def __init__(self):
        st.title("Document Uploader")
        st.markdown(""" <style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}</style> """, unsafe_allow_html=True)
        self.reduce_padding()
    
    def reduce_padding(self):
        padding = 0
        st.markdown(f""" <style>.reportview-container .main .block-container{{
                padding-top: {padding}rem;
                padding-right: {padding}rem;
                padding-left: {padding}rem;
                padding-bottom: {padding}rem;
            }} </style> """, unsafe_allow_html=True)

    # @st.cache(suppress_st_warning=True)
    def uploader(self):
        st.subheader("DocumentFiles")
        self.docx_file = st.file_uploader("Upload Document", type=["docx"])
        if st.button("Upload"):

            if self.docx_file is not None:
                file_details = {"filename":self.docx_file.name, "filetype":self.docx_file.type,
                                "filesize":self.docx_file.size}
                st.write(file_details)

                if self.docx_file.type == "text/plain":
                    # Read as string (decode bytes to string)
                    self.raw_text = str(self.docx_file.read(),"utf-8")
                    st.text(self.raw_text)

                else:
                    self.raw_text = str(docx2txt.process(self.docx_file))
                    st.write(self.raw_text)

    def make_form(self):
        st.subheader("Append Information to the document uploaded")
        with st.form("my_form"):
            value=st.text_input("Write the data that you want to append to the above document:")
            st.write(value)
            self.submitted = st.form_submit_button("Submit")
        if self.submitted==True:
            try:
                self.modified_data=str(docx2txt.process(self.docx_file))+"\n \n"+value
                st.write(self.modified_data)
            except:
                st.write(value)
                self.modified_data=value
            self.keyword_extractor(self.modified_data)
            
    def doc_downloader(self,data):
        st.subheader("Download the text file")
        st.download_button('Download Text File',data, 'text/plain.docx')
        # export_as_pdf = st.button("Download PDF")
        # if export_as_pdf:
        #     self.create_download_link(data,"text_pdf.pdf")

    def keyword_extractor(self,data):
        self.TR_keywords = keywords.keywords(data, scores=True)
        keyword=[]
        st.subheader("Keywords: ")
        for i in self.TR_keywords:
            keyword.append(i[0])
        data=data+"\n\n"+"Keywords: \n"
        for i in keyword:
            st.write(i)
            data=data+i+"\n"
        self.doc_downloader(data)

if __name__=="__main__":
    img=Image.open('upload.png')
    st.set_page_config(page_title="Doc Uploader",page_icon=img)
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True)
    x=doc_uploader()
    x.uploader()
    x.make_form()