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

collection_name = ["Aesthetics","ALC","Algorithm","Algorithm analysis","Algorithm complexity",
"Alphabet","Artificial intelligence (AI)","ASCII","Association Rule Learning","Asymptotic",
"Asymptotic complexity","Attack","Big O notation","Binary number system","Binary search","Bit",
"Bozo search","Brooks' law","Brute force attack","Bubble sort","Bug","Byte","Caesar cipher",
"Cartesian coordinate system","Central Processing Unit","Character","Chatterbot","Check digit",
"Check equation","Chomsky hierarchy","Cipher","Ciphertext","Client","Compiler","Complement","Complexity",
"Compression","Computer graphics","Computer program","Computer vision","Convention","Core","Correlation",
"Cost","Data point","Data processing","Decimal number system (Denary number system)","Decrypt",
"Dictionary attack","Digital signature","Edge detection","Encryption","Encryption key","Error correction",
"Error detection","Extrapolation","Feature","Feedback","Finite state automaton","Finite state machine",
"Formal language","Frequency analysis attack","GIF","Gigabyte","Grammar","Graphics transform",
"Greedy algorithm","Hash function","Heuristic","Hexadecimal","Hexadecimal colour codes","High level language",
"Human computer interaction (HCI)","Hypertext Transfer Protocol (HTTP)","Image noise","Image segmentation",
"Insertion sort","Intelligent systems","Interface","Interpolation","Interpreter","ISBN","JPEG",
"Key (in algorithms)","Key (in cryptography)","Kilobyte","Known plaintext attack","Language","Lexical analysis",
"Linear complexity","Linear search (sequential search)","Logarithm","Long tail marketing","Lossless","Lossy",
"Machine language","Megabyte","MP3","Nibble","Nielsonâ€™s heuristics","Octal","Packet","Parity","Parse tree",
"Parsing","Pattern matching","Permutation","Pivot","Pixel","Plaintext","PNG","Problem domain","Processor",
"Programming language","Protocol","Prototype","Public key cryptography","Quadratic complexity","Quicksort",
"Redundant bits","Regular expression","Rotation","Salt","Scale","Search","Selection sort","Server","Slope",
"Software","Sort","Stakeholder","String","Substitution cipher","Syntactically correct","Syntax","Syntax diagram",
"Task","Thresholding","Time complexity","Tractable","Transition","Translation","Unicode","Usability",
"Usability heuristic","User","User Experience (UX)","User story","Visual computing"]

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
            plain_password = f'pass{uid}'
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
def gen_user(num_users,num_cite):
    with open('db/generated/Users.csv',"w") as f:
        writer = get_csv_writer(f)
        print('AUTH...', end=' ', flush=True)
        research_ind = list(fake.random_int(min=0,max=12) for i in range(num_users))
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            username = profile['username']
            citeNum = num_cite[uid]
            research_interest = cs_research_field[research_ind[uid]]
            writer.writerow([uid, username, citeNum, research_interest])
        print(f'{num_users} generated')
    return

# generate fake dataset for users' browsing history
# table User_browse
def gen_user_browse(num_users, num_papers=629814):
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
                browsed_list = np.random.choice(num_papers, size=num_browsed[uid])
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

# generate fake dataset for users' Users_cite_history
# table User_cite_history
def gen_user_cite_history(num_users,num_papers=629814):
    num_order = list(fake.random_int(min=0, max=3) for i in range(num_users))
    num_cite = []
    with open('db/generated/User_cite_history.csv',"w") as f:
        writer = get_csv_writer(f)
        print('User_cite_history...', end=' ', flush=True)
        for uid in range(num_users):
            u_counter = 0 
            for order in range(num_order[uid]):
                cited_paper_list = np.random.choice(num_papers, size=fake.random_int(min=1,max=30))
                u_counter+=len(cited_paper_list)
                for cite_pid in cited_paper_list:
                    writer.writerow([uid,order+1,cite_pid])     
            num_cite.append(u_counter)
        print(f'{num_users} generated')
    return num_cite


# generate fake dataset for users' collection
# table Collections 
def gen_collections(num_users,num_papers=629814):
    user_has_collection= np.random.choice([True,False],num_users, p=[0.8,0.2])
    num_collection = list(fake.random_int(min=1,max=5) for i in range(num_users))
    with open('db/generated/Collections.csv',"w") as f:
        writer = get_csv_writer(f)
        print('Collections...', end=' ', flush=True)
        for uid in range(num_users):
            if user_has_collection[uid]:
                c_names = np.random.choice(collection_name,size=num_collection[uid])
                for c_name in c_names:
                    collected_pid = np.random.choice(num_papers,size = fake.random_int(min=1,max=15))
                    writer.writerow([uid,c_name,-1])
                    for c_pid in collected_pid:
                        writer.writerow([uid,c_name,c_pid]) 
                liked_pid = np.random.choice(num_papers,size = fake.random_int(min=0,max=10))
                if len(liked_pid)==0:
                    writer.writerow([uid, "Liked",-1])
                else:
                    writer.writerow([uid, "Liked",-1])
                    for pid in liked_pid:
                        writer.writerow([uid,"Liked",pid])
            else:
                writer.writerow([uid, "Liked",-1])
        print(f'{num_users} generated')
    return 


gen_auth(num_users)
user_browse_history, user_browse, num_browsed  =  gen_user_browse(num_users)
gen_user_cart(num_users,user_browse_history, user_browse, num_browsed)
num_cite = gen_user_cite_history(num_users)
gen_user(num_users,num_cite)
gen_user(num_users,10)
gen_collections(num_users)