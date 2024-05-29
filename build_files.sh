echo "BUILD START"
python3 -m pip install -r requirements.txt
# install all deps in the venv
pip install -r requirements.txt
python3 manage.py collectstatic
# collect static files using the Python interpreter from venv
python3 manage.py collectstatic --noinput

echo "BUILD END"
# [optional] Start the application here 
python manage.py runserver