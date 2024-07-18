# Assignment Setup

* ## Create a virtual environment
        python3 -m venv env

* ## Activate the virtual environment
        source env/bin/activate

* ## Install all required packages
        cd app 
        
        pip install -r requirements.txt

* ## Start the Server
        uvicorn main:app --reload
    * Server will run on default port 8000


* ## Go to the `localhost:8000/docs` routes to see Swagger UI of routes
    ### provide correct deails and get the data
