# gujarati_audio_book
This is a prototype project created by two students Aayush Thacker and Sultan Khatri to give locals a website where they can read as well as hear audio books which are created by an A.I.
We used a Python library called flask to build the website and gtts to build the api that translates text to Aujarati audio and a tesseract modual that can read text from any image file.
<br>
# HOW TO RUN?
Open the cmd and go to ./gujarati_audio_book directery, run the following command to set the variable *FLASK_APP* <br>
`set FLASK_APP=application.py`
<br>
then create a python virtual environment using this command:<br>
`py -m venv env`
<br>
finally use the following command to start the flask server on default localhost(127.0.0.1:5000) <br>
`flask run`
<br>
# Features:
Seeing all the books on the home page:<br>
![image](https://user-images.githubusercontent.com/59171847/180642379-c293f7be-1c77-4aeb-be04-bea4e1261e19.png)
<br>
Click on "Vadhu Jano" to see in detail about a book, also download pdf or mp3 files of that book:<br>
![image](https://user-images.githubusercontent.com/59171847/180642436-fc1bfb64-d3f4-44e1-a23d-f8d06b1226a7.png)
<br>
Go to the other two options on the navigation bar to convert text/imagetext into audio files using GTTS:<br>
![image](https://user-images.githubusercontent.com/59171847/180642577-6f3c812c-0b6f-4e8c-9d40-bafa3afd4147.png)
<br>
Go to the */secret* to upload new books:<br>
![image](https://user-images.githubusercontent.com/59171847/180642633-f8f8e13c-a6b2-4889-bff0-fe32ee8cecd9.png)
