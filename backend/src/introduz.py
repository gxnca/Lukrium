import csv
from peewee import *

# List of CSV files and their corresponding table names
lista_nome = ["sample_account_info_encripted", "sample_prod_info", "sample_sales_info_encripted", "sample_store_info"]
lista_nome_modificado = ["acc", "prod", "sales", "store"]

def inferir_tipo(valor):
    """Tenta inferir o tipo do dado com base no primeiro valor de cada coluna"""
    if valor.isdigit():  # Caso seja um número inteiro
        return IntegerField()
    try:
        float(valor)  # Caso seja um número flutuante
        return FloatField(null=True)
    except ValueError:
        return CharField()  # Caso seja texto

# Database configuration
db_path = 'database.db'
db = SqliteDatabase(db_path)

# Connect to the database
db.connect()

for nome in lista_nome:
    csv_file = f"data/{nome}.csv"
    
    # Read CSV to get headers and infer types
    with open(csv_file, newline='', encoding='utf-8') as con_csv:
        if nome == "sample_prod_info":
            reader = csv.reader(con_csv, delimiter=';')
        else:
            reader = csv.reader(con_csv, delimiter=",")
            
        headers = next(reader)  # Get column titles
        primeiro_valor = next(reader)  # Get first row of values for type inference
        
        # Create dynamic field dictionary for Peewee
        campos = {'id': AutoField()}
        for titulo, valor in zip(headers, primeiro_valor):
            campos[titulo] = inferir_tipo(valor)
        
        # Create dynamic table model
        TabelaDinamica = type(nome, (Model,), {
            **campos, 
            'Meta': type('Meta', (), {'database': db})
        })
        
        # Create the table in the database
        db.create_tables([TabelaDinamica], safe=True)  # 'safe=True' prevents error if table already exists
        
    # Insert CSV data into the table
    with open(csv_file, newline='', encoding='utf-8') as con_csv:
        if nome == "sample_prod_info":
            reader = csv.DictReader(con_csv, delimiter=';')
        else:
            reader = csv.DictReader(con_csv, delimiter=',')
            
        print(f"Headers for {nome}: {reader.fieldnames}")
        
        with db.atomic():  # Use a transaction for better performance
            for row in reader:
                # Clean the row data by removing empty values
                #cleaned_row = {key: value for key, value in row.items() if value not in [None, '']}
                try:
                    TabelaDinamica.create(**row)
                except IntegrityError as e:
                    print(f"Error inserting row: {row}, error: {e}")
                except Exception as e:
                    print(f"Unexpected error inserting row {row}: {e}")

# Close the database connection
db.close()
print(f"Tables created and data inserted successfully in database {db_path}")