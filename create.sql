CREATE TABLE Users 
(
    id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    address VARCHAR (255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    balance FLOAT NOT NULL CHECK (balance>=0)
);

CREATE TABLE Sellers
(
    id INT REFERENCES Users(id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL PRIMARY KEY
);

CREATE TABLE Product
(
 p_id INT GENERATED BY DEFAULT AS IDENTITY NOT NULL PRIMARY KEY,
 p_name VARCHAR(32) NOT NULL,
 first_seller_id INT REFERENCES Sellers(id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL
);

CREATE TABLE Listing
(
 l_id INTEGER GENERATED BY DEFAULT AS IDENTITY NOT NULL PRIMARY KEY,
 seller_id INT REFERENCES Sellers(id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
 product_id INT REFERENCES Product(p_id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
 listing_name VARCHAR(32) NOT NULL,
 price FLOAT NOT NULL,
 image VARCHAR(512),
 description VARCHAR(512) NOT NULL
);

CREATE TABLE Gift 
(
    code INTEGER NOT NULL PRIMARY KEY,
    amount FLOAT NOT NULL,
    used INT DEFAULT 0
);

CREATE TABLE Tags
(
 name VARCHAR(32) NOT NULL PRIMARY KEY
);

CREATE TABLE ListingsHaveTags
(
 l_id INTEGER NOT NULL REFERENCES Listing(l_id) ON DELETE CASCADE ON UPDATE CASCADE,
 tag_name VARCHAR(32) NOT NULL REFERENCES Tags(name) ON DELETE CASCADE ON UPDATE CASCADE,
 PRIMARY KEY(l_id, tag_name)
);

CREATE TABLE VersionInCart
(
 l_id INTEGER NOT NULL REFERENCES Listing(l_id) ON DELETE CASCADE ON UPDATE CASCADE,
 quantity INTEGER NOT NULL,
 status BIT NOT NULL,
 user_id INTEGER NOT NULL REFERENCES Users(id) ON DELETE CASCADE ON UPDATE CASCADE,
 PRIMARY KEY(l_id, user_id)
);

CREATE TABLE Inventory (
    id INT NOT NULL REFERENCES Listing(l_id) ON DELETE CASCADE ON UPDATE CASCADE PRIMARY KEY,
    seller_id INT REFERENCES Sellers(id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    quantity INT NOT NULL
);

CREATE TABLE Cart (
    u_id INT REFERENCES Users(id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL PRIMARY KEY
);

CREATE TABLE Orders (
    id INT GENERATED BY DEFAULT AS IDENTITY NOT NULL PRIMARY KEY,
    buyer_id INT REFERENCES Users(id) ON DELETE SET NULL ON UPDATE CASCADE,
    placed timestamp with time zone NOT NULL,
    fulfilled BIT NOT NULL,
    num_items INT NOT NULL
);

CREATE TABLE OrderContents (
    o_id INT REFERENCES Orders(id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    u_id INT REFERENCES Users(id) ON DELETE SET NULL ON UPDATE CASCADE,
    l_id INT REFERENCES Listing(l_id) ON DELETE SET NULL ON UPDATE CASCADE,
    price FLOAT NOT NULL,
    quantity INT NOT NULL,
    item_fulfilled BIT NOT NULL, 
    datetime_fulfilled timestamp NOT NULL,
    UNIQUE(o_id, l_id)
);

CREATE TABLE productRatings (
    reviewer INT REFERENCES Users(id) ON DELETE SET NULL ON UPDATE CASCADE,
    reviewee INT REFERENCES Product(p_id) ON DELETE SET NULL ON UPDATE CASCADE,
    rating INT NOT NULL CHECK(rating >= 0 and rating <= 5),
    review VARCHAR(255) NOT NULL,
    dateAndTime timestamp NOT NULL,
    helpful INT DEFAULT 0,
    UNIQUE(reviewer, reviewee)
);

CREATE TABLE productRatingImages (
    reviewer INT NOT NULL,
    reviewee INT NOT NULL,
    image VARCHAR(512) NOT NULL,
    FOREIGN KEY(reviewer, reviewee) REFERENCES productRatings(reviewer, reviewee) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE sellerRatings (
    reviewer INT REFERENCES Users(id) ON DELETE SET NULL ON UPDATE CASCADE,
    reviewee INT REFERENCES Sellers(id) ON DELETE SET NULL ON UPDATE CASCADE,
    rating INT NOT NULL CHECK(rating >= 0 and rating <= 5),
    review VARCHAR(255) NOT NULL,
    dateAndTime timestamp NOT NULL,
    helpful INT DEFAULT 0,
    UNIQUE(reviewer, reviewee)
);

CREATE FUNCTION checkReviewer() RETURNS trigger as $checkReviewer$
    BEGIN
        IF NEW.reviewer NOT IN(SELECT u_id FROM OrderContents as o, Listing as l WHERE o.l_id = l.l_id
        and l.seller_id = NEW.reviewee) THEN 
            RAISE EXCEPTION 'Reviewer has not purchased from seller';
        END IF;
        RETURN NEW;
    END;
$checkReviewer$ LANGUAGE plpgsql;

CREATE TRIGGER addSellerRatings
    BEFORE INSERT OR UPDATE ON sellerRatings
    FOR EACH ROW EXECUTE FUNCTION checkReviewer();

CREATE TABLE productRatingsReactions(
    reviewer INT NOT NULL,
    reviewee INT NOT NULL,
    liker INT REFERENCES Users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    action INT NOT NULL CHECK(action = 1 or action = -1),
    dateAndTime timestamp NOT NULL,
    FOREIGN KEY(reviewer, reviewee) REFERENCES productRatings(reviewer, reviewee) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE(reviewer, reviewee, liker)
);

--CREATE TABLE sellerRatingsReactions(
    --reviewer INT NOT NULL,
    --reviewee INT NOT NULL,
    --action INT NOT NULL CHECK(action = 1 or action = -1),
    --dateAndTime timestamp NOT NULL,
    --FOREIGN KEY(reviewer, reviewee) REFERENCES productRatings(reviewer, reviewee) ON DELETE CASCADE ON UPDATE CASCADE
--);

CREATE TABLE messages (
    assoc_order INT NOT NULL,
    author INT NOT NULL,
    assoc_listing INT NOT NULL,
    message VARCHAR(500) NOT NULL,
    dateAndTime timestamp NOT NULL,
    FOREIGN KEY(assoc_order, assoc_listing) REFERENCES OrderContents(o_id, l_id) ON DELETE CASCADE ON UPDATE CASCADE
);
