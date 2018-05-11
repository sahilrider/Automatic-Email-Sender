import smtplib
import csv
from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

MY_ADDRESS = 'YourEmailAddress'
PASSWORD = 'YourPassword'

'''
    CSV file containing list of contacts in format.
        S.No    Name    Email Id
'''
def get_contacts(filename):
    names = []
    emails = []
    cr=csv.reader(open('sahil.csv','r'))
    for a_contact in cr:
        names.append(a_contact[1])
        emails.append(a_contact[2])
    return names, emails

'''
Function to read template for email body
text file : for simple email body
html file : if formatting is required (can use online doc to html converter)
'''
def read_template(filename):
    with open(filename, 'r') as template_file:
        template_file_content = template_file.read()
    return template_file_content

def main():
    names, emails = get_contacts('sahil.csv') 
    message1 = read_template('cfp_email-body1.html')
    message2 = read_template('cfp_email-body2.html')

    #smtp server setup
    #you need to give access to less secure apps from your gmail account
    s = smtplib.SMTP_SSL('smtp.gmail.com',465)
    s.login(MY_ADDRESS, PASSWORD)

    
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       

        message_template = Template("Dear ${PERSON_NAME},")
        message3 = message_template.substitute(PERSON_NAME=name.title())

        message=message1+ message3 +message2
 
        message=MIMEText(message,'html')

        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']="Automated Email System"
        
        msg.attach(message)

        #Attachment 1 
        filename = "attach_1.pdf"
        attachment = open("attach_1.pdf", "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)  #to add header to the attachment to be sent
        msg.attach(p)

        #Attachment 2
        filename = "attach_2.pdf"
        attachment = open("attach_2.pdf", "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)  #to add header to the attachment to be sent
        msg.attach(p)
        s.sendmail(MY_ADDRESS,email,msg.as_string())
        
    s.quit()    #end server
    
if __name__ == '__main__':
    main()