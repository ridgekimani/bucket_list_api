# BUCKET LIST API

##AUTH API's
### 1. Register User 

* URL:
    * /api/v1/auth/register
    
* METHOD:
    * POST
    
* DATA FORMAT
    * application/json
    
* REQUIRED:
    * email
    * password
 
* SUCCESS:
   * status code 201
   * content {"email": "example@email.com", "token": "token_example"}
   

* ERROR:
   * status code 400
   * content 
        * {"error": "Bad request. Please enter some data"}
        * {"error": "Please enter your email address!"}
        * {"error": "Invalid email address"}
        * {"error": "Please enter your password"}
        * {"error": "Your password must be 6 characters long"}
        
        OR
        
   * status code 409
   * content {"error": "A user exists with that email"} 
        
### 2. Login User 

* URL:
    * /api/v1/auth/login
    
* METHOD:
    * POST
    
* DATA FORMAT
    * application/json
    
* REQUIRED:
    * email
    * password
 
* SUCCESS:
   * status code 200
   * content {"email": "example@email.com", "token": "token_example"}
   

* ERROR:
   * status code 400
   * content 
        * {"error": "Bad request. Please enter some data"}
        * {"error": "Please enter your email address!"}
        * {"error": "Invalid email address"}
        * {"error": "Please enter your password"}
        * {"error": "Email not found"}
            
    OR
        
   * status code 403
   * content {"error": "Incorrect password"}
 
### 3. Logout User 

* URL:
    * /api/v1/auth/logout
    
* METHOD:
    * POST

* SUCCESS:
    * status code 200
    * content {"success": "Logout successful"}

### 4. Reset Password 

* URL:
    * /api/v1/auth/reset_password
    
* METHOD:
    * POST
    
* DATA FORMAT
    * application/json
    
* REQUIRED:
    * email
 
* SUCCESS:
   * status code 200
   * content {"success" : "An email has been sent with instructions for your new password"}
   
* ERROR:
   * status code 400
   * content 
        * {"error": "Bad request. Please enter some data"}
        * {"error": "Please enter your email address!"}
        * {"error": "Email not found"}
        
        OR
        
   * status code 500
   * content {"error": "Password was not reset. Please try resetting again"} 
        
### 5. Change Password 

* URL:
    * /api/v1/auth/change_password
    
* METHOD:
    * PUT
    
* DATA FORMAT
    * application/json
    
* REQUIRED:
    * email
    * old_password
    * new_password
    * confirm_password
 
* SUCCESS:
   * status code 200
   * content {"success": "Password changed successfully"}
   
* ERROR:
   * status code 400
   * content 
        * {"error": "Bad request. Please enter some data"}
        * {"error": "Please enter your password"}
        * {"error": "Please enter your new password"}
        * {"error": "Please confirm your new password
        * {"error": "Email does not exist"}
        * {"error": "Passwords do not match"}
        * {"error": "Your password must be 6 characters long"}
            
    OR
   * status code 403
   * content 
        * {"error": "Incorrect password"}
        * content {"error": "Authentication required"}


### 6. Delete User 

* URL:
    * /api/v1/auth/delete_account
    
* METHOD:
    * DELETE
    
* DATA FORMAT
    * application/json
    
* REQUIRED:
    * email
    * password
   
* SUCCESS:
   * status code 200
   * content {"success": "Account deleted successfully"}
   
* ERROR:
   * status code 400
   * content 
        * {"error": "User does not exist"}
        
        OR
   * status code 403
   * content {"error": "Authentication required"}
   * content {"error": "Incorrect password"}
 
##Bucketlist API's
###1. Create Bucket
###2. Read Bucket(s)
###3. Update Bucket
###4. Delete Bucket
###5. Create Item
###6. Read Item(s)
###7. Update Item
###8. Delete Item 
        
