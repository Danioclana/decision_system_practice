from src.infra.Connection import Connection

import logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

class CategoryRepository:
    def __init__(self):
        try:
            self.connection = Connection().get_connection()
        except Exception as e:
            logging.critical("Error initializing CategoryRepository: %s", e)
            raise
    
    def get_categories(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM categories")
                categories = cursor.fetchall()
                logging.info("Fetched %d categories from database.", len(categories))
                return categories
        except Exception as e:
            logging.error("Error fetching categories: %s", e)
            return []
        
    def insert_category(self, name, description):
        try:
            with self.connection.cursor() as cursor:
                query = "INSERT INTO categories (name, description) VALUES (%s, %s)"
                cursor.execute(query, (name, description))
                self.connection.commit()
                logging.info("Category inserted successfully: %s, %s", name, description)
        except Exception as e:
            self.connection.rollback()
            logging.error("Error inserting category (name: %s): %s", name, e)
            
    def delete_category(self, category_id):
        try:
            with self.connection.cursor() as cursor:
                query = "DELETE FROM categories WHERE id = %s"
                cursor.execute(query, (category_id,))
                self.connection.commit()
                logging.info("Category deleted successfully (ID: %s).", category_id)
        except Exception as e:
            self.connection.rollback()
            logging.error("Error deleting category (ID: %s): %s", category_id, e)
            
    def update_category(self, category_id, name=None):
        try:
            fields = []
            values = []
            
            if name:
                fields.append("name = %s")
                values.append(name)
            
            query = "UPDATE categories SET " + ", ".join(fields) + " WHERE id = %s"
            values.append(category_id)
            
            with self.connection.cursor() as cursor:
                cursor.execute(query, values)
                self.connection.commit()
                logging.info("Category updated successfully (ID: %s).", category_id)
        except Exception as e:
            self.connection.rollback()
            logging.error("Error updating category (ID: %s): %s", category_id, e)
            
    def get_category_by_id(self, category_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM categories WHERE id = %s", (category_id,))
                category = cursor.fetchone()
                logging.info("Fetched category from database (ID: %s).", category_id)
                return category
        except Exception as e:
            logging.error("Error fetching category (ID: %s): %s", category_id, e)
            return None
        
    def get_categories_by_name(self, name):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM categories WHERE name = %s", (name,))
                categories = cursor.fetchall()
                logging.info("Fetched %d categories from database.", len(categories))
                return categories
        except Exception as e:
            logging.error("Error fetching categories by name (name: %s): %s", name, e)
            return []
        
