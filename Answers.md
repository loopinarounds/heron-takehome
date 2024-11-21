# What are the limitations in the current classifier that's stopping it from scaling?

1) Only detects a few specific keywords in filenames "drivers_license", "bank_statement", "invoice". This is very limiting for it's functionality and makes it quite useless as a tool for most companies of whom will deal with many other types of files - e.g A :"Report", "Proof of Address" and so on. There is also limited file extensions able to be classified. 

2) If files are named incorrectly, they will be classified incorrectly. This is problematic as file content may differ from the name of the file, leaving alot of room for user error and no way for the classifier to know as much. 


3) There is a struggle with scaling coming from the fact we can only handle one file at a time. Would be much better if we can test multiple at once. Also a scaling issue that we manually setup the options list - e.g we must add what classification types are available. Any time a new file type is used we would have to manually add it to the codebase.

# How might you extend the classifier with additional technologies, capabilities, or features?

1) Allow batched requests - multiple files at a time in the request

2) Train a model in the program to read file data and give a classification based upon the content, we can easily train new file extensions and types from this.

3) Better error handling (can be provided by the model we will train in 2.)

# How can you ensure the classifier is robust and reliable in a production environment?

1) Good testing standards - prepare for eevry edge case and possibility that could be thrown at it to ensure users are not left confused by errors

2) Good early error handling - make sure to return errors regarding things like file types as soon as possible, also ensuring that errors are handled later on at key points incase an unsupported file slips through.

3) Designing modularly - important re-used functions should have their own easy to find files. These files can then be added to with relevant functions that see similar use. e.g with data_loader - we can add more file extension functions easily.

4) Version control - make sure to make use of a staging environment for testing new updates without impacting the current live product.

# How can you deploy the classifier to make it accessible to other services and users?

1) Implement a UI with a file upload - submitting on this UI will be muich easier than making a cURL request for an average person.

2) Return succesful data in a CSV format - this is much easier to read than reading through a json in the console.

3) Expose it as a Restful API - implement some sort of api key security to be used to verify users - they can then create classes in their own codebase that interacts with our api rather than downloading and hosting themselves.







