sudo apt-get install libblas3gf
sudo apt-get install libblas-dev
sudo apt-get install liblapack3gf
sudo apt-get install liblapack-dev
sudo apt-get install zlib1g-dev
sudo apt-get install libxml2-dev
sudo apt-get install libxslt1-dev
sudo apt-get install python-dev
sudo apt-get install gfortran
sudo apt-get install python-virtualenv
sudo apt-get install cython

git clone https://github.com/supby/DeepSportsAnalytics.git
cd DeepSportsAnalytics
virtualenv .
source bin/activate
pip install -r requirements.txt
