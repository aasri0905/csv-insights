# csv-insights
# [`Demo video`](https://drive.google.com/file/d/14sWuJ7sYpELSb85nhNT_yEaOXgahqWQz/view?usp=sharing)
following project is my assignment submission for tensorgo

## Installation guide
Clone the Repository
  ```
  git clone https://github.com/aasri0905/csv-insights.git
  ```
Install required libraries
```
pip install -r requirements.txt
```
Add OpenAI key at `.env`
```
apikey=<api key>
```
Run the stream app
```
streamlit run interface.py
```
------------------------------------------
Functionality 
- The application provides many functionalities such as giving insights of mean median , mode of various columns
  ![](https://raw.githubusercontent.com/aasri0905/csv-insights/main/mean-median.png)
- Flexibility is given to the user , to select any column
  ![](https://github.com/aasri0905/csv-insights/blob/main/multiple-column.png?raw=true)
