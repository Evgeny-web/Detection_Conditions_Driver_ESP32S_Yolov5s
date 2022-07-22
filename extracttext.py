import re


# x = ("[tensor([[5.04049e+02, 2.27700e+02, 8.07149e+02, 5.74507e+02, 4.93311e-01, 1.50000e+01],"
    # " [5.03042e+02, 2.06521e+02, 8.02803e+02, 5.89118e+02, 3.87255e-01, 1.60000e+01]])]")

x = str("[tensor([[522.40430, 242.96176, 755.49634, 539.18066,   0.97812,  16.00000]])]")


try:
    list_variables_model = [float(i) for i in re.findall(r'-?\d+\.?\d*', x)]

    # достанем x, y, w, h, class_id
    if len(list_variables_model) > 6:
        x = int(list_variables_model[0] * 10 ** int(list_variables_model[1]))
        y = int(list_variables_model[2] * 10 ** int(list_variables_model[3]))
        w = int(list_variables_model[4] * 10 ** int(list_variables_model[5]))
        h = int(list_variables_model[6] * 10 ** int(list_variables_model[7]))
        class_id = int(list_variables_model[10] * 10 ** int(list_variables_model[11]))
    else:
        x = int(list_variables_model[0])
        y = int(list_variables_model[1])
        w = int(list_variables_model[2])
        h = int(list_variables_model[3])
        class_id = int(list_variables_model[5])

    # Выводим номер класса
    # print("Class_id: ", class_id)

except Exception:
    x = None
    y = None
    w = None
    h = None
    class_id = None

datas = []
datas.append(x)
datas.append(y)
datas.append(w)
datas.append(h)
datas.append(class_id)

return datas