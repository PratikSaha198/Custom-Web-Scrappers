from bs4 import BeautifulSoup
import requests
import json
from concurrent.futures import ThreadPoolExecutor
import asyncio
import time

instagram_url = 'https://www.instagram.com'

profiles = []

print()

# Entry of profiles to be parsed
num = int(input("Enter the number of profiles :"))
print()

print("Enter the Profiles : ")
print()

for i in range(num):
	entry = str(input())
	profiles.append(entry)

# To get the exact followers from the json
def get_followers_count(profile_url : str , session):
	
	response = session.get(f"{instagram_url}/{profile_url}")
	# print(response.status_code)
	if response.ok:
		html = response.text
		bs_html = BeautifulSoup(html , "html5lib")

		scripts = bs_html.select('script[type="application/ld+json"]')
		scripts_content = json.loads(scripts[0].text.strip())

		main_entity_of_page = scripts_content['mainEntityofPage']
		interaction_statistic =main_entity_of_page['interactionStatistic']
		followers_count = interaction_statistic['userInteractionCount']

		return followers_count

# To make the parsing faster => multi-threading implemented
async def get_followers_async(profiles : list) -> list:
	res = []
	with ThreadPoolExecutor(max_workers=10) as executor:
		with requests.Session() as session :
			loop = asyncio.get_event_loop()
			tasks = [
				loop.run_in_executor(executor , get_followers_count , *(profile , session)) for profile in profiles
			]
			for response in await asyncio.gather(*tasks):
				res.append(response)
	return res

# The time elapsed recorded and Details printed
start = time.time()
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(get_followers_async(profiles))
res = loop.run_until_complete(future)
end = time.time()
elapsed = end - start

print()
print("ANALYSED DATA :")

for i in range(len(profiles)) : 
	print()
	print(f"{i+1}. {profiles[i]} has {res[i]} number of followers.")

print()
print(f"It took {elapsed} seconds to parse the data using Multiple Threading.")

