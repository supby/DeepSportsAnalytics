sudo apt-get install libblas3gf
sudo apt-get install libblas-dev
sudo apt-get install liblapack3gf
sudo apt-get install liblapack-dev
sudo apt-get install zlib1g-dev

git clone https://github.com/supby/NHLPredictor.git
cd NHLPredictor
virtualenv .
source bin/activate
pip instal -r requirements.txt