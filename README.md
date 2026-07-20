## What is this?

It all started from my laziness to log in and check-in to report presence for multiple accounts because of community rules. Then I have an idea about **how to automate them**.

I'm still learning programming, so this might not be the most efficient way, but it's the best that I can do at this time. Wonder if you're in the same community as me, and if so, this code might be helpfull to you too. 

## Use

#### Clone this repository

```
git clone https://github.com/Kanaede/sleman.app.pbx-pr-automation.git
cd ./sleman.app.pbx-pr-automation
```

or just download the source code

#### Create venv and install the dependencies

```
venv -m venv venv
pip install -r requirements.txt
```

#### Environment

Create `.env` file and save it next to the `main.py`

Create a variable

```
LOGIN_SERVER = <change this to web login page>
```

#### Save account to yaml

Remove `.example` from accounts.yaml.example

Put your email and password, multiple accounts supported

## Contribute

This code is powered by PyDoll. Thanks to them because I was able to bypass Cloudflare on the site.

If you're in the same community as me, you can help implement similar site support. How do you know if you're in the same community? After reading the project title, if you know what community it is referring to, then you know.

There was some community sites, and I only has access to one of them. Because of this code based on PyDoll, I need to know the other site's structure before implement the code. If you don't know how to code but want to help or share an idea, just contact me or open an issue.

I'm not planning to expand the feature or add supported sites more than just to help people in the same community.

This code is not affiliated, partnered or part of the official community. This code exist because I want to simplified the fill in the attendance/presence with more than one account, every day.

> A special community always in a special, surprising and different way.