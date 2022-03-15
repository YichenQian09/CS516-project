from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random
num_auth = 100

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_auth(num_auth):
    with open('db/generated/Auth.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Auth...', end=' ', flush=True)
        for id in range(num_auth):
            if id % 10 == 0:
                print(f'{id}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{id}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            school=random.choice(['Harvard', 'Duke', 'Stanford', 'MIT', 'Princeton'])
            writer.writerow([id, email, password, firstname, lastname, school])
        print(f'{num_auth} generated')
    return


gen_auth(num_auth)
