import base64
import streamlit as st
import pandas as pd
import docx2txt
import pdfplumber
from summa import keywords


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

                elif self.docx_file.type == "application/pdf":
                    try:
                        with pdfplumber.open(self.docx_file) as pdf:
                            pages = pdf.pages[0]
                            self.raw_text=str(pages.extract_text())
                            st.write(self.raw_text)
                    except:
                        st.write("None")

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
            

    # def create_download_link(self,data,filename):
    #     pdf = FPDF()
    #     pdf.add_page()
    #     f = open("text_plain", "r")
    #     pdf.set_font("Arial", size = 15)
    #     for x in f:
    #         pdf.cell(200, 10, txt = x, ln = 1, align = 'C')
    #     pdf.output(filename)
    #     with open(filename, 'rb') as h_pdf:
    #         st.download_button(
    #             label="Download PDF",
    #             data=h_pdf,
    #             file_name=filename,
    #             mime="application/pdf",
    #         )

    def doc_downloader(self,data):
        st.subheader("Download the text file")
        st.download_button('Download Text File',data, 'text/plain.docx')
        # self.create_download_link(data,"text_pdf.pdf")

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
    st.set_page_config(page_title="Doc Uploader")
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