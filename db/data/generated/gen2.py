from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 100 #1000
num_sellers = 60 #600
num_products = 100 #2000
num_purchases = 100 #2500
num_tags = 100
num_tagged = 30 #300
num_cart_items = 500
num_inventory_items = 500
num_orders = 400

valid_tags = []

Faker.seed(0)
fake = Faker()

def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

def gen_users(num_users):
    with open('UsersTest2.csv', 'w') as f, open('UsersPasswords.csv', 'w') as f1:
        writer = get_csv_writer(f)
        writer1 = get_csv_writer(f1)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            #print(plain_password+'\n')
            password = generate_password_hash(plain_password)
            address = fake.address()
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            balance = f'{str(fake.random_int(max=1000))}.{fake.random_int(max=99):02}'
            writer.writerow([uid, email, password, address, firstname, lastname, balance])
            writer1.writerow([email, plain_password])
        print(f'{num_users} generated')
    return

def gen_sellers(num_sellers):
    with open('SellersTest2.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        for id in range(num_sellers):
            sid = id
            writer.writerow([sid])

def gen_products(num_products):
    with open('ListingTest2.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Listings...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            listing_id = pid
            seller_id = fake.random_int(0,num_sellers-1)
            name = fake.sentence(nb_words=1)
            listing_name = fake.sentence(nb_words=1)
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            image = fake.image_url()
            description = fake.sentence(nb_words=25)
            writer.writerow([listing_id, seller_id, pid, name, listing_name, price, image, description])
        print(f'{num_products} generated')

def gen_product_reviews2():
    with open('ProductReviewsTest2.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product Reviews...', end=' ', flush=True)
        for x in range(min(num_users, num_products)):
            reviewer = x
            product = x
            rating = fake.pyfloat(left_digits=1,right_digits=1,positive=True,min_value=1.0,max_value=5.0)
            review = fake.text(max_nb_chars=255)
            dateAndTime = fake.date_time()
            helpful = fake.random_int(min=-100,max=100)
            writer.writerow([reviewer, product, rating, review, dateAndTime, helpful])
        print(f'{min(num_users, num_products)} generated')

def gen_product_reviews():
    with open('ProductReviewsTest.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product Reviews...', end=' ', flush=True)
        for x in range(min(num_users, num_products)):
            for y in range(max(num_users, num_products)):
                if min(num_users, num_products) == num_users:
                    reviewer = x
                    product = y
                else:   
                    reviewer = y
                    product = x
                rating = fake.random_int(min=0,max=5)
                #rating = fake.pyfloat(left_digits=1,right_digits=1,positive=True,min_value=1.0,max_value=5.0)
                review = fake.text(max_nb_chars=255)
                dateAndTime = fake.date_time()
                helpful = fake.random_int(min=-100,max=100)
                writer.writerow([reviewer, product, rating, review, dateAndTime, helpful])
        print(f'{num_users*num_products} generated')

def gen_seller_reviews():
    with open('SellerReviewsTest.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Seller Reviews...', end=' ', flush=True)
        for x in range(min(num_users, num_sellers)):
            reviewer = x
            seller = x
            rating = fake.random_int(min=0,max=5)
            #rating = fake.pyfloat(left_digits=1,right_digits=1,positive=True,min_value=1.0,max_value=5.0)
            review = fake.text(max_nb_chars=255)
            dateAndTime = fake.date_time()
            helpful = fake.random_int(min=-100,max=100)
            writer.writerow([reviewer, seller, rating, review, dateAndTime, helpful])
        print(f'{min(num_users, num_sellers)} generated')

gen_users(num_users)
gen_products(num_products)
gen_sellers(num_sellers)
gen_product_reviews()
gen_seller_reviews()
#gen_purchases(num_purchases, available_pids)
