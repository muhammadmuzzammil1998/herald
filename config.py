# API and Device configurations #

api_key = ""                         #Bolt user API key
device_id = ""                       #Bolt device ID
cooldown = 10                        #Cooldown after an unsuccessful api call to device in seconds
frame_size = 5                       #Frame size for computing z-score
factor = 2                           #Factor for computing z-score
api_limit_per_minute = 20            #Ratelimit for the API requests per minute
api_limit_margin = 4                 #API calls to leave as margin
interval = 60 / (api_limit_per_minute - api_limit_margin) #Optional edit: Interval for checking status

# Email configurations #

smtp_server = ":587"                            #SMTP server with port in format smtp.gmail.com:587
sender_name = "Herald - the intrusion detector" #Sender's name to display
sender_email = ""                               #Username for SMTP server
sender_password = ""                            #Password for SMTP server
recipients = ""                                 #Single recipient in string or a list of recipients in array form
