import streamlit as st
import boto3
from PIL import Image, ImageDraw
import io
import os

# AWS clients
try:
    s3 = boto3.client('s3')
    rekognition = boto3.client('rekognition')
except Exception as e:
    st.error(f"❌ Failed to initialize AWS clients: {e}")

# Your config
BUCKET_NAME = 'smile-detection-lab-yourname'  # CHANGE THE BUCKET NAME
IMAGE_KEY = 'uploaded.jpg'

st.set_page_config(page_title="Smile & Emotion Detection", layout="centered")
st.title("😄 Smile & Emotion Detection using Amazon Rekognition':)🤩")
st.markdown("This app ate the Smile-Smile Fruit! 🍖😆")

# Step 1: Capture image using Streamlit camera
uploaded_img = st.camera_input("📸 Capture your face")

if uploaded_img:
    st.success("Image captured successfully!🎬")

    # Step 2: Convert and save image as JPEG in memory
    image = Image.open(uploaded_img)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()

    # Step 3: Upload to S3
    try:
        s3.put_object(Bucket=BUCKET_NAME, Key=IMAGE_KEY, Body=img_bytes)
        st.info("📤 Image uploaded to S3 successfully.")
    except Exception as e:
        st.error(f"❌ Failed to upload to S3: {e}")

    # Step 4: Call Rekognition
    try:
        response = rekognition.detect_faces(
            Image={'Bytes': img_bytes},
            Attributes=['ALL']
        )
        st.success("✅ Rekognition analysis completed.")
    except Exception as e:
        st.error(f"❌ Error calling Rekognition: {e}")
        response = None

    # Step 5: Draw bounding boxes & display info
    if response and 'FaceDetails' in response:
        draw = ImageDraw.Draw(image)
        img_width, img_height = image.size

        for i, face in enumerate(response['FaceDetails'], start=1):
            st.subheader(f"🧍 Face {i}")

            # Smile
            smile = face['Smile']
            st.write(f"**Smile:** {'😄 Smiling' if smile['Value'] else '😐 Not Smiling'} "
                     f"(Confidence: {smile['Confidence']:.2f}%)")

            # Emotions (Top 5)
            emotions = sorted(face['Emotions'], key=lambda x: x['Confidence'], reverse=True)[:5]
            st.write("**Top Emotions:**")
            for emo in emotions:
                st.write(f"- {emo['Type']}: {emo['Confidence']:.2f}%")

            # Draw bounding box
            box = face['BoundingBox']
            left = img_width * box['Left']
            top = img_height * box['Top']
            width = img_width * box['Width']
            height = img_height * box['Height']
            draw.rectangle([left, top, left + width, top + height], outline="red", width=3)

        # Show annotated image
        st.image(image, caption="🔍 Detected Faces with Bounding Boxes", use_column_width=True)

