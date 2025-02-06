import requests  # type: ignore
import time
from bs4 import BeautifulSoup  # type: ignore
import google.generativeai as genai  # type: ignore

API_KEY = "AIzaSyBAi7XndVKZfpmkCa9d80KxNM_q3ZwrK24"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
ai_prompt_text = """

    The text at the end of this prompt is a biography for a memeber Ohio State House of Representatives. Using the biography return a summarization of the biography. The summarization format and notes on each section is described next.

    Summarization format and information:

    1. A comma delimited list of their education.
        a. The list should follow the format 'University, Degree, Area of Study'.
        b. If one of the three sections is not specified then leave it blank. In this case do not include the comma either. This means the list could be "University, Degree", "Degree, Area of Study", Etc.
        c. Here is an example of what a representatives list might look like "The Ohio State University, MS, Political Science, Ohio University, BS, Nursing"
    2. A comma delimited list of their past political experience. 
        a. The list should follow the format 'Organization, Role, Term'
        b. If one of the three sections is not specified then leave it blank. In this case do not include the comma either. This means the list could be "Organization, Term", "Role, Term", Etc.
        c. The political experience can include Previous Terms in the house or senate of anywhere and city councils.
        d. Here is an example of what a representatives list might look like "House of Representatives, Majority Whip, 2017-2021, Columbus City Council, Gahanna City Council, President"
    3. A comma delmited list of their employment history.
        a. The list should follow the format 'Organization, Role, Status'.
        b. If one of the three sections is not specified then leave it blank. In this case do not include the comma either. This means the list could be "Organization, Status", "Role, Status", Etc.
        c. Include any instances of buying, selling, or starting businesses
        d. Here is an example of what a representatives list might look like "JP Morgan Chase, Accountant, Formerly, Bought Johns Company, Started Columbus Mowing"
    4. A comma delimited list of their community involvement. This includes churches, local organizations, school boards, etc.
        a. The list should follow the format 'Organization, role'.
        b. It is possible that only an organization is listed. If so then include the organziation. E.g. "Church of God"
        c. Here is an example of what a representatives list might look like "Member of General Church, Neighborhood Watch, Captain"

    Listed next in any general instructions for generating the lists and the total output.

    1. The total output should be a list delimited by "|". Where each section (education, politcal history, employment history, community involvement) makes up an element in the list
    2. If a biography does not mention a section then do not include it. In this case still delimit the section. E.g. if a rep does not have employement history "Education list|Political history list||Community involvement list" would be the format of the output
    3. If no text for the bio is provided then return "||||"
    4. No new line operators or instances of the string ", ," should exist in the response 

    Biography:
    """

def main():
    """ rep_names = ["munira-abdullahi", "darnell-t-brewer", "karen-brownlee"] """
    rep_names = []
    url = "https://ohiohouse.gov/members/directory?start=1&sort=LastName"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    rep_name_divs = soup.find_all("div", class_="media-overlay-caption-text-line-1")

    for div in rep_name_divs[:10]:
        # Use re.sub in future
        rep_names.append(
            div.text.strip().replace(" ", "-").replace(".", "").replace(",", "").lower()
        )

    people = {}

    # Throttled loop to ensure it does not exceed rate limit for AI Calls
    for rep_name in rep_names:
        start_time = time.time()

        people[rep_name] = {}
        getInfo(people, rep_name)

        elapsed_time = time.time() - start_time 
        start_time = time.time()
        print(elapsed_time, "getInfo")

        fillBioFields(people, rep_name, getBio(rep_name))

        elapsed_time = time.time() - start_time 
        start_time = time.time()
        print(elapsed_time, "Bio fields")

        getCommittees(people, rep_name)

        elapsed_time = time.time() - start_time 
        print(elapsed_time, "Comittees")
        """ time_to_wait = 4 - elapsed_time 

        if time_to_wait > 0:
            time.sleep(time_to_wait)  """
        
        print("_-----------------------------------------------+_")

    print(people)


def checkResponse(response):
    if response.status_code:
        if response.status_code != 200:
            print("Bad response code: ", response.status_code)
            return 1
        else:
            return 0
    else:
        return 0


def getInfo(people, rep_name):
    address_keywords = ["77", "High", "Street", "St.", "South", "S.", "Floor"]

    url = f"https://ohiohouse.gov/members/{rep_name}"
    response = requests.get(url)

    if checkResponse(response) != 0:
        print(rep_name, "Bad Request")
        print("-------------------------")
        return

    soup = BeautifulSoup(response.content, "html.parser")

    divs = soup.find_all("div", class_="member-info-bar-module")

    for module in divs:
        module_text = module.get_text()
        if "Hometown" in module_text:
            people[rep_name]["home_town"] = module.find(
                "div", class_="member-info-bar-value"
            ).text.strip()

        if any(keyword in module_text for keyword in address_keywords):
            address_number_module = module.find_all(
                "div", class_="member-info-bar-value"
            )

            people[rep_name]["office_address"] = address_number_module[0].text.strip()
            people[rep_name]["phone_number"] = (
                address_number_module[1].text.strip().replace("Phone: ", "")
            )  # remove preceding "Phone: "
            people[rep_name]["fax_number"] = (
                address_number_module[2].text.strip().replace("Fax: ", "")
            )  # remove preceding "Fax: "


def getBio(rep_name):

    url = f"https://ohiohouse.gov/members/{rep_name}/biography"
    response = requests.get(url)

    if checkResponse(response) != 0:
        print(rep_name, "Bad Request")
        print("-------------------------")
        return

    soup = BeautifulSoup(response.content, "html.parser")

    bio_block = soup.find("div", class_="gray-block")

    if bio_block:
        bio_paragraphs = bio_block.find_all("p")

        if bio_paragraphs:
            combined_bio = " ".join(
                paragraph.text.strip() for paragraph in bio_paragraphs
            )

            return combined_bio


def getCommittees(people, rep_name):
    url = f"https://ohiohouse.gov/members/{rep_name}/committees"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    media_captions = soup.find_all("div", class_="media-overlay-caption")

    committees = ",".join(caption.text.strip() for caption in media_captions)

    people[rep_name]["committees"] = committees

def fillBioFields(people, rep_name, bio):

    response = model.generate_content(ai_prompt_text + " " + bio)

    values = response.text.split("|")
    
    people[rep_name]["education"] = values[0]
    people[rep_name]["political"] = values[1]
    people[rep_name]["employment"] = values[2]
    people[rep_name]["community"] = values[3] 



if __name__ == "__main__":
    main()
