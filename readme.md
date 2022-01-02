# HitchcockProblemVisualizationApp
This app visualizes Hitchcock problem results. It downloads and processes data from OSM and visualizes optimal routes calculated by algorithm implemented by https://github.com/Grzybiarz47. The app is deployed on heroku: https://wizualizacja-tras.herokuapp.com/visualization/. To use it type a name of a city (preferrably small - to about 500 crossings) and click the button to see tables with randomized data and results on map.

To run app locally:

Install osmnx:  
conda config --prepend channels conda-forge  
conda create -n ox --strict-channel-priority osmnx  

Activate virtual environment:  
conda activate ox  

Install packages:  
pip install -r requirements.txt  

Change DEBUG = False to True in App/settings.py  

Run:  
python manage.py runserver  
