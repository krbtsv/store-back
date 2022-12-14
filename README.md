# The Dress Store
Website for clothing store.
## Screenshots
___
![Thumbnail](Documents/products-photo.jpg)
### Stacks
+ Python
+ Django, DRF
+ [PostgreSQL](#PostgreSQL)
+ [Celery](#Celery)
+ Redis
### Functions
+ Register/Login users
+ Confirm email address
+ Authorization with GitHub
+ Users have a profile
+ Add goods to basket
+ Payment for goods through stripe payment system.
+ Purchase history
___
### PostgreSQL
Database shema:  
![Thumbnail](Documents/store_dress-public.png) 
___
### Celery
On project used `celery` with message broker `redis` for optimization email sending after registration users.  
  
Before using **Celery**:  
  
![Thumbnail](Documents/email-verification.jpg)  
After registration, the user had to wait for a response after sending the letter with email verification. Only after that was redirected to the login page.  
___  
After using **Celery**:  
  
![Thumbnail](Documents/email-verification-celery.jpg)  
Now the user is immediately redirected to the login page. And the task of sending a verification letter is taken over by `celery`  
___  
