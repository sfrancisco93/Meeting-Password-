#!/usr/local/bin/python3

from jose import jwt # used to programmatically generate a JWT token.
import time
import json
import requests
import csv

##
# Generate JWT Token
##

api_key = ''
api_secret = ''
exp = int(time.time()+600)
payload = {'iss': api_key, 'exp': exp}
encoded = jwt.encode(payload, api_secret)
print(encoded)

##
# GET https://api.zoom.us/v2/users
#	# Obtain all the users in the account
# 	# For each User in the Zoom account:
#		# GET https://api.zoom.us/v2/<user_email>/settings
#			# Return 'schedule_meeting.use_pmi_for_scheduled_meetings', 'schedule_meeting.use_pmi_for_instant_meetings'
##

userDict = { } # User Dictionary Format: <user_email>: ['schedule_meeting.use_pmi_for_scheduled_meetings', 'schedule_meeting.use_pmi_for_instant_meetings']

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


lastPage = False

while not lastPage:
	response = requests.get(getUserEndpoint, headers=getUserHeaders, params=getUserParams)
	resp = json.loads(response.content)
	for item in resp['users']:
		getUserSettingsEndpoint = 'https://api.zoom.us/v2/users/' + item['email'] + '/settings'
		responseq = requests.get(getUserSettingsEndpoint, headers=getUserSettingsHeaders, params=getUserSettingsParams)
		respq = json.loads(responseq.content)
		try:
			print('%s: %s, %s' % (item['email'], respq['schedule_meeting']['use_pmi_for_scheduled_meetings'], respq['schedule_meeting']['use_pmi_for_instant_meetings']))
			userDict[item['email']] = [respq['schedule_meeting']['use_pmi_for_scheduled_meetings'], respq['schedule_meeting']['use_pmi_for_instant_meetings']]
		except KeyError:
			print(resp)
	if(resp['page_number'] == resp['page_count']):
		lastPage = True
	else:
		page_number = page_number + 1
		getUserParams = {
			'page_size' : '10',
			'page_number': page_number
		}
value = input('Process is complete. Save to CSV? Y/n: ')
if(value == 'Y' or value == 'y'):
	with open('User PMI Settings.csv', 'w') as file:
		headers = ['E-mail', 'Use PMI for Scheduled Meetings', 'Use PMI for Instant Meetings']
		writer = csv.DictWriter(file, fieldnames=headers)
		writer.writeheader()
		for item in userDict:
			writer.writerow({'E-mail': item, 'Use PMI for Scheduled Meetings' : userDict[item][0], 'Use PMI for Instant Meetings': userDict[item][1]})
	file.close()
	print('CSV has been saved.')
print('Terminating...')
