# BesApp 💻 

In this repository is present the code used to create a [website](https://share.streamlit.io/albertodebenedittis/besapp/main/dash.py) for presenting the BES indicators in Italy. 
This website allows the user to play with the different indicators across the years. 
The analysis is conducted having three reference points:
* Macro areas (North, Centre, and South)
* Regions 
* Provinces

## Code 🐍
The code is fully written in Python. 
To create the app has been used the streamlit package.

## Repository structure 📂

In dash.py there is the code used to create the website through the streamlit package.
Functions2.py contains the code used to: 
* clean the data
* make the analysis
* create the graphs and maps

In the folders are stored the: 
* geodataframe  (Dati_Nuovi2, Dati_Streamlite, No_Profit, Factories) 
* the map created and stored as .html file (used to show the maps in the dashboard without the need to create them) (Mappe_html)
* other files such us images used to add some details to the maps (Medaglie)
* the pickle file created to store some python dictionaries used in the model for detecting the best territories (Dictionaries)
