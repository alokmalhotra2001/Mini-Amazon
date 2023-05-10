\COPY Users FROM 'data/generated/UsersTest.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);
\COPY Sellers FROM 'data/generated/SellersTest.csv' WITH DELIMITER ',' NULL '' CSV
--\COPY Products FROM 'data/Products.csv' WITH DELIMITER ',' NULL '' CSV
--\COPY Purchases FROM 'data/Purchases.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Product FROM 'data/generated/ProductTest.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.product_p_id_seq',
                          (SELECT MAX(p_id)+1 FROM Product),
                          false);
\COPY Listing FROM 'data/generated/ListingTest.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.listing_l_id_seq',
                          (SELECT MAX(l_id)+1 FROM Listing),
                          false);
\COPY Tags FROM 'data/generated/TagsTest.csv' WITH DELIMITER ',' NULL '' CSV
\COPY ListingsHaveTags FROM 'data/generated/ListingsHaveTagsTest.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Inventory FROM 'data/generated/InventoryTest.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Orders FROM 'data/generated/OrdersTest.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.orders_id_seq',
                         (SELECT MAX(id)+1 FROM Orders),
                         false);
\COPY OrderContents FROM 'data/generated/OrderContentsTest.csv' WITH DELIMITER ',' NULL '' CSV
--SELECT pg_catalog.setval('public.orders_id_seq',
                         --(SELECT MAX(id)+1 FROM Users),
                         --false);
--\COPY OrderContents FROM 'data/OrdersTest.csv' WITH DELIMITER ',' NULL '' CSV
\COPY productRatings FROM 'data/generated/ProductReviewsTestNew.csv' WITH DELIMITER ',' NULL '' CSV
\COPY sellerRatings FROM 'data/generated/SellerReviewsTestNew.csv' WITH DELIMITER ',' NULL '' CSV

\COPY productRatingImages FROM 'data/generated/ProductReviewsImages.csv' WITH DELIMITER ',' NULL '' CSV
\COPY productRatingsReactions FROM 'data/generated/ProductRatingReactions.csv' WITH DELIMITER ',' NULL '' CSV
--\COPY sellerRatingsReactions FROM 'data/generated/SellerRatingReactions.csv' WITH DELIMITER ',' NULL '' CSV

\COPY VersionInCart FROM 'data/generated/VersionInCartTest.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Gift FROM 'data/generated/GiftsTest.csv' WITH DELIMITER ',' NULL '' CSV
\COPY messages FROM 'data/generated/Messages.csv' WITH DELIMITER ',' NULL '' CSV
