from src.infra.Connection import Connection

import logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

class AssetRepository:
    def __init__(self):
        try:
            self.connection = Connection().get_connection()
        except Exception as e:
            logging.critical("Error initializing AssetRepository: %s", e)
            raise

    def get_assets(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM assets")
                assets = cursor.fetchall()
                logging.info("Fetched %d assets from database.", len(assets))
                return assets
        except Exception as e:
            logging.error("Error fetching assets: %s", e)
            return []

    def insert_asset(self, name, type, category_id):
        try:
            with self.connection.cursor() as cursor:
                query = "INSERT INTO assets (name, type, category_id) VALUES (%s, %s, %s)"
                cursor.execute(query, (name, type, category_id))
                self.connection.commit()
                logging.info("Asset inserted successfully: %s, %s, %s", name, type, category_id)
        except Exception as e:
            self.connection.rollback()
            logging.error("Error inserting asset (name: %s, type: %s, category_id: %s): %s", name, type, category_id, e)

    def delete_asset(self, asset_id):
        try:
            with self.connection.cursor() as cursor:
                query = "DELETE FROM assets WHERE id = %s"
                cursor.execute(query, (asset_id,))
                self.connection.commit()
                logging.info("Asset deleted successfully (ID: %s).", asset_id)
        except Exception as e:
            self.connection.rollback()
            logging.error("Error deleting asset (ID: %s): %s", asset_id, e)

    def update_asset(self, asset_id, name=None, type=None, category_id=None):
        try:
            fields = []
            values = []

            if name:
                fields.append("name = %s")
                values.append(name)
            if type:
                fields.append("type = %s")
                values.append(type)
            if category_id:
                fields.append("category = %s")
                values.append(category_id)

            if fields:
                with self.connection.cursor() as cursor:
                    query = f"UPDATE assets SET {', '.join(fields)} WHERE id = %s"
                    values.append(asset_id)
                    cursor.execute(query, tuple(values))
                    self.connection.commit()
                    logging.info("Asset updated successfully (ID: %s).", asset_id)
            else:
                logging.warning("No fields provided for asset update (ID: %s).", asset_id)
        except Exception as e:
            self.connection.rollback()
            logging.error("Error updating asset (ID: %s): %s", asset_id, e)

    def get_asset_by_id(self, asset_id):
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM assets WHERE id = %s"
                cursor.execute(query, (asset_id,))
                asset = cursor.fetchone()
                if asset:
                    logging.info("Fetched asset by ID: %s", asset_id)
                else:
                    logging.warning("No asset found with ID: %s", asset_id)
                return asset
        except Exception as e:
            logging.error("Error fetching asset by ID (%s): %s", asset_id, e)
            return None

    def get_assets_by_category(self, category_id):
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM assets WHERE category = %s"
                cursor.execute(query, (category_id,))
                assets = cursor.fetchall()
                logging.info("Fetched %d assets by category: %s", len(assets), category_id)
                return assets
        except Exception as e:
            logging.error("Error fetching assets by category (%s): %s", category_id, e)
            return []

    def get_assets_by_type(self, type):
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM assets WHERE type = %s"
                cursor.execute(query, (type,))
                assets = cursor.fetchall()
                logging.info("Fetched %d assets by type: %s", len(assets), type)
                return assets
        except Exception as e:
            logging.error("Error fetching assets by type (%s): %s", type, e)
            return []

    def get_assets_by_name(self, name):
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM assets WHERE name LIKE %s"
                cursor.execute(query, (f"%{name}%",))
                assets = cursor.fetchall()
                logging.info("Fetched %d assets by name: %s", len(assets), name)
                return assets
        except Exception as e:
            logging.error("Error fetching assets by name (%s): %s", name, e)
            return []

    def __del__(self):
        try:
            self.connection.close()
            logging.info("Database connection closed in AssetRepository.")
        except Exception as e:
            logging.error("Error closing database connection in AssetRepository: %s", e)
