if [ $? -eq 0 ]; then
  :
else
  echo "ERROR Can't find pip. Please install"
  exit 1
fi
pip install virtualenv
python -m virtualenv --python=python3.10 venv
if [ -d "venv/bin" ]; then
  source venv/bin/activate
elif [ -d "venv/Scripts" ]; then
  source venv/Scripts/activate
else
  echo "ERROR no virtualenv script folder found"
  exit 1
fi
pip install -r requirements.txt