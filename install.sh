<<<<<<< HEAD
#!/bin/bash

echo "You may need to tweak .flashenv and db/setup.sh manually"
sudo apt-get -qq coreutils
=======
# #!/bin/bash

# echo "You may need to tweak .flashenv and db/setup.sh manually"
# sudo apt-get -qq coreutils
# mypath=`realpath $0`
# mybase=`dirname $mypath`
# user=`whoami`
# echo "Assume your database user name is: $user"
# read -p "Enter database password and press [ENTER]: " dbpasswd

# secret=`tr -dc 'a-z0-9-_' < /dev/urandom | head -c50`
# cd $mybase
# cp -f flaskenv-template.env .flaskenv
# sed -i "s/default_secret/'$secret'/g" .flaskenv
# sed -i "s/default_db_user/$user/g" .flaskenv
# sed -i "s/default_db_password/$dbpasswd/g" .flaskenv

# sudo apt-get -qq update
# sudo apt-get -qq --yes install python3-virtualenv
# virtualenv env
# source env/bin/activate
# pip install -r requirements.txt
# db/setup.sh

#!/bin/bash

brew install coreutils
# brew install python3
pip3 install virtualenv
brew install gsed
# brew install postgresql

echo "You may need to tweak .flashenv and db/setup.sh manually"
# sudo apt-get -qq coreutils
>>>>>>> origin/zx_dev
mypath=`realpath $0`
mybase=`dirname $mypath`
user=`whoami`
echo "Assume your database user name is: $user"
read -p "Enter database password and press [ENTER]: " dbpasswd

<<<<<<< HEAD
secret=`tr -dc 'a-z0-9-_' < /dev/urandom | head -c50`
cd $mybase
cp -f flaskenv-template.env .flaskenv
sed -i "s/default_secret/'$secret'/g" .flaskenv
sed -i "s/default_db_user/$user/g" .flaskenv
sed -i "s/default_db_password/$dbpasswd/g" .flaskenv

sudo apt-get -qq update
sudo apt-get -qq --yes install python3-virtualenv
virtualenv env
source env/bin/activate
pip install -r requirements.txt
=======
secret=`LC_ALL=C tr -dc 'a-z0-9-_' < /dev/urandom | head -c50`
cd $mybase
cp -f flaskenv-template.env .flaskenv
gsed -i "s/default_secret/'$secret'/g" .flaskenv
gsed -i "s/default_db_user/$user/g" .flaskenv
gsed -i "s/default_db_password/$dbpasswd/g" .flaskenv

# sudo apt-get -qq update
# sudo apt-get -qq --yes install python3-virtualenv
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
chmod +x db/setup.sh
>>>>>>> origin/zx_dev
db/setup.sh
