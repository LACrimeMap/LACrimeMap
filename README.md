# LACrimeMap
## Team:
Weihao Zhou, Kaiwen Yang, Xu Han, Laura McCallion
## About:
This project attempts to predict criminal activity by analyzing
trends in LA Crime Data from [Los Angeles Open Data](https://data.lacity.org/).
The [data source](https://data.lacity.org/A-Safe-City/Arrest-Data-from-2010-to-Present/yru6-6re4) updates weekly.
The project also visualizes the data and functions as an interactive exploratory
tool. The website can be found [here](http://35.245.178.4:1050).
## Project Architecture:
This project uses MongoDB as the database. All data acquired are stored in raw form to the 
database (with de-duplication). An abstract layer is built in `database.py`.
A `plot.ly` & `dash` app is serving this web page. Actions on responsive components on the page 
are redirected to `app.py` which will then update certain components on the page. 