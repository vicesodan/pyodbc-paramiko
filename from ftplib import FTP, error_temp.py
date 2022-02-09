from os import listdir, path
from datetime import datetime, timedelta
from configparser import ConfigParser
import smtplib


def check_folder(folder_path, dt_now, match_list=[]): 
    files = [path.join(folder_path, f) for f in listdir(folder_path) if path.isfile(path.join(folder_path, f))]
    new_files = []
    msg = ""
    for file in files:
        file_md = datetime.fromtimestamp(path.getmtime(file))
        if dt_now - timedelta(minutes=6) < file_md:
            new_files.append(file)
    for match in match_list:
        cnt = 0
        for new_file in new_files:
            if match in new_file:
                cnt += 1
                if cnt == 2:
                    break
        else:
            msg += "\n\nNedostaje " + match + " datoteka u mapi " + folder_path
            print("Nedostaje", match, "datoteka u mapi", folder_path, "Vrijeme provjere:", dt_now)
    return msg

    
if __name__ == "__main__":
    # Get current time
    year, month, day, hour, minutes = datetime.now().strftime("%Y %m %d %H %M").split(' ')
    time_now = datetime(int(year), int(month), int(day), int(hour), int(minutes))

    # Read config file
    config = ConfigParser()
    config.read("alarm_config.ini")

    # Write email
    host = config["email"]["host"]
    sender = config["email"]["sender"]
    receivers = config["email"]["receivers"].split(';')
    
    msg_from = "From: " + sender.split('@')[0] + " <" + sender + ">\n"
    
    msg_to = "To: "
    for receiver in receivers:
        msg_to += receiver + ";"
    msg_to += "\n"
    
    msg_subject = "Subject: " + config["email"]["subject"] + "\n"
    msg_body = "\nProvjera za: " + (time_now - timedelta(minutes=4)).strftime("%d.%m.%Y. %H:%M")
    msg_body += check_folder("D:/Data Files/HOPS/IMPORT/SN", time_now, match_list=["_SSH_", "_SV_", "_TP_"])


    # If True send a email
    if msg_body != "\nProvjera za: " + (time_now - timedelta(minutes=4)).strftime("%d.%m.%Y. %H:%M"):
        # Send email
        message = msg_from + msg_to + msg_subject + msg_body
        try:
            smtp_obj = smtplib.SMTP(host=host)
            smtp_obj.sendmail(sender, receivers, message)
            print("Successfully sent email")
        except SMTPException:
            print("Error: Unable to send email")
    else:
        print("No need for alarming anyone!")
    
    
    
    

    
