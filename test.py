# import re
# string = ["connor.clark@WorLEYparsons.com",  # Correct
#           "connorclark@worleyparsons.com",  # Missing . in name
#           "connor.clark@worleyparson.com",  # Missing S in parsons
#           "connor.clark@worleyparsons.com.au",  # Added .au
#           "connor.clark1@worleyparsons.com",  # Confirm number are OK
#           "connor.clark@worley.com",  # Confirm shorthand is ok (for future)
#           "connor.clark1@Worley.com"  # Confirm number and shorthand is ok (for future)
#           ]
# Answers = [1,0,0,0,1,1,1]
# pattern = "[a-zA-Z]+\.[a-zA-Z0-9]+@(worleyparsons|worley)+\.(com)"
#
# for email in string:
#     email=email.lower()
#     if(re.search(pattern,email)):
#         print("%s  is valid"% email)
#     else:
#         print("%s is invalid"% email)
#


string = "password"
x = "*" * len(string)
print(x)