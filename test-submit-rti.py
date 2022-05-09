from io import BytesIO
from random import randrange

import pytesseract
import requests
from lxml import etree, html
from PIL import Image

headers = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "Upgrade-Insecure-Requests": "1",
    "Origin": "https://rtionline.gov.in",
    # "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryiExwe0CefHJZlaUF",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://rtionline.gov.in/request/request.php",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
}

headers_captcha = {
    "Connection": "keep-alive",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
    "sec-ch-ua-platform": '"Linux"',
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Dest": "image",
    "Referer": "https://rtionline.gov.in/request/request.php",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
}

sess = requests.Session()
response = sess.get("https://rtionline.gov.in/request/request.php", headers=headers)
response_text = response.text
to_search = '<input type="hidden" name="hndSessionFromId" value="'
temp = response_text[response_text.find(to_search) + len(to_search):]
form_id = temp[:temp.find('" />')]
print(form_id)

params_captcha = {
    "rand": str(randrange(100000, 999999)),
}

# captcha in the same session
response = sess.get(
    "https://rtionline.gov.in/captcha_code_file.php",
    headers=headers_captcha,
    params=params_captcha,
    cookies=sess.cookies,
)
catpcha_img = BytesIO(response.content)
img = Image.open(catpcha_img)

captcha_ocr = pytesseract.image_to_string(img).strip()[0:6]
print(f"{captcha_ocr=}")

ministryId: str = input("ministryId: ")
departmentId: str = input("departmentId: ")
email: str = input("email: ")
name: str = input("name: ")
gender: str = input("gender: ")
address1: str = input("address1: ")
address2: str = input("address2: ")
pincode: str = input("pincode: ")
stateId: str = input("stateId: ")
description: str = input("description: ")
captcha: str = captcha_ocr
formId: str = str(form_id)

ministryId = "75"
departmentId = "2"
email = "rti@sflc.in"
name = "Nikhil K Singh"
gender = "M"
address1 = "K-9, 2nd floor"
address2 = "Birbal Road, Jangpura Ext"

description = """This is with respect to the Central Government RTI portal (rtionline.gov.in), The applicant wishes to seek the following queries:

1. Is there any RTI related API available for the general public? Like an API that can be used to get the status of an already filed RTI or an API to submit/file a RTI.

2. If no, then is there any progress being made towards this?

If the information sought herein is with any other public authority please transfer the application to such authority within a period 5 days (as per S. 6(3) of the Right to Information Act, 2005) and inform me of such transfer and related communication.

I am a citizen of of India and I am requesting for this information as a citizen of India. I am ready to pay any expenses related to making photocopies of documents on intimation of the same.
"""

files = {
    "SearchMinistry": (None, ""),
    "MinistryId": (None, ministryId),
    "DepartmentId": (None, departmentId),
    "Email": (None, email),
    "MobileStdCode": (None, "+91"),
    "cell": (None, ""),
    "ConfirmEmail": (None, email),
    "Name": (None, name),
    "gender": (None, gender),
    "address1": (None, address1),
    "address2": (None, address2),
    "address3": (None, ""),
    "pincode": (None, pincode),
    "chkCountry": (None, "001"),
    "stateId": (None, stateId),
    "txtCountry": (None, ""),
    "PhoneStdCode": (None, "+91"),
    "phone": (None, ""),
    "Citizenship": (None, "I"),
    "BPL": (None, "N"),
    "bplCardNo": (None, ""),
    "YearOfUssue": (None, ""),
    "IssuAuthority": (None, ""),
    "Description": (None, description),
    "DocumentFile": (None, ""),
    "chkPdfFileType": (None, ""),
    "6_letters_code": (None, captcha),
    "requestSubmit": (None, "Make Payment"),
    "hndSessionFromId": (None, formId),
}

response = sess.post(
    "https://rtionline.gov.in/request/request.php",
    headers=headers,
    files=files,
    cookies=sess.cookies,
)

print(response.url)
print(sess.cookies["PHPSESSID"])

# eggsml: html.HtmlElement = html.fromstring(response.text)
# status_info_form = eggsml.xpath("//*[@id='content-frm']/div/form")[0]


# etree.tostring(status_info_form).decode("UTF-8").replace("\n", "").replace("\t", "")

