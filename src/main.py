print('Hello World!')
while True:
    xper1 = int(input("Введите номер месяца: "))
    if xper1 in (1, 2):
        print("Это зимние месяцы")
    elif xper1 in (3, 4, 5):
        print("Это весенние месяцы")
