import logging
import logging.handlers
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread
from time import sleep

sender = ""
sender_pass = ""
recipient = ""

def setup_logging(logger_name):
    
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)5s %(name)7s %(thread)d - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger

logger = setup_logging('threadz') 


def send_email(to_address, subject, text, html):
    '''
    Given an email address, a subject, and a body, this function 
    will create and send an email out from mycoinfolio@gmail.com
    '''
    
    try:
        logger.info(f'Composing Email for {to_address}')
        from_address = sender
        
        
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = to_address    
    
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)
        
        # Send the message via gmail SMTP server.
        s = smtplib.SMTP("smtp.gmail.com:587")
        s.starttls()
        s.login(sender,sender_pass)
        s.sendmail(from_address, to_address, msg.as_string())
        logger.info(f'Email sent to {to_address}')
        s.quit()    

    except Exception as e:
        logger.error(f'Error sending email: {e}')

def main():
    
    threadz = []
    
    for number in range(5):
        logger.info(f'sending email')
        t = Thread(target = send_email, args = (recipient,'thread testing','test','test'))
        t.daemon = True
        t.start()
        threadz.append(t)
        
    for x in threadz:
        x.join()
        logger.info(f'joining threads')

    
    logger.info(f'done')
        
    
if __name__ == "__main__":
    main()