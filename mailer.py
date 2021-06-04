import smtplib, ssl
from email.mime import multipart as msg, text as body

def send(server, sender, recipients, subject, text, password = "", name = ""):
    serverInfo = server.split(":")
    if type(recipients) != type([]):
        recipients = list([recipients])

    with smtplib.SMTP(serverInfo[0], serverInfo[1]) as smtp:
        smtp.starttls(context = ssl.create_default_context())
        smtp.login(sender, password)

        if name != "":
            sender = f"{name} <{sender}>"

        message = msg.MIMEMultipart()
        message["Subject"] = subject
        message["From"] = sender
        message.attach(body.MIMEText(text, 'plain'))

        for i in recipients:
            message["To"] = i
            smtp.sendmail(sender, i, message.as_string())
