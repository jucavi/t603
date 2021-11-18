import csv

with open('users.csv') as file:
    csv_reader = csv.reader(file, delimiter=';')
    for row in csv_reader:
        print(row)


rows = [[f'id({i})', f'f_name({i})', f'l_name{i}'] for i in range(10,20)]

with open('users.csv', "a") as file:
    csv_writer = csv.writer(file, delimiter=',')
    csv_writer.writerow(['001', 'Vito', 'Genovese'])
    csv_writer.writerows(rows)
    
    for row in rows:
        csv_writer.writerow(row)