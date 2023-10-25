# Secure File Storage Application

## Overview

This Flask-based application provides users with the ability to securely upload and store files. One of the key features of this application is the encryption of file content and the obfuscation of file names. The application utilizes the JSON Web Encryption (JWE) standard for secure transmission of data.

## Technical Details

### File Upload and Encryption Flow

1. **User File Upload**: When a user uploads a file, the server initiates the following process:

   - The server generates a random encryption key.
   - It also generates a random file name for obfuscation purposes.

2. **File Encryption**: The server encrypts the uploaded file using the generated encryption key and saves it with the newly generated file name.

3. **Secure Transmission**: The server then packages the following data into a JWE:

   - Original file name
   - Randomly generated file name
   - Encryption key

4. **User Response**: The JWE, containing the above data, is sent back to the user for safekeeping.

### File Decryption Flow

1. **User Request**: When a user wants to retrieve a file, they send the previously received JWE to the server.

2. **JWE Decryption**: The server first decrypts the JWE to extract the following information:

   - Original file name
   - Encryption key

3. **File Retrieval**: With the decryption key and the original file name, the server locates the encrypted file associated with the user's request.

4. **File Decryption**: The server decrypts the requested file using the encryption key and sends the unencrypted file content to the user.

## Schema

Below is a simplified flowchart illustrating the process of file upload and retrieval in this application:

```sequence
User->Server: Upload File Request
Note right of Server: Server prepares to\nhandle the upload
User->Server: Upload File
Server->Server: Generate Encryption Key
Server->Server: Generate Random File Name
Server->Server: Encrypt File with Key
Server->Server: Save File with Random Name
Server->Server: Package Data (Original Name, Random Name, Key) into JWE
Server-->User: Send JWE Response

User->Server: Download File Request (JWE)
Server->Server: Decrypt JWE to extract data
Server->Server: Retrieve File with Key and Original Name
Server-->User: Send Decrypted File
```

This application ensures the secure storage and retrieval of files, maintaining user privacy by encrypting file content and using random file names, while also providing secure data transmission through JWE.

## Getting Started

To get started with this application, you can use Docker Compose (`docker compose up -d`) to launch the application in a containerized environment. Before running the application, make sure to provide the necessary environment variables in the `.env` file. Here are the required environment variables:

- `WEBSITE_NAME`: The name of your website.
- `ENCRYPTED_FILE_STORAGE`: The directory where encrypted files will be stored.
- `PRIVATE_FOLDER`: The private folder for the application.
- `SECRET_KEY`: Your secret key for the application. Make sure to change this to a strong and secure key.

You can create a `.env` file and set the values for these variables:

```env
WEBSITE_NAME="Anon Hosting"
ENCRYPTED_FILE_STORAGE="uploads"
PRIVATE_FOLDER="private"
SECRET_KEY="my_secret_key_CHANGE_ME !"
```
