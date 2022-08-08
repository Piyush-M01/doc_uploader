import streamlit as st
import docx2txt
from summa import keywords


class doc_uploader:

    def __init__(self):
        st.title("Document Uploader")

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
    x=doc_uploader()
    x.uploader()
    x.make_form()
