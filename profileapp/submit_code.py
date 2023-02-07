# from utils import *
import requests
from time import sleep
import json
# from telegram import #print

global main_log
main_log = ""
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "origin": "https://practice.geeksforgeeks.org",
    "referer": "https://practice.geeksforgeeks.org/",
}


LOGIN_HEADERS = HEADERS.copy()
LOGIN_HEADERS["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
LOGIN_HEADERS["Host"] = "auth.geeksforgeeks.org"
LOGIN_HEADERS["Origin"] = "https://auth.geeksforgeeks.org"
LOGIN_HEADERS["Referer"] = "https://auth.geeksforgeeks.org/"


STATS_URL = (
    "https://practiceapi.geeksforgeeks.org/api/v1/problems-of-day/problem/today/"
)
LOGIN_URL = "https://auth.geeksforgeeks.org/auth.php"
BASE_LOGIN_DETAILS = {
    "reqType": "Login",
    "user": "",
    "pass": "",
    "rem": "false",
    "rem": "on",
    "to": "https://auth.geeksforgeeks.org/?to=https://auth.geeksforgeeks.org/user/trexcod5gdw/",
    "g-recaptcha-response": "",
    "browserInfo": '{"appName":"Netscape","appCodeName":"Mozilla","cookieEnable":true,"prodName":"Gecko","appVersion":"5.0 (Windows)","appOs":"Win32","appLang":"en-US","vendorName":"","loginDomain":"auth"}',
}


def get_cookies(filename="cookies.json"):
    cookies = {}
    with open("./profileapp/cookies/" + filename) as f:
        data = json.load(f)
        if type(data) == dict:
            cookies = data
        elif type(data) == list:
            for i in data:
                cookies[i["name"]] = i["value"]
    return cookies


def get_stats():
    cookies = get_cookies()
    r = requests.get(STATS_URL, cookies=cookies, headers=HEADERS)
    data = r.json()
    return data


def get_slug_from_problem_url(url):
    li = url.split("/")
    return li[li.index("problems") + 1]


def get_slug(stats=None):
    if not stats:
        data = get_stats()
    else:
        data = stats
    return get_slug_from_problem_url(data["problem_url"])


def get_problem_id(stats=None):
    if not stats:
        data = get_stats()
    else:
        data = stats
    return data["problem_id"]


def get_pod_stats(filename):
    cookies = get_cookies(filename)
    POD_STATS_URL = (
        "https://practiceapi.geeksforgeeks.org/api/v1/problems-of-day/my-pod-profile/"
    )
    res = requests.get(POD_STATS_URL, cookies=cookies, headers=HEADERS)
    data = res.json()
    return data


def get_cookies_from_login_details(email, password, filename=None):
    #print("Fetching cookies for " + email)
    session = requests.Session()
    temp = session.get("https://auth.geeksforgeeks.org/")
    temp2 = session.post(
        "https://auth.geeksforgeeks.org/setLoginToken.php", headers=LOGIN_HEADERS
    )

    # convert logion_details to form data
    form_data = {
        "reqType": (None, "Login"),
        "user": (None, email),
        "pass": (None, password),
        "rem": (None, "false"),
        "rem": (None, "on"),
        "to": (
            None,
            "https://auth.geeksforgeeks.org/?to=https://auth.geeksforgeeks.org/user/trexcod5gdw/",
        ),
        "g-recaptcha-response": (None, ""),
        "browserInfo": (
            None,
            '{"appName":"Netscape","appCodeName":"Mozilla","cookieEnable":true,"prodName":"Gecko","appVersion":"5.0 (Windows)","appOs":"Win32","appLang":"en-US","vendorName":"","loginDomain":"auth"}',
        ),
    }

    r = session.post(LOGIN_URL, files=form_data, headers=HEADERS)

    cookies = {}
    for cookie in session.cookies:
        cookies[cookie.name] = cookie.value
    if filename:
        with open("./profileapp/cookies/" + filename, "w") as f:
            json.dump(cookies, f)
    #print("Cookies fetched for " + email)
    return cookies




LANG_MAPPING = {
    "C++": "cpp",
    "Java": "java",
    "Python3": "python3",
}
LOGIN_DETAILS = [
    {"email": "trex.coder.999@gmail.com", "password": "naga6242"},
    {"email": "senorita4488@gmail.com", "password": "santhu@44"},
    {"email": "2019287@iiitdmj.ac.in", "password": "santhu@44"},
]


def prepare_submission_data():
    cookies = get_cookies()
    stats = get_stats()
    slug = get_slug(stats=stats)
    metainfo_url = (
        f"https://practiceapi.geeksforgeeks.org/api/latest/problems/{slug}/metainfo/"
    )
    res = requests.get(metainfo_url, cookies=cookies, headers=HEADERS)
    metainfo = res.json()
    if not metainfo["results"]["is_user_login"]:
        #print("Cookies Expired for Solution Fetching")
        get_cookies_from_login_details(
            LOGIN_DETAILS[0]["email"], LOGIN_DETAILS[0]["password"], "cookies.json"
        )
        return prepare_submission_data()

    editorial_details = get_editorial()
    if editorial_details is None:
        #print("No Editorial Found")
        return None

    #print("Preparing code for submission")
    user_lang = editorial_details["lang"]
    user_code = editorial_details["full_func"]
    initial_code = metainfo["results"]["extra"]["initial_user_func"][
        LANG_MAPPING[user_lang]
    ]["initial_code"]
    if user_lang == "Python3":
        full_code = user_code + initial_code
    else:
        full_code = initial_code + user_code
    submit_data = {
        "source": (None, "https://practice.geeksforgeeks.org"),
        "request_type": (None, "solutionCheck"),
        "language": (None, LANG_MAPPING[user_lang]),
        "userCode": (None, user_code),
        "code": (None, full_code),
    }
    return submit_data


def get_editorial():
    cookies = get_cookies()
    data = get_stats()
    slug = get_slug_from_problem_url(data["problem_url"])
    #print(f"Fetching solution for problem: {slug}")
    editorial_url = f"https://practiceapi.geeksforgeeks.org/api/latest/problems/{slug}/hints/solution/"
    r = requests.get(editorial_url, cookies=cookies, headers=HEADERS)
    if r.status_code == 403:
        #print("Cookies Expired for Editorial Fetching")
        get_cookies_from_login_details(
            LOGIN_DETAILS[0]["email"], LOGIN_DETAILS[0]["password"], "cookies.json"
        )
        return get_editorial()
    solution_json = r.json()
    #print("Solution Fetched Successfully")
    results = solution_json["results"]
    for result in results["hints"]:
        if result["lang"] == "Python3":
            if result["full_func"]:
                #print("Python3 Solution Found")
                return result
    #print("Python3 Solution Not Found")
    for result in results["hints"]:
        if result["lang"] == "Java":
            if result["full_func"]:
                #print("Java Solution Found")
                return result
    #print("Java Solution Not Found")
    for result in results["hints"]:
        if result["full_func"]:
            #print(f"Using {result['lang']} Solution")
            return result
    raise Exception("No Solution Found")


def submit_code():
    cookies = get_cookies("submit_cookies.json")
    cookies_2 = get_cookies("submit_cookies_2.json")
    slug = get_slug()
    COMPILE_URL = f"https://practiceapiorigin.geeksforgeeks.org/api/latest/problems/{slug}/compile/"

    submit_data = prepare_submission_data()
    if submit_data is None:
        return None
    res = requests.post(
        COMPILE_URL, files=submit_data, cookies=cookies, headers=HEADERS
    )
    if res.status_code == 403:
        #print("Cookies Expired for Submission 1")
        get_cookies_from_login_details(
            LOGIN_DETAILS[1]["email"],
            LOGIN_DETAILS[1]["password"],
            "submit_cookies.json",
        )
        return submit_code()
    data = res.json()
    res_2 = requests.post(
        COMPILE_URL, files=submit_data, cookies=cookies_2, headers=HEADERS
    )
    if res_2.status_code == 403:
        #print("Cookies Expired for Submission 2")
        get_cookies_from_login_details(
            LOGIN_DETAILS[2]["email"],
            LOGIN_DETAILS[2]["password"],
            "submit_cookies_2.json",
        )
        return submit_code()
    data_2 = res_2.json()
    submission_id = data["results"]["submission_id"]
    submission_id_2 = data_2["results"]["submission_id"]
    #print("Code Submitted Successfully with submission id: " + submission_id)
    #print("Code Submitted Successfully with submission id: " + submission_id_2)
    return (submission_id, submission_id_2)


def check_submission(submission_id, submission_id_2):
    #print("Checking Submission Status")
    cookies = get_cookies("submit_cookies.json")
    cookies_2 = get_cookies("submit_cookies_2.json")
    CHECK_URL = f"https://practiceapiorigin.geeksforgeeks.org/api/latest/problems/submission/result/"
    submission_data = {
        "sub_id": (None, submission_id),
        "sub_type": (None, "solutionCheck"),
        "pid": (None, get_problem_id(stats=get_stats())),
    }
    submission_data_2 = {
        "sub_id": (None, submission_id_2),
        "sub_type": (None, "solutionCheck"),
        "pid": (None, get_problem_id(stats=get_stats())),
    }
    res = requests.post(
        CHECK_URL, files=submission_data, cookies=cookies, headers=HEADERS
    )
    res_2 = requests.post(
        CHECK_URL, files=submission_data_2, cookies=cookies_2, headers=HEADERS
    )
    data = res.json()
    data_2 = res_2.json()
    while data["status"] == "QUEUED":
        res = requests.post(CHECK_URL, files=submission_data, cookies=cookies)
        data = res.json()
        sleep(1)
        #print(f"Submission Status of account 1 : {data['status']}")
    while data_2["status"] == "QUEUED":
        res_2 = requests.post(CHECK_URL, files=submission_data_2, cookies=cookies_2)
        data_2 = res_2.json()
        sleep(1)
        #print(f"Submission Status of account 2 : {data_2['status']}")
    #print(f"Your Code Status of account 1 : {data['view_mode']}")
    #print(f"Your Code Status of account 2 : {data_2['view_mode']}")
    #print(f"Test cases passed for account 1 : {data['test_cases_processed']}/{data['total_test_cases']}")
    with open("./profileapp/logs.txt","w") as f:
        f.write(f"Test cases passed for account 1 : {data['test_cases_processed']}/{data['total_test_cases']}")
        f.write(f"Test cases passed for account 2 : {data_2['test_cases_processed']}/{data_2['total_test_cases']}")
    #print(f"Test cases passed for account 2 : {data_2['test_cases_processed']}/{data_2['total_test_cases']}")
    return (data, data_2)


def startAutomate():
    # return "Santhosh"
    # global main_log
    # main_log=""
    submission_id, submission_id_2 = submit_code()

    if submission_id:
        data, data_2 = check_submission(submission_id, submission_id_2)
        sleep(2)
        pod_stats = get_pod_stats("submit_cookies.json")
        pod_stats_2 = get_pod_stats("submit_cookies_2.json")
        with open("./profileapp/logs.txt","a") as f:
            f.write("Current Problem of the Day Streak for account 1 :  "+ str(pod_stats["pod_solved_current_streak"]))
            f.write("Current Problem of the Day Streak for account 2 :  "+ str(pod_stats_2["pod_solved_current_streak"]))
            f.write("Current Geek Bits for account 1 :  " + str(pod_stats["active_bits"]))
            f.write("Current Geek Bits for account 2 :  " + str(pod_stats_2["active_bits"]))
        #print("Current Problem of the Day Streak for account 1 :  "+ str(pod_stats["pod_solved_current_streak"]))
        #print("Current Problem of the Day Streak for account 2 :  "+ str(pod_stats_2["pod_solved_current_streak"]))

        #print("Current Geek Bits for account 1 :  " + str(pod_stats["active_bits"]))
        #print("Current Geek Bits for account 2 :  " + str(pod_stats_2["active_bits"]))
    else:
        print("Problem not Submitted")
    #print("Done...")
    #print("\nExiting in 5 seconds...")
    sleep(5)
    return 

