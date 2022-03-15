from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 10
# num_products = 2000
# num_purchases = 2500
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
    with open('AUTH.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('AUTH...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            school = profile['company']
            writer.writerow([uid, email, password, firstname, lastname,school])
        print(f'{num_users} generated')
    return

def gen_user(num_users):
    with open('USER.csv',"w") as f:
        writer = get_csv_writer(f)
        print('AUTH...', end=' ', flush=True)
        research_ind = list(fake.random_int() for i in range(num_users))
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

'''
def gen_products(num_products):
    available_pids = []
    with open('Products2.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(pid)
            writer.writerow([pid, name, price, available])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


def gen_purchases(num_purchases, available_pids):
    with open('Purchases2.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            time_purchased = fake.date_time()
            writer.writerow([id, uid, pid, time_purchased])
        print(f'{num_purchases} generated')
    return

'''

gen_auth(num_users)
gen_user(num_users)
# available_pids = gen_products(num_products)
# gen_purchases(num_purchases, available_pids)
