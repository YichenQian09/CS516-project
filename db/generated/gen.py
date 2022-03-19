from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random
import numpy as np 

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

# generate fake dataset for authentification 
# table Auth
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

# generate fake dataset for user, each matched with previous AUTH dataset
# table Users
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

# generate fake dataset for users' citation cart
# table User_cart

# def gen_user_cart(num_users, num_papaers):
#     user_has_cart = np.random_choice([True,False],num_users, p=[0.7,0.3])
#     with open('db/generated/User_cart.csv',"w") as f:
#         writer = get_csv_writer(f)
#         print('User_cart...', end=' ', flush=True)
#         for uid in range(num_users):



# generate fake dataset for users' browsing history
# table User_browse

# generate fake dataset for users' collection
# table Collections 


def gen_purchases(num_purchases,):

            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            time_purchased = fake.date_time()
            writer.writerow([id, uid, pid, time_purchased])

gen_auth(num_users)
gen_user(num_users)
