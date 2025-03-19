# Blog API
A FastAPI-based blog application that allows users to create, read, update, and delete blog posts and comments. It supports authentication via JWT tokens and provides functionalities for both authenticated and unauthenticated users to interact with posts and comments.

## Application Structure
+ Authentication: Users can register and log in using JWT-based authentication.
+ Blog Posts: Users can create, update, and delete their own posts.
+ Comments: Both authenticated and unauthenticated users can add comments to posts.
+ Replies: Comments support nested replies, allowing users to engage in discussions.
+ Authorization: Post owners can delete any comment on their post, and users can only edit/delete their own comments.
+ ID Management: Unique IDs are automatically generated for each comment and reply.
+ Nested Deletion: If a comment is deleted, all its nested replies are also deleted.

## Features
+ User authentication using JWT tokens
+ CRUD operations for blog posts
+ Commenting system supporting replies
+ Authorization for modifying/deleting comments and posts
+ Supports both authenticated and unauthenticated users

## Cloning the Repository
To get started, clone the repository to your local machine
``` git clone https://github.com/Ebiladou/Beanie-blog ```

## Installing Dependencies
Create a virtual environment and install dependencies
``` pip install -r requirements.txt ```

## Environment Variables
Before running the application, create a .env file in the root directory and fill in the following environment variables:
### Sign into cloudinary and get the cloud API credentials.
+ CLOUD_NAME 
+ CLOUD_API_KEY
+ CLOUD_API_SECRET

### Get the JTW credentials:
+ SECRET_KEY 
+ ALGORITHM 
+ ACCESS_TOKEN_EXPIRE_MINUTES

## Running the Application
CD into app and start the application with
``` uvicorn main:app ```

## API Documentation
+ Swagger UI: http://127.0.0.1:8000/docs
+ ReDoc UI: http://127.0.0.1:8000/redoc