# ipChecker
To facilitate running a home web server behind a router, this script checks to see if external IP has changed, alerts user via email, and updates dynamic DNS rules via the domains.google API.

### Update:
Now universally accessible. Windows/Mac/Linux it will ask for your details on first run. I also added command line options/arguments (see `./ipchecker.py --help`) for loading/deleting a user and changing credentials/settings.


### Installation:

Install requirements:

`pip install -r requirements.txt`

Simply run the script with Python 3.6+. On first run, you will need your Dynamic DNS autogenerated username and password as described in [the documentation.](https://support.google.com/domains/answer/6147083?hl=en-CA) If you choose to receive email notifications, you will be asked to input your gmail email address and password which will then be encoded before being saved. (The notification is sent from the user's own email address via the gmail smtp server, you will need to allow less secure apps on your Google account to use.). For more info on how to set up Dynamic DNS and the process I went through writing this script check [this article.](https://mjfullstack.medium.com/running-a-home-web-server-without-a-static-ip-using-google-domains-python-saves-the-day-246570b26d88)

After initial setup, the script takes care of everything: if your IP has changed since you last ran it, it will update your Dynamic DNS rule on domains.google.com.



On **Windows** you can use Task Scheduler; on **Linux/Mac**, simply add `ipchecker.py` to your crontab (mark as executable with `chmod +x ipchecker.py`) and you can choose the frequency of the checks. My crontab entry looks like this:

`0 * * * * /home/me/ipChecker/ipchecker.py >> ~/cron.log 2>&1`


Logs to `ipchecker.log` in the same directory and stdout so that the logs also appear in the cron log. Check the logs if the script does not run as expected, or to see when the IP was last checked.

If you forget your IP or need to check it for any reason, running `ipchecker.py` without options will log your current IP to the terminal. 

As well as the command line options, to change your user details or delete them, you can also just delete the `/.user` file.
