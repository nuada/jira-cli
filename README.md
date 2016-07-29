# JIRA CLI

Simple toolkit for accessing information from JIRA using CLI.


## Dependencies

Setup using [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html):

```
mkvirtualenv jira-cli
workon jira-cli
pip install -r requirements.txt
```

## Setup

1. Generate key pair using `mkkey.sh`
1. Create OAuth consumer at "Application links" [https://<jira_host>/plugins/servlet/applinks/listApplicationLinks](https://<jira_host>/plugins/servlet/applinks/listApplicationLinks)
 * URL: `http://localhost` -> "Create new link" -> "Continue"
 * Set applicaion name: `jira-cli`
2. Edit link "jira-cli"
 * Switch to "Incoming Authentiction"
 * Set required fields
    * Consumer Key - `jira-cli`
    * Consumer Name - `jira-cli`
    * Public key - copy from file `public_key.pem` generated in step 1.
3. Authenticate to OAuth endpoint using: `jira-auth.py https://<jira_host> <consumer_key>`
