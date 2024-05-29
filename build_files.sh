echo "BUILD START"

# create a virtual environment named 'venv' if it doesn't already exist
python3 -m venv venv

# activate the virtual environment
source venv/bin/activate

python3 -m pip install -r requirements.txt
# install all deps in the venv
pip install -r requirements.txt
python3 manage.py collectstatic
# collect static files using the Python interpreter from venv
python3 manage.py collectstatic --noinput

echo "BUILD END"
# [optional] Start the application here 
# python manage.py runserver