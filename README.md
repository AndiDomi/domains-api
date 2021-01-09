# Google Domains API Client
To facilitate running a home web server behind a router without a static IP, this package checks to see if your external IP has changed and automatically updates your Dynamic DNS rules on Google Domains, via the API; also notifies user by email if required.

### Installation (Python 3.6+):
`pip install domains-api`

### Usage:
Can be run from the command line like so:

`python -m domains_api`

or imported into your projects in the normal way*:
```
>>>from domains_api import IPChanger
>>>ipchanger = IPChanger()
>>>ipchanger.user.domain
example.com
```

*See below for an example with Django and Apache2.

Windows/Mac or Linux, it will ask for your credentials on first run and then shouldn't need any input after that. I added command line options/arguments (see `python domains_api --help`) for loading/deleting a profile and changing credentials/settings more easily. On POSIX systems you will need to run with 'sudo' first.

You will need your Dynamic DNS autogenerated username and password as described in [this documentation.](https://support.google.com/domains/answer/6147083?hl=en-CA) For more info on how to set up Dynamic DNS and the process I went through writing this script check [this blog post.](https://mjfullstack.medium.com/running-a-home-web-server-without-a-static-ip-using-google-domains-python-saves-the-day-246570b26d88)

If you choose to receive email notifications, you will be asked to input your gmail email address and password which will then be encoded before being saved as part of a User instance. (The notification is sent from the user's own email address via the gmail smtp server, you will need to allow less secure apps on your Google account to use.).

On **Windows** you can use Task Scheduler; on **Linux/Mac**, add a line to your crontab and you can choose the frequency of the checks. An example hourly cron job would look like this:

`0 * * * * python3 -m domains_api >> ~/cron.log 2>&1`

If reducing downtime is essential, you could increase the frequency of checks to every 5 minutes, or even less, like this:

`*/5 * * * * ...etc`

On Google Domains the default TTL for Dynamic DNS is 1 min, but unless you expect your external IP to change very frequently, more regular cron jobs might be a slight waste of resources; even so, the script is very light weight and usually only takes just over a second to run normally on a Rasberry Pi 3 Ubuntu server.

Check `~/cron.log` if the script does not run as expected, or to see when the IP was last checked.

The logs are written to both `/var/www/domains-api/domains.log` (posix) or `%LOCALAPPDATA%/domains-api/domains.log` (win), and stdout, so that they also appear in the terminal (&/ cron log).

After initial setup, the script takes care of everything: if your IP has changed since you last ran it, it will update your Dynamic DNS rule on domains.google.com.

If you forget your IP or need to check it for any reason, running:

`python -m domains_api -i` 

...will log your current external IP to the terminal without doing anything else.

Other options include:

    domains-api help manual (command line options):
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    You will need your autogenerated Dynamic DNS keys from
    https://domains.google.com/registrar/example.com/dns
    to create a user profile.
    
    python -m domains_api                    || -run the script normally without arguments
    python -m domains_api -h --help          || -show this help manual
    python -m domains_api -i --ip            || -show current external IP address
    python -m domains_api -c --credentials   || -change API credentials
    python -m domains_api -e --email         || -email set up wizard > use to delete email credentials (choose 'n')
    python -m domains_api -n --notifications || -toggle email notification settings > will not delete email address
    python -m domains_api -u user.file       || (or "--user_load path/to/user.file") -load user from pickle file
    python -m domains_api -d --delete_user   || -delete current user profile
                                             || User file is saved as "/var/www/domains_api/domains.user"

### Example in Django/Apache2 application:

In your Django virtual environment (recommended):

`pip install domains-api APScheduler==3.6.3`

Then, in your project you can create a new module called ipChanger in your project's root directory, with an empty `__init__.py` file and an `ip_changer.py` file.

`ip_changer.py` should look something like this:

```
from apscheduler.schedulers.background import BackgroundScheduler
from domains_api import IPChanger


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(IPChanger, 'interval', minutes=10)
    scheduler.start()
```

Careful not to call `IPChanger` within the `add_job()` method (no parentheses).

Then you will need to add the following to your main app's `apps.py` file:

```
class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        from ipChanger import ip_changer
        ip_changer.start()
```
Before you fire up / restart your server you will need to run the script with `sudo` first, so that the appropriate permissions can be set to enable the Apache2 user (www-data) to create/update the log and user configuration files (in `var/www/domains-api/`). If you are running from within a virtual environment (recommended) you will need to specify the virtual environment's python path or sudo will use the root-owned one (`sudo venv/bin/python -m domains_api`). You will then be asked to input your credentials as above. After this process is complete, you can restart your web server. Check `cat /var/log/apache2/error.log` (all logs - they are logged as mod_wsgi errors) and `/var/www/domains-api/domains-api.log` (warnings only) to see everything is working as expected.