from bs4 import BeautifulSoup
import requests

def get_single_page(letter = 'A', gender = 'N', offset = 0):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    params = {
        "advanced": 1,
        "starts" : letter,
        "gender": gender,
        "offset": int(offset)
    }
    response = requests.post('https://babynames.com/names/search.php', data = params, headers = headers)
    page_dom = BeautifulSoup(response.text, 'html.parser')
    names = page_dom.select("ul.searchresults > li")
    for i in range(len(names)):
        names[i] = names[i].get_text()
    return names

def get_number_of_names(number, letter = 'A', gender = 'N'):
    names = get_single_page(letter, gender)
    while len(names) < number:
        print("%.2f%% done." % (len(names) / number * 100))
        names = names + get_single_page(letter, gender, len(names))
    return names

try:
    number = int(input("How many names you want to list? "))
except:
    print("This must be a number.")
    exit()
letter = input("What should the name begin with? ")
gender = input("What gender should the names be (M, F, N)? ")
if gender not in ["M", "F", "N"]:
    print("Not a vaild choice.")
    exit()
names = get_number_of_names(number, letter, gender)
print(names)
txt_file = open("names.txt", "w", encoding= "UTF-8")
txt_file.write(' '.join([str(elem) for elem in names]))
txt_file.close()
print("Names saved as \"names.txt\"")