# Azure Marketplace SaaS Offer Integration Sample Application (WORK IN PROGRESS)

## Simple Disclaimer
**This application is a sample only and must be treated that way. It is NOT a production level code. It is written for my personal use.**  

## SaaS Offer background
If you are here and wondering what this sample is all about, please continue to read otherwise feel free to skip and continue to the next section. The intended audience for this sample is a **Company(Independent Software Vendor/Publisher)** who ideally have or going to have a [SaaS](https://azure.microsoft.com/en-us/overview/what-is-saas/) and want to sell it to their customers. 
One of the cloud selling markets to sell a [SaaS](https://azure.microsoft.com/en-us/overview/what-is-saas/) is [Azure Marketplace](https://azuremarketplace.microsoft.com/en-us/marketplace/) and you can use Azure Marketplace store front to sell your SaaS application to your customers. Find more information on [Azure Marketplace here](https://docs.microsoft.com/en-us/azure/marketplace/). When you are selling your SaaS on Azure Marketplace, Microsoft helps deal with the transactions. [Benefits of selling through Commercial Marketplace](https://docs.microsoft.com/en-us/azure/marketplace/marketplace-publishers-guide#commercial-marketplace-benefits). 

To sell anything on Azure Marketplace you would need to create an offer in [Partner Center](http://partner.microsoft.com/)/[Partner Portal](http://cloudpartner.azure.com/) and publish to Azure marketplace. If you are not already on Azure Marketplace, [please find more information here](https://docs.microsoft.com/en-us/azure/marketplace/partner-center-portal/create-account) .

There are [many types of offers](https://docs.microsoft.com/en-us/azure/marketplace/publisher-guide-by-offer-type) you can create, publish and sell on Azure Marketplace and SaaS offering happens to be one of them. When you create different types of offers there are different requirements which needs to be fulfilled to successfully publish it to public.

As this sample is a requirement for creating a SaaS offer, we will only talk about SaaS offering but if you like you can view the information-about/requirements for different offerings [here](https://docs.microsoft.com/en-us/azure/marketplace/publisher-guide-by-offer-type). Please read more about [SaaS offer on Azure Marketplace here](https://docs.microsoft.com/en-us/azure/marketplace/marketplace-saas-applications-technical-publishing-guide).

You would need to follow [SaaS offer checklist here](https://docs.microsoft.com/en-us/azure/marketplace/partner-center-portal/offer-creation-checklist) to create one. 

On a high level below are things we need to be addressed to publish and sell a SaaS offer.
1. Complete Tax profile and Payout
2. Marketing and Plan/Pricing model
3. Technical requirements (An application to interact between the subscriber/customer, company/publisher and Azure Marketplace - This is exactly what this sample is for)

#### Steps Explanation

1. **Complete Tax profile and Payout** -  This is a one-time activity, just in case if not already done so. Basically, how SaaS offer works is
    - Publish your offer in Azure Marketplace
    - Customer buys the offer 
    - Microsoft bills the customer as per their selected billing term
    - Microsoft pays out to the Company/ISV
  For microsoft to pay the publisher, it needs 


2. **Marketing and Plan/Pricing model** 
    - You will need to provide information to go on your offer page. This includes descirption, support links, logos, screenshots and videos. There are few options on how you would want to sell your offer by creating different plans eg. 
        - flat rate + monthly/yearly + (optional meter_billing or 30 day free trial)
        - per user + monthly/yearly + (optional 30 day free trial)

3. :small_red_triangle_down:**Technical requirements**

    - :red_circle:**Azure Ad application registration** - This is a single tenant app and the details(TenantId and AppId) are used in the Technical configuration section when creating a SaaS Offer. You will need this to get the [marketplace authorization token](https://docs.microsoft.com/en-us/azure/marketplace/partner-center-portal/pc-saas-registration#get-a-token-based-on-the-azure-ad-app) and use in it the authorization header for calling the [Marketplace fulfilment api](https://docs.microsoft.com/en-us/azure/marketplace/partner-center-portal/pc-saas-fulfillment-api-v2), be it from Landing page or Dashboard admin page. This token is like the password to call the [Marketplace fulfilment api](https://docs.microsoft.com/en-us/azure/marketplace/partner-center-portal/pc-saas-fulfillment-api-v2)

    - :red_circle:**Landing page** - A [multi-tenant authenticated webpage](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-convert-app-to-be-multi-tenant) for customer to send email of managing their subscription to the Publisher Company Ops team.
        1. Customer would be redirected to landing page along with query string (e.g ?token=121212121), this token is kind of what represents that customers subscirption
        2. Customer login's to the landing page(using multi-tenant authentication flow), customer is authenticated
        3. After login:
        4. Get JWT token as per the first technical requirement above.
        5. Page calls the [Marketplace API Resolve endpoint](https://docs.microsoft.com/en-us/azure/marketplace/partner-center-portal/pc-saas-fulfillment-api-v2#resolve-a-subscription) (using marketplace auth jwt token(from #4) and query string token(#1)) which will respond with a subscription Id.
        6. Then, Page calls the Get on [Subscription endpoint](https://docs.microsoft.com/en-us/azure/marketplace/partner-center-portal/pc-saas-fulfillment-api-v2#gethttpsmarketplaceapimicrosoftcomapisaassubscriptionsapi-versionapiversion) passing the subscription Id to get more details/status of that subscription
        7. Submit button on the landing page will send an email to the Publisher Company Ops team to activate, update or cancel the subscription.
    
    - :red_circle:**Webhook** -  Webhook is an url endpoint provided by the publisher, where Azure Marketplace can call the publisher to inform the activies/actions performed by the customer outside of landing page. This [activites/actions are listed here](https://docs.microsoft.com/en-us/azure/marketplace/partner-center-portal/pc-saas-fulfillment-api-v2#implementing-a-webhook-on-the-saas-service). An example flow for delete would look like below
        1. Customer deletes SaaS offer
        2. Publisher Webhook gets a notification
        3. Validate the AUTH token on that request
        4. Ideally store the notification and have some mechanisum to bubble up like a email notification
        4. Perform the required action on your solution you have provided to the customer(In this case would be blocking the customer access to your SaaS solution)
        5. Send a PATCH request back to [Marketplace Operation API](https://docs.microsoft.com/en-us/azure/marketplace/partner-center-portal/pc-saas-fulfillment-api-v2#operations-api) with Success/Failure status 
           
    - :red_circle:**Dashboard Admin page** - Dashboard admin page is for your Ops team to manage all the your customers subscriptions. Publisher can list, get, update/patch, delete, check the status of an operation, view opertations from webhook, patch operations and [send usage of metered dimension](https://docs.microsoft.com/en-us/azure/marketplace/partner-center-portal/saas-metered-billing) for a subscirption. Intent of the customer activates can come through below ways
        1. LANDING PAGE Email from customer to ACTIVATE a subscirption
        2. LANDING PAGE Email from customer to CHANGE PLAN on a subscirption
        3. LANDING PAGE Email from customer to UNSUBSCRIBE
        4. WEBHOOK notifications
        5. Customer using Metered dimensions
        
       Publisher would 
       - Perform the actions on their SaaS solution accordingly 
       - Make changes to the customers subscription on the dashboard admin page.
        
    
## About the sample
