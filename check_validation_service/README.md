**Check validation service documentation**

This service uses graphQL to validate a check for the Loan Application.

It is called by the *customer_service*, which ask the customer to input information such as :
 - Their full name
 - Their bank's name
 - The issue date on their check
 - The check's ID
 - The amount of the check

Based on this information, the service will return a boolean to the *customer_service*
If the check is not valid, the check will bounce and this service calls the *notification_service* to send a mail to the email associated with the customer's account.