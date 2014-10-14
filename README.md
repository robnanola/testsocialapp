TEST SOCIAL APP
===


- Standard Django Registration
- Facebook Login Integration
- Personal "Profiles" where you can set information about yourself
- Upload Photos to Profile
- Set already-uploaded photo as Profile Picture
- View other profile's Information and Wall
- Post to your own Wall
- Post to another profile's wall
- Comment system for all Wall Posts
- Simple Search for finding Other Profiles


FACEBOOK API Settings
---

App Secret: ****

url: ****

App ID: *****



SETTING UP
---

1. virtualenv --no-site-packages --distribute /path/to/env

2. source /path/to/env/bin/activate

3. pip install -r requirements.txt

4. define outsourced-demo.com in you /etc/hosts (used for facebook login integration)

    # NOTE since the facebook app used by this demo is not yet live it will return an error.
    # you may create your own facebook app then just configure the settings

    $ sudo vi /etc/hosts
    # and paste the line below
    127.0.0.1 outsourced-demo.com

5. Set EMAIL related settings in local_settings.py 

6. python manage.py buildwatson

7. python manage.py installwatson

8. python manage.py runserver 


