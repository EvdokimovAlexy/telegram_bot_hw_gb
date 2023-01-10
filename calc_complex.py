def complex_input(user_str):
    lenght = len(user_str)
    strRe = ''
    strIm = ''
    flagIm = False
    for i in range(lenght):
        if user_str[i].isdigit() or user_str[i] == '-':
            if flagIm == False and user_str[i + 1] != "i":
                strRe = strRe + user_str[i]
                if user_str[i + 1] == "+" or user_str[i + 1] == "-":
                    flagIm = True
            else:
                strIm = strIm + user_str[i]
    if strIm == '':
        strIm = '1'
    if strRe == '':
        strRe = '0'
    return [int(strRe), int(strIm)]


def complex_operations(num1, num2, oper):
    match oper:
        case '+':
            if (num1[1] + num2[1]) >= 0:
                result = str(num1[0] + num2[0]) + '+' + str(num1[1] + num2[1]) + 'i'
            else:
                result = str(num1[0] + num2[0]) + str(num1[1] + num2[1]) + 'i'
        case '-':
            if (num1[1] + num2[1]) >= 0:
                result = str(num1[0] - num2[0]) + '+' + str(num1[1] - num2[1]) + 'i'
            else:
                result = str(num1[0] - num2[0]) + str(num1[1] - num2[1]) + 'i'
        case '*':
            if (num1[0] * num2[1] + num1[1] * num2[0]) >= 0:
                result = str(num1[0] * num2[0] - num1[1] * num2[1]) + '+' + str(
                    num1[0] * num2[1] + num1[1] * num2[0]) + 'i'
            else:
                result = str(num1[0] * num2[0] - num1[1] * num2[1]) + str(num1[0] * num2[1] + num1[1] * num2[0]) + 'i'
        case '/':
            if ((num1[1] * num2[0] - num1[0] * num2[1]) / (num2[0] ** 2 + num2[1] ** 2)) >= 0:
                result = str((num1[0] * num2[0] + num1[1] * num2[1]) / (num2[0] ** 2 + num2[1] ** 2)) + '+' + str(
                    (num1[1] * num2[0] - num1[0] * num2[1]) / (num2[0] ** 2 + num2[1] ** 2)) + 'i'
            else:
                result = str((num1[0] * num2[0] + num1[1] * num2[1]) / (num2[0] ** 2 + num2[1] ** 2)) + str(
                    (num1[1] * num2[0] - num1[0] * num2[1]) / (num2[0] ** 2 + num2[1] ** 2)) + 'i'
    return result