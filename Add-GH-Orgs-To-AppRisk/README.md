# What is this tool for? <br>

This tool will configure the GitHub integration for AppRisk. <br>
The benefit is that you can add GitHub Profile with multiple GitHub Orgs in one request.


## Prerequisites:
- Snyk Group Id
- GitHub Token
- CSV that contains all your GitHub Org names.

## Installation instructions:

Clone this repo and run <pre><code>pip3 install -r requirements.txt</pre></code><br>

## How do I use this tool?<br>

Edit the CSV  or add your own CSV that includes the GitHub Orgs

Update the config.json to include the following:
- Snyk Group Id
- The name of the Profile for the integration
- GitHub token
- The name of the CSV file

## Example:
```python
 python3 ./add-GH-Orgs-To-Apprisk.py
```





