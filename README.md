# NASA NeoWs API
###### Author: Jide Ogunjobi

1. Install pipenv by running `pipenv install`. This should install all required packages for a successful execution
2. Run `pipenv shell` to jump into the virtual environment
3. Rename the **env_template** file to **.env**
4. Copy and paste your API Key from the NASA API website into the placeholder in the newly created **.env** file. If you dont have an API Key, go to <https://api.nasa.gov> to create a new key
5. Run `python main.py --input_date '<your-end-date>'`. Your date format must be in YYYY-MM-DD format. For example `python main.py --input_date '2023-05-01'`. Don't forget the quotes around the date