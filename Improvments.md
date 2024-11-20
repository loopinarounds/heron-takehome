# Problems

1) Only detects a few specific keywords in filenames "drivers_license", "bank_statement", "invoice". This is very limiting for it's functionality and makes it quite useless as a tool for most companies of whom will deal with many other types of files - e.g A :"Report", "Proof of Address" and so on. There is also limited file extensions able to be classified. 

2) If files are named incorrectly, they will be classified incorrectly. This is problematic as file content may differ from the name of the file, leaving alot of room for user error and no way for the classifier to know as much. 


3) There is a struggle with scaling coming from the fact we can only handle one file at a time. Would be much better if we can test multiple at once. Also a scaling issue that we manually setup the options list - e.g we must add what classification types are available. Any time a new file type is used we would have to manually add it to the codebase.

# Improvements

1) Allow batched requests - multiple files at a time in the request

2) Train the program to read file data and give a classification based upon the content

3) Better error handling (can be provided by the model we will train in 2.)


