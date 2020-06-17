# caerus by precedented

## Roster

- **Vishwaa Sofat**: Project Manager and Success.
- **Kazi Jamal**: Opportunity bulletin, scholarship finder
- **Eric Lau**: OAuth, accounts, reminders/notifications
- **Raymond Lee**: Opportunity bulletin, scholarship finder
- **Ahmed Sultan**: UI/UX, routing, form submission, productivity

## Description

Caerus is a website based off of Mr. Blumm's weekly Opportunity Bulletin, where students at Stuyvesant can search through a database of opportunities, internships and scholarships curated by Mr. Blumm and Stuyvesant faculty.

## Video Demo

[video demo here](https://www.youtube.com/watch?v=cPlkgKidTiU&feature=youtu.be)

## APIs Used

- [Google OAuth2 API](https://docs.google.com/document/u/3/d/1ByvzxoEhH1UuHJR2RW2w5-unr6sOeJBm9Hh-YFq3RSw): Retrieves basic information from a user's Google account. We use it for authentication and to get the email, name, and picture from a user's account.

## Instructions

### Assuming python3 and pip are already installed

### Virtual Environment

- To prevent conflicts with globally installed packages, it is recommended to run everything below in a virtual environment.

Set up a virtual environment by running the following in your terminal:

```shell
python -m venv hero
# replace hero with anything you want
# If the above does not work, run with python3 (this may be the case if a version of python2 is also installed)
```

To enter your virtual environment, run the following:

```shell
. hero/bin/activate
```

To exit your virtual environment, run the following:

```shell
deactivate
```

### Cloning

Run the following commands in your terminal

```shell
git clone https://github.com/vsofat/caerus.git

cd caerus
```

### Dependencies

Run the following line in your virtual environment

```shell
pip install -r requirements.txt
```

### Launch Codes

#### Google OAuth 2.0 Client

1. Head over to the [Google API Console](https://console.developers.google.com/projectselector2) and create a new project.
2. Click on the OAuth consent screen tab and select the External option.
3. Name the application and click save.
4. Click on the Credentials tab and click **CREATE CREDENTIALS**.
5. Select the OAuth client ID option.
6. Choose web application as the Application type.
7. Add <http://127.0.0.1:5000> as an Authorized JavaScript origin.
8. Add <http://127.0.0.1:5000/redirect> as an Authorized redirect URI.
9. Create the project and click **OK**.
10. Click the download button on the right-hand side of the OAuth 2.0 Client ID.
11. Rename the file to `oauth-client.json` and place it in the root of this repository.

The file should look like this:

```json
{
    "web": {
        "client_id": "",
        "project_id": "",
        "auth_uri": "",
        "token_uri": "",
        "auth_provider_x509_cert_url": "",
        "client_secret": "",
        "redirect_uris": [],
        "javascript_origins": []
    }
}
```

### Running

Run the following line in your virtual environment

```shell
python3 app/__init__.py
```

Open a browser and head to <http://127.0.0.1:5000/>
