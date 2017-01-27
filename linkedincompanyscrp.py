#Auther Ahmed Ameen
from lxml import html
import csv, os, json
import requests
from exceptions import ValueError
from time import sleep


def linkedin_companies_parser(url):
    for i in range(5):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
            response = requests.get(url, headers=headers)
            formatted_response = response.content.replace('<!--', '').replace('-->', '')
            doc = html.fromstring(formatted_response)
            datafrom_xpath = doc.xpath('//code[@id="stream-promo-top-bar-embed-id-content"]//text()')
            if datafrom_xpath:
                try:
                    json_formatted_data = json.loads(datafrom_xpath[0])
                    company_name = json_formatted_data['companyName']
                    size = json_formatted_data['size']
                    industry = json_formatted_data['industry']
                    description = json_formatted_data['description']
                    follower_count = json_formatted_data['followerCount']
                    year_founded = json_formatted_data['yearFounded']
                    website = json_formatted_data['website']
                    type = json_formatted_data['companyType']
                    specialities = json_formatted_data['specialties']
                    city = json_formatted_data["headquarters"]['city']
                    country = json_formatted_data["headquarters"]['country']
                    state = json_formatted_data["headquarters"]['state']
                    street1 = json_formatted_data["headquarters"]['street1']
                    street2 = json_formatted_data["headquarters"]['street2']
                    street = street1 + ', ' + street2
                    zip = json_formatted_data["headquarters"]['zip']
                    data = {
                                'company_name': company_name,
                                'size': size,
                                'industry': industry,
                                'description': description,
                                'follower_count': follower_count,
                                'founded': year_founded,
                                'website': website,
                                'type': type,
                                'specialities': specialities,
                                'city': city,
                                'country': country,
                                'state': state,
                                'street': street,
                                'zip': zip,
                                'url': url
                            }
                    return data
                except:
                    print "cant parse page", url

            # Retry in case of captcha or login page redirection
            if len(response.content) < 2000 or "trk=login_reg_redirect" in url:
                if response.status_code == 404:
                    print "linkedin page not found"
                else:
                    raise ValueError('redirecting to login page or captcha found')
        except :
            print "retrying :",url
#add company page below to company url list
def readurls():
    companyurls = ['https://www.linkedin.com/company/cisco',
                    'https://www.linkedin.com/company/tata-consultancy-services',
                   'https://www.linkedin.com/company/infosys',
                   'https://www.linkedin.com/company/adobe',
                   'https://www.linkedin.com/company/tesla-motors',
                   'https://www.linkedin.com/company/spacex'
                   ]
    extracted_data = []
    for url in companyurls:
        extracted_data.append(linkedin_companies_parser(url))
        sleep(5)
    f = open('data.json', 'w')
    json.dump(extracted_data, f, indent=4)


if __name__ == "__main__":
    readurls()