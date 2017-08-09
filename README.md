# BUCKET LIST API
This is your day to day activity recording app as a restful web service used to perform CRUD 
operations of Bucket and Items.
[![Build Status](https://travis-ci.org/ridgekimani/bucket_list_api.svg?branch=master)](https://travis-ci.org/ridgekimani/bucket_list_api)
[![Coverage Status](https://coveralls.io/repos/github/ridgekimani/bucket_list_api/badge.svg?branch=master)](https://coveralls.io/github/ridgekimani/bucket_list_api?branch=master)
![python](https://img.shields.io/badge/python-3.6%203.5-green.svg)
![flask](https://img.shields.io/badge/flask-0.12.2-blue.svg)
 

## AUTH API endpoints
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
 
## Bucket API endpoints
### 1. Create Bucket
* URL:
    * /api/v1/bucketlists/
    
* METHOD:
    * POST
    
* DATA FORMAT
    * application/json
    
* REQUIRED:
    * bucket_name
    * description
 
* SUCCESS:
   * status code 201
   * content 
        
        
         {
             "bucket": {
                 "bucket_name": "bucket_name",
                 "created": "datetime object",
                 "description": "description",
                 "id": int(id),
                 "updated": "datetime object",
                 "user": "example user"
             }
         }
   

* ERROR:
   * status code 400
   * content 
        * {"error": "Bad request. Please enter some data"}
        * {"error": "Please enter the bucket name"}
        * {"error": "Please describe your bucket"}
   OR
   * status code 403
   * content
        * {"error": "Unauthorized. Please login"}

### 2. Read Bucket
* URL:
    * /api/v1/bucketlists/?[params]
    * /api/v1/bucketlists/{bucket_id}
    
* METHOD:
    * GET
    
* DATA FORMAT
    * application/json
    
* OPTIONAL:
    * bucket_id
    * limit
    * page
 
* SUCCESS:
   * status code 201
   * content 
   
   
         {
             "bucket": {
                 "bucket_name": "bucket_name",
                 "created": "datetime object",
                 "description": "description",
                 "id": int(id),
                 "updated": "datetime object",
                 "user": "example user"
             }
         }
        
   OR
   
   * content
   
   
         {
              buckets": [
                  {
                      "bucket_name": "bucket_name",
                      "created": "datetime object",
                      "description": "description",
                      "id": int(id),
                      "updated": "datetime object",
                      "user": "example user"
                  },
                  {
                      "bucket_name": "bucket_name",
                      "created": "datetime object",
                      "description": "description",
                      "id": int(id),
                      "updated": "datetime object",
                      "user": "example user"
                  }
              ]
         }

* ERROR:
   * status code 400
   * content
    {"error": "Please enter valid limit and page numbers"}
     
   OR
   * status code 403
   * content
        * {"error": "Unauthorized. Please login"}
        
### 3. Update Bucket
* URL:
    * /api/v1/bucketlists/{bucket_id}
    
* METHOD:
    * PUT
    
* DATA FORMAT
    * application/json
    
* REQUIRED:
    * bucket_name
    * description
 
* SUCCESS:
   * status code 200
   * content
   
    
         {
             "bucket": {
                 "bucket_name": "bucket_name",
                 "created": "datetime object",
                 "description": "description",
                 "id": int(id),
                 "updated": "datetime object",
                 "user": "example user"
             }
         }
   

* ERROR:
   * status code 400
   * content
        * {"error": "Please specify your bucket id" 
        * {"error": "Bad request. Please enter some data"}
        * {"error": "Please enter the bucket name"}
        * {"error": "Please describe your bucket"}
        * {"error": "Bucket not found"}
   OR
   * status code 403
   * content
        * {"error": "Unauthorized. Please login"}

### 4. Delete Bucket
* URL:
    * /api/v1/bucketlists/{bucket_id}
    
* METHOD:
    * DELETE
    
* DATA FORMAT
    * application/json
    
* REQUIRED:
    * password
    
* SUCCESS:
    * status code 200
    * content = 
    
    
          {
              "buckets": 
              [
                  {bucket1},
                  {bucket2}
              ]
          }
              where bucket 1 and bucket 2 are json objects

* ERROR:
    * status code 400
    
    OR
    * status code 403
    * content
        * {"error": "Unauthorized. Please login"}
 
 
## Item API endpoints
### 1. Create Item
* URL:
    * /api/v1/bucketlists/{bucket_id}
    
* METHOD:
    * POST
    
* DATA FORMAT
    * application/json
    
* REQUIRED:
    * description
 
* SUCCESS:
   * status code 201
   * content 
   
   
         {
             "activity": {
                 "description": "activity description",
                 "created": "datetime object",
                 "id": int(id),
                 "bucket_id": int(id)
                 "updated": "datetime object",
                 "user": "example user"
             }
         }


* ERROR:
   * status code 400
   * content 
        * {"error": "Bad request. Please enter some data"}
        * {"error": "Bucket not found"}
        * {"error": "Please specify your bucket id"}
        * {"error": "Please describe your activity"}
   OR
   * status code 403
   * content
        * {"error": "Unauthorized. Please login"}

### 2. Read Item
* URL:
    * /api/v1/bucketlists/{bucket_id}/items/{item_id}
    
* METHOD:
    * GET
    
* DATA FORMAT
    * application/json
    
* OPTIONAL:
    * item_id
    * limit
    * page
 
* SUCCESS:
   * status code 201
   * content
   
    
         {
             "activity": {
                 "created": "datetime object",
                 "description": "description",
                 "id": int(id),
                 "bucket_id": "bucket id"
                 "updated": "datetime object",
                 "user": "example user"
             }
         }
        
   OR
   
   * content
    
    
         {
         activities": [
                 {
                     "created": "datetime object",
                     "description": "description",
                     "id": int(id),
                     "bucket_id": "bucket id"
                     "updated": "datetime object",
                     "user": "example user"
                 },
                 {
                     "created": "datetime object",
                     "description": "description",
                     "id": int(id),
                     "bucket_id": "bucket id"
                     "updated": "datetime object",
                     "user": "example user"
                 }
         ]
         }
   

* ERROR:
   * status code 400
   * content
    * {"error": "Please enter valid limit and page numbers"}
     
   OR
   * status code 403
   * content
        * {"error": "Unauthorized. Please login"}
        
### 3. Update Item
* URL:
    * /api/v1/bucketlists/{bucket_id}/items/{item_id}
    
* METHOD:
    * PUT
    
* DATA FORMAT
    * application/json
    
* REQUIRED:
    * bucket_id
    * item_id
    * description
 
* SUCCESS:
   * status code 200
   * content
   
    
          {
              "activity": {
                  "created": "datetime object",
                  "description": "description",
                  "id": int(id),
                  "bucket_id": int(id)
                  "updated": "datetime object",
                  "user": "example user"
              }
          }


* ERROR:
   * status code 400
   * content
        * {"error": "Please specify your bucket id" 
        * {"error": "Bad request. Please enter some data"}
        * {"error": "Please describe your activity"}
        * {"error": "Bucket not found"}
   OR
   * status code 403
   * content
        * {"error": "Unauthorized. Please login"}

### 4. Delete Item
* URL:
    * /api/v1/bucketlists/{bucket_id}/items/{item_id}
    
* METHOD:
    * DELETE
    
* DATA FORMAT
    * application/json
    
* REQUIRED:
    * password
    
* SUCCESS:
    * status code 200
    * content 
    
    
          {
          "activities": 
              [
                  {activity1},
                  {activity2}
              ]
          }
    
* ERROR:
    * status code 400
        * {"error": "Activity not found"}
    
    OR
    * status code 403
    * content
        * {"error": "Unauthorized. Please login"}
  
## SEARCH API endpoints
* URL:
    * /api/v1/search/?q={}
    
* METHOD:
    * GET
    
* DATA FORMAT
    * application/json
    
* REQUIRED:
    * q
    
* SUCCESS:
    * status code 200
    * content 
    
    
          {
          "activities": 
              [
                  {activity1},
                  {activity2}
              ]
          "buckets":
            [
                {bucket1},
                {bucket2}
          }
    