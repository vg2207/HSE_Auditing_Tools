import streamlit as st
import cv2
import numpy as np
import pandas as pd
from datetime import timedelta, datetime
from PIL import Image
import os

# from utils.helper import send_email
# from utils.constants import (SMTP_SERVER, PORT, SENDER_ADDRESS, SENDER_PASSWORD)
import smtplib
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage


@st.cache_data
def send_email(sender, password, receiver, smtp_server, smtp_port, email_message, subject, attachment=None, attach_file=None) :
    message = MIMEMultipart()
    message['To'] = Header(receiver)
    message['From'] = Header(sender)
    message['Subject'] = Header(subject)
    message.attach(MIMEText(email_message, 'plain', 'utf-8'))
    file_name=(datetime.today() + timedelta(hours=7)).strftime('%d-%b-%Y %H-%M-%S')+'.png'
    
    if attachment:
        att = MIMEImage(attach_file, _subtype='png')
        att.add_header('Content-Disposition', 'attachment', filename=file_name)
        # att = MIMEApplication(attachment.read(), _subtype='txt')
        # att.add_header('Content-Disposition', 'attachment', filename=attachment.name)
        message.attach(att)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.ehlo()
    server.login(sender, password)
    text = message.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()


SENDER_ADDRESS='cobacobavg@gmail.com'
PORT='587'
SMTP_SERVER_ADDRESS='smtp.gmail.com'
SENDER_PASSWORD='jrsi ommh hacv lrpq'

if __name__ == '__main__' :


    # start_camera = st.button("Start Camera", type="secondary", use_container_width=True, key='start_camera_button')
    # if start_camera:
    data = {
        "Foto Temuan" : [],
        "Lokasi": [],
        "Keterangan": [],
        "Rekomendasi" : []
        }


    if 'df1' not in st.session_state:
        df1 = pd.DataFrame(data)
        st.session_state.df1 = df1
    
    df1 = st.session_state.df1
    st.sidebar.write(df1)
    
    picture = st.camera_input("Take a picture")



    if picture is not None:
        # To read image file buffer with OpenCV:
        bytes_data = picture.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        result_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

        st.image(result_img)

        with st.form("Input Form"):
            user_location_input = st.text_input(label="Lokasi Temuan", placeholder="Please enter location of finding")
            user_description_input = st.text_input(label="Deskripsi Temuan", placeholder="Please enter description of finding")
            save_data = st.form_submit_button(label="Save Data")
            # _ , image_in_excel = cv2.imencode('.png', result_img, [cv2.IMWRITE_JPEG_QUALITY, 100])
            img_pil = Image.fromarray(result_img)
            if save_data :
                new_row = pd.DataFrame({
                    "Foto Temuan" : [img_pil],
                    "Lokasi": [user_location_input],
                    "Keterangan": [user_description_input],
                    "Rekomendasi" : [None]})
                st.session_state.df1 = pd.concat([st.session_state.df1, new_row])
                st.write(st.session_state.df1)

                current_directory = os.getcwd()
                result_path = os.path.join(current_directory, r'result', str((datetime.today() + timedelta(hours=7)).strftime('%d-%b-%Y')))
                if not os.path.exists(result_path):
                    os.makedirs(result_path)
                writer = pd.ExcelWriter(result_path+str('/result.xlsx'), engine='xlsxwriter')
                st.session_state.df1.to_excel(writer, sheet_name="Sheet1", startrow=0, header=True, index=False)
                workbook  = writer.book
                worksheet = writer.sheets["Sheet1"]
                # worksheet = workbook.add_worksheet()

                for i, image in enumerate(st.session_state.df1["Foto Temuan"]):
                    image_path = os.path.join(current_directory, r'result', str((datetime.today() + timedelta(hours=7)).strftime('%d-%b-%Y')))
                    if os.path.exists(image_path) == False:
                        os.mkdir(image_path)
                    image.save(f"{image_path}/img_{i}.png", "PNG") # Save your image before inserting
                    worksheet.insert_image(i+1, 0, f"{image_path}/img_{i}.png")

                writer.save()



    # with st.form("Email Form"):
    #     subject = st.text_input(label="Subject", placeholder="Please enter subject of your mail")
    #     fullName = st.text_input(label="Full Name", placeholder="Please enter your full name")
    #     email = st.text_input(label="Email address", placeholder="Please enter your email address")
    #     text = st.text_area(label="Email text", placeholder="Please enter your text here")
    #     # uploaded_file = st.file_uploader("Attachment")
    #     attachment , uploaded_file = cv2.imencode('.png', result_img, [cv2.IMWRITE_JPEG_QUALITY, 100])
    #     submit_res = st.form_submit_button(label="Send")

    #     if submit_res:
    #         extra_info = """

    #         ----------------------------------------------

    #         Email Address of sender {} \n
            
    #         Sender Full Name {} \n

    #         ---------------------------------------------- \n \n


    #         """.format(email, fullName)

    #         message = extra_info + text

    #         st.write("SENDER : ", SENDER_ADDRESS)
    #         st.write("SENT TO :", email)
    #         # st.write("PORT", PORT)


    #         send_email(sender=SENDER_ADDRESS, password=SENDER_PASSWORD, receiver=email, smtp_server=SMTP_SERVER_ADDRESS, smtp_port=PORT, email_message=message, subject=subject, attachment=attachment, attach_file=uploaded_file)
    #         st.success('Email has been sent')





