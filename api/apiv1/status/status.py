from io import BytesIO
from random import randrange
from typing import Any

import pytesseract
import requests
from api import deps
from fastapi import APIRouter, Depends, HTTPException
from lxml import etree, html
from PIL import Image
from schemas import status

router = APIRouter()


@router.post("/rtistatus/")
async def get_rti_status(content: status.StatusIn) -> Any:

    headers = {
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "Upgrade-Insecure-Requests": "1",
        "Origin": "https://rtionline.gov.in",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://rtionline.gov.in/request/status.php",
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
        "Referer": "https://rtionline.gov.in/request/status.php",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    }

    sess = requests.Session()
    response = sess.get("https://rtionline.gov.in/request/status.php", headers=headers)
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

    captcha_ocr = pytesseract.image_to_string(img).strip()
    print(f"{captcha_ocr=}")

    data = {
        "registration_no": "DITEC/R/E/22/00174",
        "Email": "rattanmeek@sflc.in",
        "6_letters_code": str(captcha_ocr),
        "Submit": "Submit",
    }

    response = sess.post(
        "https://rtionline.gov.in/request/status.php",
        headers=headers,
        data=data,
        cookies=sess.cookies,
    )

    if "captcha_code_file.php" in (response_text := response.text):
        raise HTTPException(status_code=500, detail="Captcha was wrong! Please retry!")

    eggsml: html.HtmlElement = html.fromstring(response_text)
    status_info_form = eggsml.xpath("//*[@id='content-frm']/div/form")[0]

    return etree.tostring(status_info_form).decode("UTF-8").replace("\n", "").replace("\t", "")
