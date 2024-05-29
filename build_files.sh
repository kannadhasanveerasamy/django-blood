echo "BUILD START"

# create a virtual environment named 'venv' if it doesn't already exist
python -m venv venv

# activate the virtual environment
source venv/bin/activate

python -m pip install -r requirements.txt
# install all deps in the venv
pip install -r requirements.txt
python manage.py collectstatic
# collect static files using the Python interpreter from venv
python manage.py collectstatic --noinput

echo "BUILD END"
# [optional] Start the application here 
# python manage.py runserver