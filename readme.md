# Zoom Meeting Password Configuration
This tool will allow Zoom Administrators to determine which of their users have enabled the following settings:
* Use PMI for Instant Meetings
* Use PMI for Scheduled Meetings

For security purposes, it would be best not to use your PMI for all of your meetings. A Meeting ID is just like a phone number, so anyone that dials it will attempt to enter your meeting.

## Two tools
* 'main.py' returns to you a CSV file of all users. The downside is that it is written synchronously so it may take about 10 minutes per 1000 users.
* 'multi.py' is asynchrnous so can complete within seconds, but the CSV file creation I have not yet achieved. I am having trouble determining how to asynchrnously update a global dictionary (this dictionary stores all of the user information, then writes to a CSV file)

## Future Implementations:
* Improve multi.py so main.py can be deprecated.
* Add user input functionality such that user can ask for other lists (i.e. only users with PMI for instant meetings enabled)

## Suggestions
* These tools are created just for self-development and learning purposes. _Please use this tool at your own risk._ I am not responsible for any unexpected changes to your Zoom account due to the usage of this script.
* For any feedback, bugs, feature requests, or anything similar, please reach out to me at sfrancisco93@gmail.com
