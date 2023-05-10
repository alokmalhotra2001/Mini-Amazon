from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random

num_users = 100 #1000
num_sellers = 60 #600
num_products = 100 #2000
num_listings = 175
num_purchases = 100 #2500
num_tags = 100
num_tagged = 145 #300
num_cart_items = 500
num_inventory_items = 175 #500
num_orders = 400
num_cards = 20

valid_tags = []
listings = []
orders = []
purchased_from = {}
product_reviews = []
seller_reviews = []
order_contents = []

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

def get_csv_reader(f):
    return csv.reader(f, dialect='unix')

def gen_users(num_users):
    with open('UsersTest.csv', 'w') as f, open('UsersPasswords.csv', 'w') as f1:
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
            purchased_from[uid] = set()
        print(f'{num_users} generated')
        print(purchased_from)
    return

def gen_sellers(num_sellers):
    with open('SellersTest.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        for id in range(num_sellers):
            sid = id
            writer.writerow([sid])
        print(f'{num_sellers} generated')

def gen_products(num_products):
    with open('ProductTest.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 99 == 0:
                print(f'{pid}', end=' ', flush=True)
            first_seller_id = fake.random_int(0,num_sellers-1)
            p_name = fake.sentence(nb_words=1)
            writer.writerow([pid, p_name, first_seller_id])
        print(f'{int(num_products)} generated')
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
    
def gen_tags(num_tags):
    with open('TagsTest.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Tags...', end=' ', flush=True)
        for _ in range(num_tags):
            tag = fake.sentence(nb_words=1)
            if tag not in valid_tags:
                writer.writerow([tag])
                valid_tags.append(tag)
        print(f'{num_tags} generated')

def gen_gifts(num_cards):
    with open('GiftsTest.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Gifts...', end=' ', flush=True)
        code = 2000000001
        for i in range(num_cards):
            amount = f'{str(fake.random_int(max=100))}.{fake.random_int(max=99):02}'
            used = fake.random_int(max = 1)
            writer.writerow([code, amount, used])
            code = fake.random_int(min = 1000000000, max = 2000000000)
        print(f'{num_cards} generated')


def gen_listing_tags(num_tagged):
    with open('ListingsHaveTagsTest.csv', 'w') as f, open('TempListingsHaveTagsTest.csv', 'w+') as t:
        fwriter = get_csv_writer(f) 
        twriter = get_csv_writer(t) 
        i = 0
        print('ListingsHaveTags...', end=' ', flush=True)
        for x in range(num_tagged):
            l_id = fake.random_int(max=num_listings-1)
            tag = fake.random_element(elements=valid_tags)
            twriter.writerow([l_id, tag])
        t.seek(0)
        treader = get_csv_reader(t) 
        seen = set() # set for fast O(1) amortized lookup
        for row in treader:
            if tuple(row) in seen: 
                i = i+1
                continue # skip duplicate
            seen.add(tuple(row))
            fwriter.writerow(row)
        num_tagged = num_tagged - i
        print(f'{num_tagged - i} generated')

# def gen_cart_items(num_cart_items):
#     with open('VersionInCartTest.csv', 'w') as f:
#         writer = get_csv_writer(f)
#         print('VersionInCart...', end=' ', flush=True)
#         for rows in range(num_cart_items):
#             l_id = fake.random_int(max=num_products-1)
#             quantity = fake.random_int(max=1000)
#             status = fake.random_int(max=1)
#             user_id = fake.random_int(max=num_users)
#             writer.writerow([l_id, quantity, status, user_id])
#         print(f'{num_cart_items} generated')


def gen_orders(num_orders):
    with open('OrdersTest.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)
        for o_id in range(num_orders):
            buyer_id = fake.random_int(max=num_users-1)
            placed = fake.date_time()
            fulfilled = fake.random_int(max=1)
            num_items = fake.random_int(max=50)
            writer.writerow([o_id, buyer_id, placed, fulfilled, num_items])
            orders.append((o_id, buyer_id, placed, fulfilled, num_items))
        print(f'{num_orders} generated')
   

def gen_order_contents():
    with open('OrderContentsTest.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('OrderContents...', end=' ', flush=True)
        for order in orders:
            o_id = order[0]
            buyer_id = order[1]
            placed = order[2]
            fulfilled = order[3]
            num_items = order[4]
            available_listings = [x for x in listings]
            for x in range(num_items):
                listing = random.choice(available_listings)
                available_listings.remove(listing)
                l_id = listing[0]
                price = listing[1]
                listing_seller = listing[2]
                #price needs to match a price of product with corresponding l_id
                
                quantity = fake.random_int(max=1000)
                item_fulfilled = fake.random_int(max=1)
                datetime_fulfilled = fake.date_time()

                writer.writerow([o_id, buyer_id, l_id, price, quantity, item_fulfilled, datetime_fulfilled])
                #print(type(purchased_from[buyer_id]))
                order_contents.append((o_id, l_id, buyer_id, listing_seller))
                purchased_from[buyer_id].add(listing_seller)
        print('generated')
        #print(f'{num_order_contents} generated')

def gen_seller_reviews():
    with open('SellerReviewsTestNew.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Seller Reviews...', end=' ', flush=True)
        for user in range(num_users):
            for seller in purchased_from[user]:
                reviewer = user
                rating = fake.random_int(min=0,max=5)
                #rating = fake.pyfloat(left_digits=1,right_digits=1,positive=True,min_value=1.0,max_value=5.0)
                review = fake.text(max_nb_chars=255)
                dateAndTime = fake.date_time()
                helpful = fake.random_int(min=-100,max=100)
                writer.writerow([reviewer, seller, rating, review, dateAndTime, helpful])
                seller_reviews.append((reviewer, seller))
        print('generated')
        #print(f'{min(num_users, num_sellers)} generated')

def gen_product_reviews():
    with open('ProductReviewsTestNew.csv', 'w') as f:
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
                product_reviews.append((reviewer, product))
        print(f'{num_users*num_products} generated')

def gen_product_reviews_images():
    with open('ProductReviewsImages.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product Reviews Images...', end=' ', flush=True)
        for x in product_reviews:
            reviewer = x[0]
            reviewee = x[1]
            for y in range(fake.random_int(min=0, max=4)):
                image = fake.image_url()
                writer.writerow([reviewer, reviewee, image])
        print('generated')
                
def gen_product_reactions():
    with open('ProductRatingReactions.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product Rating Interactions...', end=' ', flush=True)
        for review in product_reviews:
            reviewer = review[0]
            reviewee = review[1]
            available_users = [x for x in range(num_users)]
            for _ in range(fake.random_int(max=100)):
                action = random.choice([1, -1])
                when = fake.date_time()
                liker = random.choice(available_users)
                available_users.remove(liker)
                writer.writerow([reviewer, reviewee, liker, action, when])
        print('generated')

def gen_seller_reactions():
    with open('SellerRatingReactions.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Seller Rating Interactions...', end=' ', flush=True)
        for review in seller_reviews:
            reviewer = review[0]
            reviewee = review[1]
            for _ in range(fake.random_int(max=100)):
                action = random.choice([1, -1])
                when = fake.date_time()
                writer.writerow([reviewer, reviewee, action, when])
        print('generated')

def gen_messages():
    with open('Messages.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Messages...', end=' ', flush=True)
        for x in order_contents:
            o_id = x[0]
            l_id = x[1]
            buyer = x[2]
            seller = x[3]
            for _ in range(fake.random_int(min=0, max=30)):
                message = fake.text(max_nb_chars=500)
                dateAndTime = fake.date_time()
                author = random.choice([buyer, seller])
                writer.writerow([o_id, author, l_id, message, dateAndTime])
        print('generated')

def gen_order_contents2(num_order_contents):
    with open('OrderContentsTest1.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('OrderContents...', end=' ', flush=True)
        for o_id in range(num_order_contents):
            buyer_id = fake.random_int(max=num_users)
            u_id = fake.random_int(max=num_users-1)
            l_id = fake.random_int(max=num_products-1)
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            #price needs to match a price of product with corresponding l_id
            quantity = fake.random_int(max=1000)
            item_fulfilled = fake.random_int(max=1)
            datetime_fulfilled = fake.date_time()
            writer.writerow([buyer_id, u_id, l_id, price, quantity, item_fulfilled, datetime_fulfilled])
        print(f'{num_order_contents} generated')
    return

def gen_purchases(num_purchases, available_pids):
    with open('Purchases.csv', 'w') as f:
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

gen_users(num_users)
gen_products(num_products)
gen_listings(num_listings)
# gen_sellers(num_sellers)
gen_tags(num_tags)
gen_listing_tags(num_tagged)
# gen_cart_items(num_cart_items)
gen_orders(num_orders)
gen_order_contents()
# print(purchased_from)
gen_product_reviews()
gen_seller_reviews()
gen_product_reactions()
gen_seller_reactions()
gen_product_reviews_images()
gen_messages()
gen_gifts(num_cards)
#gen_purchases(num_purchases, available_pids)
