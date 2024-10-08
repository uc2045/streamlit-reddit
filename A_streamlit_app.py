import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json

# Replaced
# Authenticate to Firestore with the JSON account key.
# db = firestore.Client.from_service_account_json("st-firestore-credentials.json")

# With:
key_dict = json.loads(st.secrets["firestore_key"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="st-firestore")

# # Create a reference to the Google post.
# doc_ref = db.collection("posts").document("Google")

# # Then get the data at that reference.
# doc = doc_ref.get()

# # Let's see what we got!
# st.write("The id is: ", doc.id)
# st.write("The contents are: ", doc.to_dict())


# # Now let's make a reference to ALL of the posts
# posts_ref = db.collection("posts")

# # For a reference to a collection, we use .stream() instead of .get()
# for doc in posts_ref.stream():
# 	st.write("The id is: ", doc.id)
# 	st.write("The contents are: ", doc.to_dict())

# Streamlit widgets to let a user create a new post
title = st.text_input("Post title")
url = st.text_input("Post url")
submit = st.button("Submit new post")

# Once the user has submitted, upload it to the database
if title and url and submit:
	doc_ref = db.collection("posts").document(title)
	doc_ref.set({
		"Title": title,
		"url": url
	})

# And then render each post, using some light Markdown
posts_ref = db.collection("posts")
for doc in posts_ref.stream():
	post = doc.to_dict()
	title = post["Title"]
	url = post["url"]

	st.subheader(f"Post: {title}")
	st.write(f":link: [{url}]({url})")