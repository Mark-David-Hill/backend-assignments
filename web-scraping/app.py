import requests
from bs4 import BeautifulSoup

url = "https://realpython.github.io/fake-jobs/"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

card_list = soup.find_all(class_='card-content')
card_dictionary_list = []

for card in card_list:
    card_dictionary = {}

    title = card.find(class_='title').text.strip()
    card_dictionary['title'] = title

    company = card.find(class_='company').text.strip()
    card_dictionary['company'] = company

    location = card.find(class_='location').text.strip()
    [city, state] = location.split(", ")
    card_dictionary['city'] = city
    card_dictionary['state'] = state

    time = card.find('time').text.strip()
    card_dictionary['time'] = time

    url_to_apply = card.find_all(class_='card-footer-item')[1]['href']
    card_dictionary['url_to_apply'] = url_to_apply

    application_page = requests.get(url_to_apply)
    application_soup = BeautifulSoup(application_page.content, "html.parser")

    description = application_soup.find_all('p')[1].text.strip()
    card_dictionary['description'] = description

    card_dictionary_list.append(card_dictionary)

    print(card_dictionary, '\n')

# for card in card_dictionary_list:
#     print(card, "\n")


# print(page)
# print(dir(page))

# print(type(page.text))
# print(page.text[0])
# print(page.text[1])
# print(page.text[2])


# print(soup)
# print(type(soup))
# print(dir(soup))

# job_titles = soup.find_all('h2')

# # print(job_titles)
# # print(type(job_titles[0]))

# # for job_title in job_titles:
# #     print(job_title.text.strip())

# company_list = soup.find_all(class_='subtitle')
# company_name_list = []

# for company in company_list:
#     company_name_list.append(company.text.strip())

# # print(company_name_list)

# first_company_name = soup.find(class_='is-6')

# # print(first_company_name.attrs)

# # company_attr_list = []

# # for company in company_name_list:
# #     company_attr_list.append(company.attrs['class'][2])

# # print(first_company_name.attrs['class'][2])
