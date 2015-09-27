sudo apt-get install libblas3gf
sudo apt-get install libblas-dev
sudo apt-get install liblapack3gf
sudo apt-get install liblapack-dev
sudo apt-get install zlib1g-dev

git clone https://github.com/supby/DeepSportsAnalytics.git
cd DeepSportsAnalytics
virtualenv .
source bin/activate
pip install -r requirements.txt