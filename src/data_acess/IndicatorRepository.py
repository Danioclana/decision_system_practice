from src.infra.Connection import Connection

import logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

class IndicatorRepository:
    def __init__(self):
        try:
            self.connection = Connection().get_connection()
        except Exception as e:
            logging.critical("Error initializing IndicatorRepository: %s", e)
            raise

    def get_indicators(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM indicators")
                indicators = cursor.fetchall()
                logging.info("Fetched %d indicators from database.", len(indicators))
                return indicators
        except Exception as e:
            logging.error("Error fetching indicators: %s", e)
            return []

    def insert_indicator(self, name, value, asset_id):
        try:
            with self.connection.cursor() as cursor:
                query = "INSERT INTO indicators (name, value, asset_id) VALUES (%s, %s, %s)"
                cursor.execute(query, (name, value, asset_id))
                self.connection.commit()
                logging.info("Indicator inserted successfully: %s, %s, %s", name, value, asset_id)
        except Exception as e:
            self.connection.rollback()
            logging.error("Error inserting indicator (name: %s, value: %s, asset_id: %s): %s", name, value, asset_id, e)

    def delete_indicator(self, indicator_id):
        try:
            with self.connection.cursor() as cursor:
                query = "DELETE FROM indicators WHERE id = %s"
                cursor.execute(query, (indicator_id,))
                self.connection.commit()
                logging.info("Indicator deleted successfully (ID: %s).", indicator_id)
        except Exception as e:
            self.connection.rollback()
            logging.error("Error deleting indicator (ID: %s): %s", indicator_id, e)

    def update_indicator(self, indicator_id, name=None, value=None, asset_id=None):
        try:
            fields = []
            values = []

            if name:
                fields.append("name = %s")
                values.append(name)
            if value is not None:
                fields.append("value = %s")
                values.append(value)
            if asset_id:
                fields.append("asset_id = %s")
                values.append(asset_id)

            if fields:
                with self.connection.cursor() as cursor:
                    query = f"UPDATE indicators SET {', '.join(fields)} WHERE id = %s"
                    values.append(indicator_id)
                    cursor.execute(query, tuple(values))
                    self.connection.commit()
                    logging.info("Indicator updated successfully (ID: %s).", indicator_id)
            else:
                logging.warning("No fields provided for indicator update (ID: %s).", indicator_id)
        except Exception as e:
            self.connection.rollback()
            logging.error("Error updating indicator (ID: %s): %s", indicator_id, e)

    def get_indicator_by_id(self, indicator_id):
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM indicators WHERE id = %s"
                cursor.execute(query, (indicator_id,))
                indicator = cursor.fetchone()
                if indicator:
                    logging.info("Fetched indicator by ID: %s", indicator_id)
                else:
                    logging.warning("No indicator found with ID: %s", indicator_id)
                return indicator
        except Exception as e:
            logging.error("Error fetching indicator by ID (%s): %s", indicator_id, e)
            return None

    def get_indicators_by_name(self, name):
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM indicators WHERE name LIKE %s"
                cursor.execute(query, (f"%{name}%",))
                indicators = cursor.fetchall()
                logging.info("Fetched %d indicators by name: %s", len(indicators), name)
                return indicators
        except Exception as e:
            logging.error("Error fetching indicators by name (%s): %s", name, e)
            return []

    def get_indicators_by_asset(self, asset_id):
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM indicators WHERE asset_id = %s"
                cursor.execute(query, (asset_id,))
                indicators = cursor.fetchall()
                logging.info("Fetched %d indicators by asset ID: %s", len(indicators), asset_id)
                return indicators
        except Exception as e:
            logging.error("Error fetching indicators by asset ID (%s): %s", asset_id, e)
            return []

    def __del__(self):
        try:
            self.connection.close()
            logging.info("Database connection closed in IndicatorRepository.")
        except Exception as e:
            logging.error("Error closing database connection in IndicatorRepository: %s", e)
