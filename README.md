# PASSMAN
Making passman application with UI and more functionality
Current functions:  

 - Create Account, stores username and hashed and salted password in database for user authentication
 - User account login
 - All site passwords encrypted in database, can only be accessed with decryption key generated at login
 - Ability to read database from non-default location
   - Allows you to bring your passwords with you, accessible anywhere PassMan is installed 
 - Delete Account, removes Master account and all associated login credentials from database
 - Account screen displays site name and username for each site you add to your account
	 
	 - passwords are stored in database with encryption key that is only
   generated upon login
   
	 - ability to copy, update, or remove passwords from your account using right click context menus
       
	 - ability to add new site passwords to your account
	 - password generator to generate more complex passwords using preselected criteria (Password length, Include uppercase, lowercase, numbers or symbols)
	
	 - Ability to export all account data to external storage for mobility
 - Update Master Password functionality, reencrypts and updates all site passwords under account with new decryption key

       
