import requests
import time
import random

headers = {
    "Accept": "application/json, text/plain, */*",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODk3MDgzOTIsInVzZXJfdXVpZCI6IjkyYjQ1MzE5LTU3NjUtNGZjYS04YzA2LWY2OGJmMTFlYjVhMSIsInN0YXR1cyI6dHJ1ZSwiZW1haWwiOiI0RG0xbkBzc2JfZ2gwc3QuZzB2LnRyIiwicm9sZSI6ImFkbWluIiwibmFtZSI6IkFkbWluIiwic3VybmFtZSI6IkFkbWluIn0.1Xq3ybAbl-oAZN5paoAVlHWFPO6sxvJ7IhC9_MUaFfg",
    "Content-Type": "application/json",
    "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Opera GX\";v=\"100\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "Referer": "https://ghost.ssb.gov.tr/",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0'
}

# form_referee_url = "https://api-ghost.ssb.gov.tr/api/v1/forms/referee"
# form_url = "https://api-ghost.ssb.gov.tr/api/v1/forms"
# referee_url = "https://api-ghost.ssb.gov.tr/api/v1/users/referee"
# referees = requests.get(referee_url, headers=headers)
# forms = requests.get(form_url, headers=headers)
#
# referee_ids = [x['uuid'] for x in referees.json()]
# forms_ids = [x['uuid'] for x in forms.json() if x['status'] == 'Tamamlandı']
# check_idx = []
# rek = ['890c8013-5dff-4c02-a86f-79a92a5d34af',
#        'e85f902c-84bb-4182-95d2-86a85468b2e5',
#        'b42086f1-1798-4629-98a8-d6767bb97dbf',
#        'd7f090e6-febd-4028-8a21-16e820d4f47a',
#        '8f95f1c4-8397-47ea-a733-87a4bdb46b75']
# for form_id in forms_ids:
#     if form_id == '5f81b603-adb9-4e52-9baa-bf7271f9839c':
#         print('mustafa test')
#         continue
#     user_id = []
#     i = 0
#     while True:
#         tmp_index = random.randint(0, 100000000) % len(referee_ids)
#         if tmp_index not in check_idx:
#             check_idx.append(tmp_index)
#             if referee_ids[tmp_index] not in user_id and referee_ids[tmp_index] not in rek:
#                 user_id.append(referee_ids[tmp_index])
#                 i += 1
#         elif len(check_idx) == len(referee_ids):
#             check_idx = []
#         if i > 2:
#             break
#     tmp_form_data = {
#         "user_id": user_id,
#         "form_id": form_id
#     }
#     res = requests.post(form_referee_url, json=tmp_form_data, headers=headers)
#     print(res.json())
#     time.sleep(1)





# with open('hakem.csv', encoding='utf-8') as f:
#     for line in f:
#         lines = line.split(';')
#         mobile_phone = ''
#         address = '-'
#         if lines[7].strip().replace(' ', '') == '':
#             mobile_phone = lines[6].strip().replace(' ', '')
#         elif lines[6].strip().replace(' ', '') == '':
#             mobile_phone = lines[7].strip().replace(' ', '')[:10]
#             address = lines[7].strip().replace(' ', '')
#         else:
#             mobile_phone = lines[6].strip().replace(' ', '')
#             address = lines[7].strip().replace(' ', '')
#         tmp_data = {
#             "person_national_id": lines[2],
#             "name": ' '.join(lines[1].split(' ')[:-1]),
#             "surname": lines[1].split(' ')[-1],
#             "email": lines[4].strip(),
#             "mobile_phone": mobile_phone,
#             "address": address,
#             "education_level": "lisans",
#             "corporation": lines[3],
#             "birth_date": "01-01-1900"
#         }
#         res = requests.post("https://api-ghost.ssb.gov.tr/api/v1/users", json=tmp_data, headers=headers)
#         print(res.json())
#         time.sleep(3)

