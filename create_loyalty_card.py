import os
from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
from google.auth import jwt, crypt

load_dotenv()

# Authenticate

key_file_path = 'google_wallet_key.json'
credentials = Credentials.from_service_account_file(
    key_file_path,
    scopes=[
        'https://www.googleapis.com/auth/wallet_object.issuer'
    ]
)

client = build('walletobjects', 'v1', credentials=credentials)

# Options

issuer_id = os.getenv('ISSUER_ID')
class_id = 'CLASS_ID'
object_id = 'OBJECT_ID'
program_name = 'PROGRAM_NAME'
issuer_name = 'ISSUER_NAME'
background_color = '#FF0000'
barcode_type = 'CODE_128'
hero_image = 'HERO_IMAGE_URL'
logo_image = 'LOGO_IMAGE_URL'
barcode_value = 'BARCODE_VALUE'
alt_text = ''

def create_class():
    try:
        client.loyaltyclass().get(resourceId=f'{issuer_id}.{class_id}').execute()
    except HttpError as e:
        if e.status_code != 404:
            # Something else went wrong...
            print(e.error_details)
            return f'{issuer_id}.{class_id}'
    else:
        print(f'Class {issuer_id}.{class_id} already exists!')
        return f'{issuer_id}.{class_id}'
    
    loyalty_class = {
        "id": f'{issuer_id}.{class_id}',
        "reviewStatus": "UNDER_REVIEW",
        "programLogo": {
            "sourceUri": {
                "uri": logo_image
            },
            "contentDescription": {
                "defaultValue": {
                    "language": "en-US",
                    "value": "LOGO_IMAGE_DESCRIPTION"
                }
            }
        },
        "localizedIssuerName": {
            "defaultValue": {
                "language": "en-US",
                "value": issuer_name
            }
        },
        "localizedProgramName": {
            "defaultValue": {
                "language": "en-US",
                "value": program_name,
            },
        },
        "hexBackgroundColor": background_color,
        "heroImage": {
            "sourceUri": {
                "uri": hero_image
            },
            "contentDescription": {
                "defaultValue": {
                    "language": "en-US",
                    "value": "HERO_IMAGE_DESCRIPTION"
                }
            }
        } if hero_image else None,
    }
    
    try:
        response = client.loyaltyclass().insert(body=loyalty_class).execute()
        print(response)
    except Exception as e:
        print(f'Error inserting loyalty class: {e}')


def create_object():
    try:
        client.loyaltyobject().get(resourceId=f'{issuer_id}.{object_id}').execute()
    except HttpError as e:
        if e.status_code != 404:
            # Something else went wrong...
            print(e.error_details)
            return f'{issuer_id}.{object_id}'
    else:
        print(f'Object {issuer_id}.{object_id} already exists!')
        return f'{issuer_id}.{object_id}'
    
    loyalty_object = {
        "id": f'{issuer_id}.{object_id}',
        "classId": f'{issuer_id}.{class_id}',
        "state": "ACTIVE",
        "barcode": {
            "type": barcode_type,
            "value": barcode_value,
            "alternateText": alt_text
        },
    }
    
    try:
        response = client.loyaltyobject().insert(body=loyalty_object).execute()
        print(response)
    except Exception as e:
        print(f'Error inserting loyalty object: {e}')


def main():
    
    create_class()
    create_object()
    
    claims = {
        'iss': credentials.service_account_email,
        'aud': 'google',
        'origins': ['www.example.com'],
        'typ': 'savetowallet',
        'payload': {
            'loyaltyObjects': [{
                "id": f'{issuer_id}.{object_id}',
                "classId": f'{issuer_id}.{class_id}',
            }]
        }
    }

    # The service account credentials are used to sign the JWT
    signer = crypt.RSASigner.from_service_account_file(key_file_path)
    token = jwt.encode(signer, claims).decode('utf-8')

    print('Add to Google Wallet link:')
    print(f'https://pay.google.com/gp/v/save/{token}')

    return f'https://pay.google.com/gp/v/save/{token}'


if __name__ == '__main__':
    main()
