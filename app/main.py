from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator


from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.requests import Request

from fastapi import FastAPI, File, UploadFile
import pytesseract
from transformers import pipeline
import cv2
import io
from random import randint
import uuid
from PIL import Image
from fastapi.responses import JSONResponse
import cv2
import logging
import sys
import numpy as np
import os
import datetime

app = FastAPI(title="Data Science Challenge - Invoice Extraction",
    description="In today's increasingly complicated world with a variety of businesses and procedures within, manually extracting information from invoices can be time-consuming. Additionally, there are various issues that arise throughout the processing of an invoice. Develop a method to retrieve this data automatically that could help businesses digitize and automate the whole process of invoice extraction.",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url=None,  
    swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect")

@app.get("/")
def home():
    return "Hello World"


# Configure the logging
logging.basicConfig(
    filename="invoiceExtraction_"+datetime.datetime.today().strftime('%Y-%m-%d')+".log",  
    level=logging.INFO,     
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def imageEnhancements(inputImage):
    # Identify the bold characters within the image file
    try:
        logging.info(f"Starting imageEnhancements module...>>> {inputImage}")
        logging.info(f"Identify the bold characters within the image file")
        img = cv2.imread(inputImage)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)[1]
        kernel = np.ones((5,5),np.uint8)
        kernel2 = np.ones((3,3),np.uint8)
        marker = cv2.dilate(thresh,kernel,iterations = 1)
        mask=cv2.erode(thresh,kernel,iterations = 1)
        while True:
            tmp=marker.copy()
            marker=cv2.erode(marker, kernel2)
            marker=cv2.max(mask, marker)
            difference = cv2.subtract(tmp, marker)
            if cv2.countNonZero(difference) == 0:
                break

        marker_color = cv2.cvtColor(marker, cv2.COLOR_GRAY2BGR)
        out=cv2.bitwise_or(img, marker_color)
        cv2.imwrite('boldImage.jpg', out)

        image1 = cv2.imread("boldImage.jpg", 0)
        image2 = cv2.imread(inputImage, 0)

        # Calculate the per-element absolute difference between 
        # two arrays or between an array and a scalar
        diff = 255 - cv2.absdiff(image1, image2)
        cv2.imwrite("boldImageDiff.jpg", diff)
        logging.info(f"Removed the bold characters within the uploaded image")
    except:
        logging.error(f"Bold characters module failed! for the {inputImage}, Please check the image!")
        sys.exit(f"Bold characters module failed! for the {inputImage},Please check the image!")


    try:
        logging.info(f"Image processing within the uploaded image started")
        # Load the image
        image = cv2.imread("boldImageDiff.jpg", cv2.IMREAD_COLOR)
        # image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Gaussian blur 
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        # thresholding 
        _, binary_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # adaptive thresholding 
        binary_image = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        # Save image
        cv2.imwrite('enhanced_image.jpg', binary_image)

        logging.info(f"Successfully completed imageEnhancements module...>>> {inputImage}")
        return binary_image
    except:
        logging.error(f"imageEnhancements module failed! for the {inputImage}, Please check the image!")
        sys.exit(f"imageEnhancements module failed! for the {inputImage},Please check the image!")


@app.post("/upload/")
async def upload_image(file: UploadFile):
    
    if not file:
        logging.info(f"<<<< No file received, Stopped Invoice Extarction >>>>")
        return JSONResponse(content={"error": "No file received"}, status_code=400)

    # Save the uploaded file to a temporary location
    with open(file.filename, "wb") as f:
        f.write(file.file.read())
    logging.info(f"<<<< Starting the Invoice Extarction >>>>")
    logging.info(f"The Uploaded image found : {file.filename}")

    # Calling the imgae enhancements module
    binary_image = imageEnhancements(file.filename)

    # Use Tesseract to perform OCR on the uploaded image
    text = pytesseract.image_to_string(binary_image)
    logging.info(f"The extracted text from the image :\n {text}")

    try:
        logging.info(f"Using Hugging face transformers : layoutlm for the {file.filename}")
        image = Image.open(r"enhanced_image.jpg")
        nlp = pipeline("document-question-answering",model="impira/layoutlm-invoices",framework = "pt")
        finalResultWithImageProc=[]
        finalResultWithoutImageProc=[]
        for q in ["What is the Company Name?", "What is the Amount?", "What is the Address?", "What is the date?"]:
            #print(nlp(image,q)[0]['answer'])
            finalResultWithImageProc.append(nlp(image,q)[0]['answer'])
        image = Image.open(file.filename)
        for q in ["What is the Company Name?", "What is the Amount?", "What is the Address?", "What is the date?"]:
            #print(nlp(image,q)[0]['answer'])
            finalResultWithoutImageProc.append(nlp(image,q)[0]['answer'])

        logging.info(f"Info successfully extracted from the image! ")

    except:
        logging.error(f"Hugging face transformers module failed! for the {file.filename}, Please check the image!")

    logging.info(f"The Invoice module is completed for the {file.filename}")
    logging.info(f"<<<< Completed the Invoice Extarction >>>>")

    # removing the  temp images
    os.remove("boldImage.jpg")
    os.remove("boldImageDiff.jpg")
    os.remove("enhanced_image.jpg")
    return JSONResponse(content={"FinalResultWithImageProcsessing" :{"Company Name": finalResultWithImageProc[0], "Amount": finalResultWithImageProc[1], "Address": finalResultWithImageProc[2], "Date": finalResultWithImageProc[3]},
                                "FinalResultWithoutImageProcsessing" :{"Company Name": finalResultWithoutImageProc[0], "Amount": finalResultWithoutImageProc[1], "Address": finalResultWithoutImageProc[2], "Date": finalResultWithoutImageProc[3]}})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Instrumentator().instrument(app).expose(app)
