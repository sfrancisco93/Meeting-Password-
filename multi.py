#!/usr/local/bin/python3

from multiprocessing import Pool
from jose import jwt
import time
import json
import requests
import csv


api_key = ''
api_secret = ''
exp = int(time.time()+600)
payload = {'iss': api_key, 'exp': exp}
encoded = jwt.encode(payload, api_secret)
print(encoded)

userDict = { }
userList = []
page_number = 1
count = 1

getUserHeaders = {
    'authorization' : 'Bearer ' + encoded,
    'content-type' : 'application/json'
}

page_number = 1 # Will be incremented to paginate
getUserParams = {
    'page_size' : '300',
    'page_number': page_number
}

getUserEndpoint = 'https://api.zoom.us/v2/users'

getUserSettingsHeaders = {
    'authorization' : 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IjZ4eHN1dVFuUmtXZXplQldtd29PTVEiLCJleHAiOjE1ODU5NDUxMjksImlhdCI6MTU4NTg1ODcyOX0._24yrmc8VkAlQljYEgkhHM94DFh-ZgKFB6AkS0TnpxE',
    'content-type' : 'application/json'
}

getUserSettingsParams = {
    # n/a
}

def f(x):
    getUserParams = {
    'page_size' : '10',
    'page_number': x
    }
    getUserEndpoint = 'https://api.zoom.us/v2/users'
    response = requests.get(getUserEndpoint, headers=getUserHeaders, params=getUserParams)
    resp = json.loads(response.content)
    for item in resp['users']:
        count = count + 1
        getUserSettingsEndpoint = 'https://api.zoom.us/v2/users/' + item['email'] + '/settings'
        responseq = requests.get(getUserSettingsEndpoint, headers=getUserSettingsHeaders, params=getUserSettingsParams)
        respq = json.loads(responseq.content)
        try:
            print('%s: %s, %s' % (item['email'], respq['schedule_meeting']['use_pmi_for_scheduled_meetings'], respq['schedule_meeting']['use_pmi_for_instant_meetings']))
            userDict[item['email']] = [respq['schedule_meeting']['use_pmi_for_scheduled_meetings'], respq['schedule_meeting']['use_pmi_for_instant_meetings']]
        except KeyError:
            print(resp)
    return(resp['page_number'])

def h(x):
    with open('User PMI Settings.csv', 'w') as file:
        headers = ['E-mail', 'Use PMI for Scheduled Meetings', 'Use PMI for Instant Meetings']
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for item in userDict:
            writer.writerow({'E-mail': item, 'Use PMI for Scheduled Meetings' : userDict[item][0], 'Use PMI for Instant Meetings': userDict[item][1]})
            return item

if __name__ == '__main__':
    getUserEndpoint = 'https://api.zoom.us/v2/users'
    response = requests.get(getUserEndpoint, headers=getUserHeaders, params=getUserParams)
    resp = json.loads(response.content)
    page_list = []
    print(resp['page_count'])
    page_num = 1
    count_num = 1
    while page_num <= resp['page_count']:
        page_list.append(page_num)
        page_num = page_num + 1
    with Pool(10) as p:
        print(p.map(f, page_list))
        while count_num < count:
            print(p.map(h, page_list))

    value = input('Process is complete. Save to CSV? Y/n: ')
