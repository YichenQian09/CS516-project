## Team members:
- Xinyu (Diane) Hu - xh112
- Yichen Qian - yq82
- Zhensheng Xie - zx93
- Angikar Ghosal - ag520


## Project chosen:  semi-standard project
Our team chooses to do a “semi-standard” course project: a researcher club application based on databases containing published scholarly papers (paper title, author, abstract, affiliation, year, etc). On our application, users can “shop” papers they are interested in. The goal of our application is to help researchers efficiently access useful papers.


## Team name: Crouching Tiger Hidden Dragons


Github repository: https://github.com/halfmoontonight/CS516-project


## To run the project:
0. download "citation-network1.zip" from https://lfs.aminer.cn/lab-datasets/citation/citation-network1.zip and put the "citation-network1.zip" under \db\data directory. Unzip the zip file, you will get a "outputacm.txt" file. Make sure you have "outputacm.txt" and "reformat_data.py" under \db\data directory; then execute command `$python reformat_data.py` in your terminal; you will get four .csv file: abstract.csv, authorship.csv, citation.csv, papers.csv 

1. If you are using MacOS, switch your shell to bash ($chsh -s /bin/bash)

2. Make sure you have installed python3, pip3, psql

3. psql user role and password setting
```
# set a database role of <<username>
# make the username as same as your account on your host machine
$ sudo -u postgres createuser <<username>>

# give the user a super permission
$ sudo -u postgres psql -c "ALTER ROLE <<username>> WITH SUPERUSER;"

# make sure the username is bind with password
$ sudo -u postgres psql -c "ALTER ROLE <<username>> WITH PASSWORD '<<password>>';"
```

4. Run install.sh
If you are using windows, install WSL and execute `$./install.sh`

If you are using MacOs, tweak your install.sh as follows and then execute `$./install.sh`
```
#!/bin/bash
 
brew install coreutils
# brew install python3
pip3 install virtualenv
brew install gsed
# brew install postgresql
 
echo "You may need to tweak .flashenv and db/setup.sh manually"
# sudo apt-get -qq coreutils
mypath=`realpath $0`
mybase=`dirname $mypath`
user=`whoami`
echo "Assume your database user name is: $user"
read -p "Enter database password and press [ENTER]: " dbpasswd
 
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
db/setup.sh
```
5. Activate and enter virtual env
```
$ source env/bin/activate
```

6. Run flask app
```
$ flask run
```
