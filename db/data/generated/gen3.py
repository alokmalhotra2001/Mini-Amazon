from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random


num_listings = 175
num_sellers = 60 #600
num_products = 100
listings = []

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_listings(num_listings):
    with open('ListingTest.csv', 'w') as f, open('InventoryTest.csv', 'w') as f1:
        writer = get_csv_writer(f)
        writer1 = get_csv_writer(f1)
        print('Listings...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 99 == 0:
                print(f'{pid}', end=' ', flush=True)
            listing_id = pid
            seller_id = fake.random_int(0,num_sellers-1)
            quantity = fake.random_int(max=1000)
            listing_name = fake.sentence(nb_words=1)
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            image = fake.image_url()
            description = fake.sentence(nb_words=25)
            writer.writerow([listing_id, seller_id, pid, listing_name, price, image, description])
            writer1.writerow([listing_id, seller_id, quantity])
            listings.append((listing_id, price, seller_id))
        for pid in range(int(num_products/2)):
            if pid % 49 == 0:
                print(f'{pid}', end=' ', flush=True)
            listing_id = pid+100
            seller_id = fake.random_int(0,num_sellers-1)
            quantity = fake.random_int(max=1000)
            listing_name = fake.sentence(nb_words=1)
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            image = fake.image_url()
            description = fake.sentence(nb_words=25)
            writer.writerow([listing_id, seller_id, pid, listing_name, price, image, description])
            writer1.writerow([listing_id, seller_id, quantity])
            listings.append((listing_id, price, seller_id))
        for pid in range(int(num_products/4)):
            if pid % 24 == 0:
                print(f'{pid}', end=' ', flush=True)
            listing_id = pid+150
            seller_id = fake.random_int(0,num_sellers-1)
            quantity = fake.random_int(max=1000)
            listing_name = fake.sentence(nb_words=1)
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            image = fake.image_url()
            description = fake.sentence(nb_words=25)
            writer.writerow([listing_id, seller_id, pid, listing_name, price, image, description])
            writer1.writerow([listing_id, seller_id, quantity])
            listings.append((listing_id, price, seller_id))
        print(f'{int(num_products+(num_products/2)+(num_products/4))} generated')


def gen_inventory(num_inventory_items):
    with open('InventoryTest.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventory...', end=' ', flush=True)
        for l_id in range(num_inventory_items):
            id = l_id
            quantity = fake.random_int(max=1000)
            seller_id = fake.random_int(max=num_sellers-1)
            writer.writerow([id, seller_id, quantity])
        print(f'{num_inventory_items} generated')

gen_listings(num_listings)
