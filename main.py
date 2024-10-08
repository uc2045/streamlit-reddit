import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json
import toml

# Replace:
# db = firestore.Client.from_service_account_json("firebase-key.json")

# With:

# # Load the secrets from secrets.toml
secrets = toml.load("./.streamlit/secrets.toml")

# # Create credentials from the service account key
creds = service_account.Credentials.from_service_account_info(secrets)
print("KV1 CREDS:", creds)
db = firestore.Client(credentials=creds, project="st-firebase-b8bed")
print("KV2 DB:", db)

# Streamlit widgets to let a user create a new post
title = st.text_input("Post title")
print("KV3 title:", title)
url = st.text_input("Post url")
print("KV4 URL:", url)
submit = st.button("Submit new post")

# Once the user has submitted, upload it to the database
if title and url and submit:
	doc_ref = db.collection("posts").document(title)
	doc_ref.set({
		"title": title,
		"url": url
	})

# And then render each post, using some light Markdown
posts_ref = db.collection("posts")
for doc in posts_ref.stream():
	post = doc.to_dict()
	title = post["title"]
	url = post["url"]

	st.subheader(f"Post: {title}")
	st.write(f":link: [{url}]({url})")
	print("KV99 URL", url)
