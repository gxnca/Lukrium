from peewee import *
import json

# Database connection
db_path = 'database.db'
db = SqliteDatabase(db_path)

# Define the model for the `sample_prod_info` table
class SampleProdInfo(Model):
    id = AutoField()
    product_dsc = CharField()
    product_short_dsc = CharField()

    _20231226 = FloatField(column_name='20231226', null = True)

    class Meta:
        database = db
        db_table = 'sample_prod_info'

def export_sample_prod_info_to_json(output_file='sample_prod_info.json'):
    """
    Queries the `sample_prod_info` table, filters the data, and writes it to a JSON file.

    Args:
        output_file (str): The name of the output JSON file.
    """
    try:
        with db.atomic():  # Ensure atomic transactions
            # Query all records from `sample_prod_info`
            records = SampleProdInfo.select()

            # Prepare a list to hold the data
            data_list = []

            # Collect data from each record
            for record in records:
                record_data = {field.name: getattr(record, field.name) for field in record._meta.sorted_fields}
                data_list.append(record_data)

            # Filter the dataset based on the condition
            filtered_dataset = [item for item in data_list if item.get("_20231226", 0) <= 0.9]
            # Write the filtered data to a JSON file
            with open(output_file, 'w') as json_file:
                json.dump(filtered_dataset, json_file, indent=4)

    except IntegrityError as e:
        print(f"Integrity error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()  # Ensure the connection is closed
