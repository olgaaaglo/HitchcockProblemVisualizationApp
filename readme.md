Install osmnx: 
conda config --prepend channels conda-forge
conda create -n ox --strict-channel-priority osmnx

Activate virtual environment:
conda activate ox

Install packages:
pip install -r requirements.txt

Run:
python manage.py runserver
