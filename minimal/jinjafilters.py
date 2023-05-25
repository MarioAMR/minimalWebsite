from inflection import parameterize
from flask import g,Markup

def slugify(myvar):
    return parameterize(myvar)[:80].rstrip('-')

#This data would better go in a database...
errorDict = { 
    "Err1": "ERROR 1: watch out for error n.1!",
    "Err2": "ERROR 2: watch out for error n.2!",
    "Err9": "ERROR 9: watch out for error n.9!"
}

def displayError(errNum):
    key = "Err"+str(errNum)
    result = errorDict[key]
    return result


msgDict = { 
    "Msg1": "<p>This is a <b>nice</b> message, the first of the list</p>",
    "Msg2": "<p>This is an even <b>nicer</b> message.</p>",
    "Please login to access your portal": "<p>Please login to access your portal.</p>",
    "Logged in successfully!":"<p>Logged in successfully!</p>",
    "Incorrect password, try again.":"<p>Incorrect password, try again.</p>",
    "Email does not exist.":"<p>Email does not exist.</p>",
    "E-mail must be greater than 5 characters":"<p>E-mail must be greater than 5 characters</p>",
    "First name must be greater than 1 characters":"<p>First name must be greater than 1 characters</p>",
    "Password must be greater than 6 characters":"<p>Password must be greater than 6 characters</p>",
    "Passwords don\'t match":"<p>Passwords don\'t match</p>",
    "Account created!":"<p>Account created!</p>",
    "Email already exists.":"<p>Email already exists.</p>"
}

def displayMessage(msgKey):
    #THE DECORATOR IS NEEDED TO DISABLE CACHING OF JINJA CALLS!!!
    result = Markup(msgDict[msgKey])
    return result
