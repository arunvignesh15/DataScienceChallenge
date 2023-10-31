<h1 align="center">Data Science Challenge</h1>

## Case study 

In today's increasingly complicated world with a variety of businesses and procedures within, manually extracting information from invoices can be time-consuming. Additionally, there are various issues that arise throughout the processing of an invoice. Develop a method to retrieve this data automatically that could help businesses digitize and automate the whole process of invoice extraction.

## Outcome

Using this solution, user will be able to extract the below outcomes as result when user uploads a invoice image.
* Company Name
* Amount
* Address
* Date

## Installation

There are only two prerequisites:

* [Docker](https://docs.docker.com/get-docker/)
* [Docker-compose](https://docs.docker.com/compose/install/)

Having both, you'll need to clone the repository:

``` bash
git clone https://github.com/Kludex/fastapi-prometheus-grafana
```

## Usage

You'll need to run the docker containers:

``` bash
docker-compose up
```

Now you have access to those three containers and their respective ports:

* FastAPI: http://localhost:8000/
* Prometheus: http://localhost:9090/
* Grafana: http://localhost:3000/

To view the FastAPI Swagger page is available on `http://localhost:8000/docs` endpoint, here you can see all aviable routes which has been added.

On the FastAPI, you can access `/metrics` endpoint to see the data Prometheus is scraping from it.

## How would you montior the solution?

Here i have come up with 2 approches 
1. Using Log monitoring 
2. Using Prometheus and Grafana 

The Log files will be created for each execution within the container image.

Also, you can montior the solution using Grafana, which provides 
* Total request per minutes
* Request per minutes
* Errors per seconds
* Average response time
* Request Duration
* Memory Usage
* CPU Usage

You can access via `http://localhost:3000/`

## How would you enchanced the given data?

For enchancement i have used Image processing technique to the user uploaded image. At first i have identified the bold characters fom the image and removed from the user uploaded image, then later on i have appplied the below techiques 

* Threshold
* GaussianBlur
* Adaptive Threshold

## Output

As a output, `FinalResultWithImageProcsessing` and `FinalResultWithoutImageProcsessing` keys dict will be provided.

The `FinalResultWithImageProcsessing` results means the output from the enchanced image after the image processing.

The `FinalResultWithoutImageProcsessing` results means the output from the raw user uploaded image without the image processing.
 

_{
  "FinalResultWithImageProcsessing": {
    "Company Name": "TRADING",
    "Amount": "37,00",
    "Address": ",H0.284,JALAN HARMONT",
    "Date": "3/2,"
  },
  "FinalResultWithoutImageProcsessing": {
    "Company Name": "tan chay yee ABC HO TRADING",
    "Amount": "31.00",
    "Address": "81100",
    "Date": "09/01/2019"
  }
}_

