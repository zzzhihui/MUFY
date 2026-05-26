str1 = 'The'
str2 = 'Thumbs up'
str3 = 'Theatre can be boring'
def check_string(input_str):
    if input_str in ['The', 'Theatre can be boring']:
       return 'Found it!'
    else:
       return "Nope." 
print(check_string(str1))
print(check_string(str2))
print(check_string(str3))