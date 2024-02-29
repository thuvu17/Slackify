# Instructions for MongoDB

## Setting up MongoDB
First, follow these general steps to set up MongoDB on your local machine. Please note that the exact details might vary depending on your operating system.

### For Windows:
#### Download MongoDB:
Visit the MongoDB Download Center and download the MongoDB Community Server for Windows.
#### Install MongoDB:
Run the installer and follow the installation instructions. You can choose the "Complete" setup type.
#### Start MongoDB:
- After installation, open a Command Prompt as an administrator.
- Navigate to the MongoDB installation directory (C:\Program Files\MongoDB\Server\<version>\bin by default).
- Run the following command to start the MongoDB server:
```
mongod
```
This will start the MongoDB server.

### For macOS:
#### Install Homebrew (if not already installed):
Open Terminal and run the following command:
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```
#### Install MongoDB:
Run the following command to install MongoDB using Homebrew:
```
brew tap mongodb/brew
brew install mongodb-community
```

## Starting MongoDB
### Setting environment variables
- To connect to MongoDB on the locally, you need to set your environment variable **CLOUD_MONGO** to 0
```
export CLOUD_MONGO="0"
```
- To connect to MongoDB on the cloud, you need to set your environment variable **CLOUD_MONGO** to 1
```
export CLOUD_MONGO="0"
```
### Start MongoDB:
- Run the following command to start the MongoDB server:
```
brew services start mongodb-community
```
- On your terminal, open your API swagger to view and test all the endpoints:
```
./local.sh 
```