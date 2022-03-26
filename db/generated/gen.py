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

# generate fake dataset for users' browsing history
# table User_browse
def gen_user_browse(num_users, num_papaers=629814):
    user_browse_history =dict()
    user_browse = np.random.choice([True,False],num_users, p=[0.95,0.05])
    num_browsed = list(fake.random_int(min=10,max=40) for i in range(num_users))
    with open('db/generated/User_browse.csv',"w") as f:
        writer = get_csv_writer(f)
        print('User_browse...', end=' ', flush=True)
        for uid in range(num_users):
            one_browse_history=dict()
            if user_browse[uid]:
                #min pid 0, max pid 629813
                browsed_list = np.random.choice(num_papaers, size=num_browsed[uid])
                for browsed_pid in browsed_list:
                    time_browsed= fake.date_time()
                    writer.writerow([uid,browsed_pid,time_browsed])
                    one_browse_history.update({browsed_pid:time_browsed})
            user_browse_history.update({uid:one_browse_history})
        print(f'{num_users} generated')
    return user_browse_history, user_browse, num_browsed

# generate fake dataset for users' citation cart
# table User_cart
def gen_user_cart(num_users, browse_history, user_browse, num_browsed):
    user_has_cart = np.random.choice([True,False],num_users, p=[0.7,0.3])
    num_citation = list(fake.random_int(min=1,max=num_browsed[i]) for i in range(num_users))
    with open('db/generated/User_cart.csv',"w") as f:
        writer = get_csv_writer(f)
        print('User_cart...', end=' ', flush=True)
        for uid in range(num_users):
            if user_has_cart[uid] and user_browse[uid]:
                #min pid 0, max pid 629813
                citation_list = np.random.choice(list(browse_history[uid].keys()), size=num_citation[uid])
                for cite_pid in citation_list:
                    time_cited = fake.date_time_between(start_date=browse_history[uid][cite_pid])
                    writer.writerow([uid,cite_pid,time_cited])     
        print(f'{num_users} generated')
    return 


# generate fake dataset for users' collection
# table Collections 

#gen_auth(num_users)
#gen_user(num_users)
user_browse_history, user_browse, num_browsed  =  gen_user_browse(num_users)
gen_user_cart(num_users,user_browse_history, user_browse, num_browsed)