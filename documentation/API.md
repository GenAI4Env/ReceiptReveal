## Overview

Below are suggested API endpoints derived from the backend structure. Adjust or rename them as needed.

## Authentication

• POST /auth/register  
    - Registers a new user via AuthManager.register_user  
• POST /auth/login  
    - Authenticates a user via AuthManager.login  
• POST /auth/logout  
    - Logs out the current user via AuthManager.logout  

## GenAI

• POST /genai/text  
    - Returns a text-based response from text_resp  
• POST /genai/image  
    - Returns an image-based response from image_resp  

## Database

• GET /db/prompts  
    - Retrieves prompts for the current user  
• POST /db/prompts  
    - Stores a new prompt and optional context  
