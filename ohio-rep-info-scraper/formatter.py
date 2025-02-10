import csv
import re

data = {
    "rodney-creech": {
        "getInfo": (
            "West Alexandria",
            "77 South High Street12th Floor Columbus, OH 43215",
            "(614) 466-2960",
            "(614) 719-6940",
        ),
        "getCommittees": "Agriculture,Commerce and Labor,Local Government,Public Safety",
        "getBio": (
            "Morehead State University, Bachelor’s Degree, Agronomy, Turf Science",
            "Twin Township Trustee, 2008-2014, Preble County Commissioner, 2015-2020, Ohio House of Representatives, Chairman of the House Agriculture Committee, 2021-Present",
            "Started a small lawn care business",
            "\n",
        ),
    },
    "jack-k-daniels": {
        "getInfo": (
            "New Franklin",
            "77 South High Street11th Floor Columbus, OH 43215",
            "(614) 466-1790",
            "(614) 719-6943",
        ),
        "getCommittees": "Insurance,Small Business,Transportation,Ways and Means",
        "getBio": (
            "University of Akron",
            "",
            "House of Representatives, Vice Chair of the House Transportation Committee, 2024-Present, New Franklin City Council, Council President, 2024",
            "",
        ),
    },
    "levi-dean": {
        "getInfo": (
            "Not Listed",
            "77 South High Street11th Floor Columbus, OH 43215",
            "(614) 466-1470",
            "(614) 719-6984",
        ),
        "getCommittees": "Agriculture,Commerce and Labor,Development,Small Business",
        "getBio": None,
    },
    "kellie-deeter": {
        "getInfo": (
            "Not Listed",
            "77 South High Street13th Floor Columbus, OH 43215",
            "(614) 466-9628",
            "(614) 719-3958",
        ),
        "getCommittees": "Arts, Athletics, and Tourism,Children and Human Services,Health,Insurance",
        "getBio": (
            "Marysville University of St. Louis, Doctorate, Nursing Practice, University of Akron, Master's, , BGSU in consortium with the Medical College of Ohio, BS, Nursing",
            "Ohio State Association of Nurse Anesthetists, President, , Ohio State Association of Nurse Anesthetists, Treasurer, , Ohio State Association of Nurse Anesthetists, Director of State Government Relations, , American Association of Nurse Anesthesiology, Finance Committee Member, , Ohio House of Representatives, Representative, 2023-",
            "Firelands Anesthesia, Owner, Actively practices",
            "St. Paul Catholic Church, Member\n",
        ),
    },
    "steve-demetriou": {
        "getInfo": (
            "Bainbridge Twp.",
            "77 S. High St12th Floor Columbus, OH 43215",
            "(614) 644-5088",
            "(614) 719-6998",
        ),
        "getCommittees": "Development,Small Business,Technology and Innovation,Ways and Means",
        "getBio": (
            "United States Military Academy at West Point, BS, Economics",
            "Ohio House of Representatives, Majority Whip, 2023-Present, Ohio House of Representatives, Representative, 2021-2023",
            "U.S. Army, Infantry Officer, Formerly, Small Business Owner, Owner, Formerly, Investment Business, Owner, Currently",
            "Sts. Constantine and Helen Greek Orthodox Church, Parish Council\n",
        ),
    },
    "sedrick-denson": {
        "getInfo": (
            "Cincinnati",
            "77 South High Street10th Floor Columbus, OH 43215",
            "(614) 466-1308",
            "(614) 719-3587",
        ),
        "getCommittees": "Financial Institutions,Natural Resources,Technology and Innovation",
        "getBio": (
            "School for Creative and Performing Arts,,Drama, dance, music theatre and percussion,University of Cincinnati,Organizational Leadership",
            "Cincinnati-Hamilton County Community Action Agency,Educator, ,Cincinnati City Council,Chief of Staff, ,For Ohio’s Future Action Fund,Southwest Ohio Outreach Director, ",
            "Cincinnati-Hamilton County Community Action Agency,Educator,Formerly,Ohio Environmental Council,Southwest Ohio Director,Currently",
            "Greater Cincinnati National Action Network,Political Action Chair,African American Chamber of Commerce,Government Affairs Chair\n",
        ),
    },
    "michael-d-dovilla": {
        "getInfo": (
            "Not Listed",
            "77 South High Street13th Floor Columbus, OH 43215",
            "(614) 466-4895",
            "(614) 719-6957",
        ),
        "getCommittees": "Energy,Finance,Veterans and Military Development,Workforce and Higher Education",
        "getBio": (
            "Baldwin Wallace University, BA, Economics and Political Science, The American University, MPA, International Management, U.S. Naval War College, MA, National Security and Strategic Studies, University of Illinois, EdD, Education Policy, Organization and Leadership",
            "Ohio House of Representatives, Representative, 2011-2016, 2023-Present, Ohio House of Representatives, Majority Whip, House Republican Policy Committee, Chairman, House Finance Committee, Vice Chairman",
            "U.S. Office of Personnel Management, Senior-level presidential appointee, Formerly, U.S. Senator George V. Voinovich, Principal advisor, Formerly, U.S. Department of State, Presidential Management Fellow, Formerly, The Dovilla Group, Founder and Leader, Formerly, The Grindstone Institute, Founder and Leader, Formerly, USS Cleveland Legacy Foundation, President and CEO, Formerly",
            "Scripture reader at church, Mentor to college students\n",
        ),
    },
    "ron-ferguson": {
        "getInfo": (
            "Wintersville",
            "77 South High Street13th Floor Columbus, OH 43215",
            "(614) 466-3735",
            "(614) 719-6995",
        ),
        "getCommittees": "Financial Institutions,Government Oversight,Medicaid,Technology and Innovation",
        "getBio": (
            "The Ohio State University, BA, Communications",
            "Ohio House of Representatives, Representative, 2021-Present, House Government Oversight Committee, Vice Chair, 2021-Present, Financial Institutions Committee, Member, 2021-Present, Medicaid Committee, Member, 2021-Present, Technology and Innovation Committee, Member, 2021-Present",
            "WTOV-TV, Television Journalist, Formerly, 7 Ranges Entertainment, Co-owner, Currently",
            "",
        ),
    },
    "tex-fischer": {
        "getInfo": (
            "Not Listed",
            "77 South High Street13th Floor Columbus, OH 43215",
            "(614) 466-6107",
            "(614) 719-3959",
        ),
        "getCommittees": "Development,Energy,General Government,Natural Resources",
        "getBio": (
            "",
            "",
            "American Conservation Coalition, National Field Director, 2018-2021, Mahoning County Republican Party, 1st Vice Chairman, 2022, Ohio House of Representatives, Representative, 2023-Present",
            "Digital Media Business, Owner, Currently",
        ),
    },
    "sarah-fowler-arthur": {
        "getInfo": (
            "Ashtabula",
            "77 South High Street12th Floor Columbus, OH 43215",
            "(614) 466-1405",
            "(614) 719-6999",
        ),
        "getCommittees": "Children and Human Services,Community Revitalization,Education,Local Government",
        "getBio": (
            "Ohio University, BS",
            "",
            "Ohio House of Representatives, Chair of the Education Committee, 2021-Present, State Board of Education, , 2013-2020",
            "",
        ),
    },
    "haraz-n-ghanbari": {
        "getInfo": (
            "Perrysburg",
            "77 South High Street13th Floor Columbus, OH 43215",
            "(614) 466-8104",
            "(614) 719-0006",
        ),
        "getCommittees": "Arts, Athletics, and Tourism,Public Safety,Small Business,Veterans and Military Development",
        "getBio": (
            "Kent State University, BS, Visual Journalism,United States Naval War College, , Command and Staff Program,University of Toledo, MS",
            "Ohio House of Representatives, Representative, 2019-Present,The University of Toledo, Director of Military and Veteran Affairs, Formerly,The Associated Press, Staff Photojournalist, Formerly",
            "Iraq and Afghanistan Veterans of America, American Legion, VFW, Military Officer Association of America, CedarCreek Church",
            "\n",
        ),
    },
    "chris-glassburn": {
        "getInfo": (
            "North Olmsted",
            "77 South High Street10th Floor Columbus, OH 43215",
            "(614) 466-3100",
            "(614) 719-6944",
        ),
        "getCommittees": "Development,Energy,Finance,Public Insurance and Pensions",
        "getBio": None,
    },
    "michele-grim": {
        "getInfo": (
            "Toledo",
            "77 S. High St14th Floor Columbus, OH 43215",
            "(614) 644-6017",
            "(614) 719-6947",
        ),
        "getCommittees": "Arts, Athletics, and Tourism,Finance,Health,Rules and Reference,Transportation",
        "getBio": (
            "Northeastern University, Doctorate, Law and Policy,University of Toledo, Master’s, Public Health",
            "Toledo City Council, At-large member",
            ",",
            "\n",
        ),
    },
    "jennifer-gross": {
        "getInfo": (
            "West Chester",
            "77 South High Street13th Floor Columbus, OH 43215",
            "(614) 466-8550",
            "(614) 719-6955",
        ),
        "getCommittees": "Community Revitalization,Government Oversight,Health,Medicaid",
        "getBio": (
            "Ohio University, BS, Nursing",
            "House of Representatives, , 2021-Present, Air Force, Lt. Colonel, 1987-2008",
            "Eli Lilly, Territory Manager, Formerly, , Family Nurse Practitioner, Currently, Sub-investigator for Operation WARP Speed, Currently",
            "American Legion Post 681, Member, VFW Post 7696, Member\n",
        ),
    },
    "derrick-hall": {
        "getInfo": (
            "Akron",
            "77 South High Street11th Floor Columbus, OH 43215",
            "(614) 466-1177",
            "(614) 719-6942",
        ),
        "getCommittees": "Energy,Medicaid,Veterans and Military Development,Ways and Means",
        "getBio": None,
    },
    "thomas-hall": {
        "getInfo": (
            "Madison Township",
            "77 South High Street12th Floor Columbus, OH 43215",
            "(614) 644-5094",
            "(614) 719-6953",
        ),
        "getCommittees": "Energy,Finance,Government Oversight,Public Safety",
        "getBio": (
            "Miami University, Bachelor’s Degree, Small Business Management",
            "Madison Township Trustee, 2015-2017, Ohio House of Representatives, Chairman of the House Government Oversight Committee, 2021-Present, Ohio House of Representatives, Member of the House Energy, Finance, and Public Safety committees, 2021-Present",
            "Middletown Area YMCA, Board Member,  United Way, Role, Action Council, Role, Butler County Township Association, Role, Volunteer Fireman, Part-time",
            "\n",
        ),
    },
}


def main():
    printIntoFile()


def printIntoFile():
    with open("results.txt", "w", newline="") as file:
        writer = csv.writer(file, delimiter="\t")

        for name, info in data.items():
            hometown, address, phone, fax = info["getInfo"]
            committees = info["getCommittees"]

            bio = info["getBio"]
            education = checkAIOutput(bio[0]) if bio and bio[0] else ""
            politics = checkAIOutput(bio[1]) if bio and len(bio) > 1 else ""
            employment = checkAIOutput(bio[2]) if bio and len(bio) > 2 else ""
            community = checkAIOutput(bio[3]) if bio and len(bio) > 3 else ""

            writer.writerow(
                [
                    name,
                    hometown,
                    address,
                    phone,
                    fax,
                    committees,
                    education,
                    politics,
                    employment,
                    community,
                ]
            )


def checkAIOutput(val):
    val = val.replace("\n", "")
    val = val.replace("   ", "")
    val = val.replace(", ,", ",")
    val = val.replace("�", "")
    val = val = re.sub(r"\s+", " ", val)

    return val


if __name__ == "__main__":
    main()
