from firebase import firebase
import json
import reddit
import time
import urllib2
import sendgrid
import sys
firebase = firebase.FirebaseApplication('https://blistering-fire-9098.firebaseio.com', None)

send_grid_password = sys.argv[1]

def get_count_url(url):
    try:
        if url[-5:]!= ".json":
            url = url+".json"
        print "checking " + url
        response = urllib2.urlopen(url)
        js = json.load(response) 
    except Exception as e:
        print e
        print "sleeping for 10 before requesting again"
        time.sleep(20)
        get_count_url(url)
        return
    count = reddit.get_comment_count(js)
    print str(url) + " has " + str(count)
    return count

def email(person):
    sg = sendgrid.SendGridClient('DaxEarl', send_grid_password)
    message = sendgrid.Mail()
    message.add_to(person["email"])
    message.set_subject('Your Reddit Ama Is Ready!')
    message.set_html('Body')
    message.set_text('Your ama is availibe at available at  ')
    message.set_from('easyAMA<easyAma@sendgrid.net>')
    status, msg = sg.send(message)
    print status,msg
    print "sent "+person["email"] +" an email"

while True:
    result = firebase.get('/', None)
    for x in range(10):
        for k in result:
            person = result[k]
            if person["trigger"]=="count":
                if get_count_url(person["thread"])>person["min"]:
                    print "Emailing "+str(person["email"])
                    email(person)
                    print "Removing "+str(person["email"])
                    firebase.delete('/',k)
                    print "Deleted!"
                time.sleep(20)
