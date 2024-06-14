# Google Wallet Card Maker

## Instructions

1. Install the following requirements
    - python google api client
    - pytohn-dotenv

2. Go to Google cloud console and create a new project
   - Enable the Google Wallet API for the project
   - Create a new service account and download the credentials file named `gogole_wallet_key.json`

3. Go to the Google Wallet API Console by going [here](https://developers.google.com/wallet) and clicking get started at the bottom of the page
    - Complete your business profile 
    - Copy your issuer ID and add it to a `.env` file in the root of this project

3. Update the `create_loyalty_card.py` script with the options you want for customizing your card

4. Run the script `python3 create_loyalty_card.py` to get a link to add the card to your Google Wallet