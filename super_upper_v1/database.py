sections_table = """
                 CREATE TABLE sections(
                         id INT NOT NULL AUTO_INCREMENT, 
                         name VARCHAR(255), 
                         url VARCHAR(255), 
                         PRIMARY KEY(id)
                 );
                 """

products_table = """
                 CREATE TABLE products(
                         id INT NOT NULL AUTO_INCREMENT,
                         item INT,
                         barcode INT,
                         name VARCHAR(255),
                         sub_section_id INT,
                         PRIMARY KEY(id),
                 );
                 """
       
price_records_table = """
                      CREATE TABLE price_records(
                      id INT NOT NULL AUTO_INCREMENT,
                      product_id INT,
                      price float,
                      record_time int,
                      PRIMARY KEY(id),
                      FOREIGN KEY (product_id) REFERENCES products(id)
                      );
                      """
       
nutritional_values_table = """
                           CREATE TABLE nutritional_values(
                           id INT NOT NULL AUTO_INCREMENT,
                           product_id INT,
                           item INT,
                           barcode int,
                           name VARCHAR(255),
                           nutritional_facts INT,
                           PRIMARY KEY(id),
                           FOREIGN KEY (product_id) REFERENCES products(id)
                           );
                           """
       
nutritional_facts_table = """
                          CREATE TABLE nutritional_facts(
                          id INT NOT NULL AUTO_INCREMENT,
                          nutritional_facts_en VARCHAR(255),
                          nutritional_facts_he VARCHAR(255),
                          PRIMARY KEY(id)
                          );
                          """

foreign_keys_alter_nutritional_values_table = """
                                              ALTER TABLE nutritional_values 
                                              ADD FOREIGN KEY (nutritional_facts) REFERENCES nutritional_facts(id);
                                              """

foreign_keys_alter_nutritional_facts_table = """
                                             ALTER TABLE nutritional_facts
                                             ADD FOREIGN KEY (id) REFERENCES nutritional_values(nutritional_facts);
                                             """

tables_queries = [sections_table,
                  products_table,
                  price_records_table,
                  nutritional_facts_table,
                  nutritional_values_table
                  ]

foreign_keys_queries = [foreign_keys_alter_nutritional_values_table,
                        foreign_keys_alter_nutritional_facts_table
                        ]

select_products_items_query = """
SELECT item, id
FROM products
"""