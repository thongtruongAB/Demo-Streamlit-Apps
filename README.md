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
[![Screenshot-2022-12-18-212410.png](https://i.postimg.cc/d0nc9jHX/Screenshot-2022-12-18-212410.png)](https://postimg.cc/1ggdmwZc)