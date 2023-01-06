To running this Rasa Demo, you need:
Install requiments (recommend using python 3.8):
* > conda create -n env python=3.8
* > python -m pip install git+https://github.com/RasaHQ/rasalit (Install Rasa and Streamlit)
* > pip install -r requirements.txt

----------------------
Train model:
* > rasa train

Prepare 2 command line:
* commandline 1: rasa run --enable-api
* commandline 2: streamlit run rasa_streamlit.py
* If run streamlit error **"cannot import name 'builder' from 'google.protobuf.internal'"** you must :
  * > pip uninstall protobuf
  * > pip install protobuf==4.21
* Run again.
----------------------------
# Demo_Streamlit_Apps
This repository is using for demo Streamlit Web Apps.

# To use this demo:
***Demo Files:***
* ***Command to run streamlit app.***
>rasa train
>rasa --enable-api
>cd streamlit
>streamlit run file_name.py
--------------------------
1. **crypto_price_streamlit.py**
[![Demo-Crypto.png](https://i.postimg.cc/MKnwcdY9/Demo-Crypto.png)](https://postimg.cc/BXfkk5kF)
--------------------------
2. **penguins-app.py**
[![Demo-Penguin-Classifier.png](https://i.postimg.cc/pr9Sd1t8/Demo-Penguin-Classifier.png)](https://postimg.cc/Pvjy3yJr)
--------------------------
3. **Rasa-chatbot**
[![Screenshot-2022-12-18-212410.png](https://i.postimg.cc/d0nc9jHX/Screenshot-2022-12-18-212410.png)](https://postimg.cc/1ggdmwZc)
