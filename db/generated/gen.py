from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random
num_users = 10
cs_research_field =['Artificial Intelligence (AI)'
                    ,'Computer Architecture & Engineering (ARC)'
                    ,'Biosystems & Computational Biology (BIO)'
                    ,'Cyber-Physical Systems and Design Automation (CPSDA)'
                    ,'Database Management Systems (DBMS)'
                    ,'Education (EDUC)'
                    ,'Graphics (GR)'
                    ,'Human-Computer Interaction (HCI)'
                    ,'Operating Systems & Networking (OSNT)'
                    ,'Programming Systems (PS)'
                    ,'Scientific Computing (SCI)'
                    ,'Security (SEC)'
                    ,'Theory (THY)']

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

def gen_auth(num_users):
    with open('db/generated/Auth.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Auth...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{id}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            school = profile['company']
            writer.writerow([uid, email, password, firstname, lastname,school])
        print(f'{num_users} generated')
    return

def gen_user(num_users):
    with open('db/generated/Users.csv',"w") as f:
        writer = get_csv_writer(f)
        print('AUTH...', end=' ', flush=True)
        research_ind = list(fake.random_int(min=0,max=12) for i in range(num_users))
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            username = profile['username']
            citeNum = 0
            research_interest = cs_research_field[research_ind[uid]]
            writer.writerow([uid, username, citeNum, research_interest])
        print(f'{num_users} generated')
    return

gen_auth(num_users)
gen_user(num_users)
