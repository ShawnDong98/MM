#!/bin/sh

# Get the preprocessed data from here:
# https://drive.google.com/file/d/1s7C2ek_mSKgmR_Tk_cjHuULHEo4gUsxs/view?usp=sharing

# Ref: https://qr.ae/pG6hRe
# Get an OAuth token:
# Go to OAuth 2.0 Playground(https://developers.google.com/oauthplayground/)
# In the “Select the Scope” box, scroll down, expand “Drive API v3”, and select https://www.googleapis.com/auth/drive.readonly
# Click “Authorize APIs” and then “Exchange authorization code for tokens”. Copy the “Access token”; you will be needing it below.

curl -H "Authorization: Bearer ya29.A0ARrdaM-4tnf-rd36Uquj2BBZDeHmY3PD_6ne8e0njx2Tu7125BntcKkcD6Gle4ztHyTUf6aTuEUDf9DtD5_ugLwMZYr0LueLEfn0BXMJBU_rKuLoL-wAj1TE7WgTf-3D7K2Fa7upENj6ZA5i1iOGHEacSpnc" https://www.googleapis.com/drive/v3/files/1s7C2ek_mSKgmR_Tk_cjHuULHEo4gUsxs?alt=media -o data.zip
unzip data.zip 
