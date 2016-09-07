import  imaplib, subprocess
from jabberbot import *
import threading
import time 
import logging
import email
from email.parser import Parser


def message_cleanup(inp):
    headers = Parser().parsestr(inp)
    sender = headers['from']
    subject = headers['subject']
    inp = email.message_from_string(inp)
    if inp.is_multipart():
        for payload in inp.get_payload():
            return str(sender +' | '+ subject +' | '+ payload.get_payload())
    else:
        return str(sender +' | '+ subject +' | '+ inp.get_payload())

    return str(sender +' | '+ subject +' | '+ inp)

def getalertemails():
    cleaned_msgs = []
    M = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    email = "<<insert gmail email here>>"
    password = "<<insert gmail password here>>"
    M.login(email, password)
    M.select()
    typ, data = M.search(None, 'SUBJECT', " ")
    #typ, data = M.Se
    
    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        #print data[0][1]
        foo = message_cleanup(data[0][1])
        cleaned_msgs.append(foo)
        M.store(num, '+FLAGS', '\\Deleted')
    #print cleaned_msgs[1]
    return '********************\n'.join(cleaned_msgs)
    M.expunge()
    M.close()
    M.logout()


(JID, PASSWORD) = ('<<INSERT JID HERE>>','<<INSERT JID PASSWORD HERE>>')


class IMAP_ForwarderBot(JabberBot):

    def __init__( self, jid, password, res = None):
        super( IMAP_ForwarderBot, self).__init__( jid, password, res)
        # create console handler
        chandler = logging.StreamHandler()
        # create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # add formatter to handler
        chandler.setFormatter(formatter)
        # add handler to logger
        self.log.addHandler(chandler)
        # set level to INFO
        self.log.setLevel(logging.INFO)

        self.users = []
        self.message_queue = []
        self.thread_killed = False

    def thread_proc( self):
        user = '<<INSERT RECIPIENT JID>>'
        while not self.thread_killed:
            self.send(user, getalertemails())
            for i in range(60):
                time.sleep( 1)
                if self.thread_killed:
                    return 

username="<<INSERT BOT JID HERE>>"
password="<<INSERT BOT PW HERE>>"
alert_bot = IMAP_ForwarderBot(username, password)
th = threading.Thread( target = alert_bot.thread_proc)
alert_bot.serve_forever(connect_callback = lambda: th.start())
alert_bot.thread_killed = True
