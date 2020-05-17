# razer-grain

This is my team Grain's submission for the Razer Fintech Digital Hackathon. 

## Usage

### FWD KYC

We make use of FWD's eKYC API in order to verify the user's NRIC during registration.

In ```grain_site/settings.py```, change the fields ```KYC_URL``` and ```KYC_KEY``` to the FWD API URL and x-api-key respectively.

### Dependencies

We use Django, a Python framework with several other Python packages, thus, please have Python 3.6 or later installed. 
Then, run the following command to install the required libraries.

```shell
pip install -r requirements.txt
```

### Running

```shell
cd grain_site
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```