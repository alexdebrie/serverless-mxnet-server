# Serverless-MXNet-Server

**This is a work in progress**. Check out the [outstanding problems](#outstanding-problems) section below.

AWS has developed [MXNet](https://mxnet.apache.org/), a deep learning framework. Recently, they [released a model server](https://aws.amazon.com/blogs/aws/aws-contributes-to-milestone-1-0-release-and-adds-model-serving-capability-for-apache-mxnet/?nc1=b_rp) for MXNet, which makes it easy to set up an endpoint for serving your models.

This is a project to deploy the MXNet server in a Serverless application. Autoscaling, low-management model serving FTW ⚡️.

## Usage

1. Install the [Serverless Framework](https://serverless.com):

    ```bash
    $ npm install -g serverless
    ```

2. Install this repository as a template:

    ```bash
    $ sls install --url https://github.com/alexdebrie/serverless-mxnet-server && cd serverless-mxnet-server
    $ npm install
    ```

3. Deploy!

    ```bash
    $ sls deploy
    ```

4. Call your endpoint!

    ```
    # Set your BASE_URL with the endpoint given with sls deploy
    $ export BASE_URL="https://58kx6wsxej.execute-api.us-east-1.amazonaws.com/dev"
    $ curl -X POST ${BASE_URL}/squeezenet/predict -F "data=@kitten.jpg"
    ```

## Outstanding problems

I'm having trouble getting the image data through API Gateway in the format expected by the MXNet server.

To get it working locally:

1. Create a virtual environment and install all required packages:

    ```bash
    $ virtualenv venv --python=python3 && source venv/bin/activate
    $ pip install -r requirements.txt
    ```

2. Start your app locally:

    ```bash
    $ sls wsgi serve
    ```

3. Make a request against it:

    ```bash
    curl -X POST http://127.0.0.1:5000/squeezenet/predict -F "data=@kitten.jpg"
    {
      "prediction": [
        [
          {
            "class": "n02124075 Egyptian cat",
            "probability": 0.9408263564109802
          },
          {
            "class": "n02127052 lynx, catamount",
            "probability": 0.05596580728888512
          },
          {
            "class": "n02123045 tabby, tabby cat",
            "probability": 0.0025502473581582308
          },
          {
            "class": "n02123159 tiger cat",
            "probability": 0.00034319929545745254
          },
          {
            "class": "n02123394 Persian cat",
            "probability": 0.000268968433374539
          }
        ]
      ]
    }
    ```
