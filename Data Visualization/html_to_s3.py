# Uploading file to S3 bucket.
k = Key(website_bucket)
k.key = "lab_1_2.jpg"
k.set_contents_from_filename("lab_1_2.jpg")
