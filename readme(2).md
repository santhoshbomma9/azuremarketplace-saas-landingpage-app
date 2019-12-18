---
page_type: sample
languages:
- python
products:
- azure
---

# Partner Center integration sample (Python)

<!-- 
Guidelines on README format: https://review.docs.microsoft.com/help/onboard/admin/samples/concepts/readme-template?branch=master

Guidance on onboarding samples to docs.microsoft.com/samples: https://review.docs.microsoft.com/help/onboard/admin/samples/process/onboarding?branch=master

Taxonomies for products and languages: https://review.docs.microsoft.com/new-hope/information-architecture/metadata/taxonomies?branch=master
-->

This sample implements basic functions required to integrate a solution into the [Azure Marketplace](https://azuremarketplace.microsoft.com) or [Microsoft AppSource](https://appsource.microsoft.com). The sample is written in Python, and provides the basic code that communicates to the marketplace using REST APIs.

## Contents

The repository contains these files.

| File/folder       | Description                                |
|-------------------|--------------------------------------------|
| `amp_app`         | Code for sample pages.                     |
| `.dockerigore`    | Optional. Docker build commands.           |
| `.gitignore`      | Define what to ignore at commit time.      |
| `Dockerfile  `    | Docker build commands                      |
| `LICENSE        ` | The license for the sample.               |
| `README.md`       | This README file.                          |
| `requirements.txt`| The list of code extensions needed.        |
| 'startup.py'       | Entry point for Python. |

## Prerequisites

Familiarity with Python is required. You must also have the following:

- [Microsoft Partner Center account](https://partner.microsoft.com/en-us/dashboard/home)
- Azure Active Directory app registration

## Setup

You must have a development environment such as Visual Studio Code to edit the code. Use below steps to setup:

1. Install [Python](https://www.python.org/downloads/)
2. Create a Virtual Env

    `python -m venv env`  
    `env\Scripts\activate`
3. Install requirements

    `pip install -r requirements.txt`

4. Set the required environment variables


| KEY           | VALUE       |
| ------------- |-------------|
| TENANT_ID     | `Multi Tenant App Azure AD App Registration` |
| CLIENT_ID | `Multi Tenant App Azure AD App Registration`  |
| CLIENT_SECRET  | `Multi Tenant App Azure AD App Registration`  |
| MARKETPLACEAPI_TENANTID | `Single Tenant App Azure AD App Registration`  |
| MARKETPLACEAPI_CLIENT_ID | `Single Tenant App Azure AD App Registration`  |
| MARKETPLACEAPI_CLIENT_SECRET | `Single Tenant App Azure AD App Registration`  |
| STORAGE_CONNECTION_STRING | `Coneection string for Azure Storage` |
| WEBHOOK_OPS_STORAGE_TABLE_NAME | `Table for Webhook Operations` |
| ISV_OPS_STORAGE_TABLE_NAME | `Table for ISV Operations` |
| DIMENSION_USAGE_STORAGE_TABLE_NAME | `Table for Dimension Operations` |
| MARKETPLACEAPI_API_VERSION | `?api-version=2018-08-31(prod), ?api-version=2018-09-15(mock)` |
| HTTP_SCHEME | `HTTP / HTTPS` |
| SENDGRID_APIKEY | `For Notification sending emails` |
| SENDGRID_FROM_EMAIL | `For Notification sending emails` |
| SENDGRID_TO_EMAIL | `For Notification sending emails` |
| Dimension_Data | Hardcoding dimensions e.g. `{"santhosh_saas_test-preview": ["persms"], "contoso_saas_offer-preview": ["persms"]}` |



## Running the sample

Local:
Goto Debug, Select _Python:Flask_ configuration and run

Azure App Service:
The sample can be deployed on Azure App Service.  

## Key concepts

See the [SaaS fulfillment APIs, version 2](https://docs.microsoft.com/azure/marketplace/partner-center-portal/pc-saas-fulfillment-api-v2)

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.