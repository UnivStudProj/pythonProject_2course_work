# Упражнение 1
# Назначение: Подсчёт кол-ва слов в документе
# Входные данные: текстовый документ
# Результаты: выполнение программы в соответсвии c заданиями
# Метод решения: добавление в спиок и считывание из него

with open('resourse_1.txt', 'r') as resourse1:
    result1 = open('result_1.txt', 'w')
    wordsDict = {}
    wordsList = []
    n = 0
    # Считываем слова из документа
    for letter in resourse1.read():
        if letter == " ":
            result1.write("\n")
        else:
            result1.write(letter)
    result1.close()
    result1 = open('result_1.txt', 'r')
    # Добавляем в словаь слово с его кол-вом
    for word in result1.readlines():
        word = word.rstrip("\n")
        if word in wordsDict:
            wordsDict[word] += 1
        else:
            wordsDict[word] = 1
    # Добавлем в список кортеж, состоящий из слова и его кол-ва
    for value in wordsDict:
        tempTuple = "tuple" + value
        wordsList.append(tempTuple)
        wordsList[n] = (wordsDict[value], value)
        n += 1
    wordsList.sort(key=lambda x: (-x[0], x[1]))
    result1.close()
    result1 = open('result_1.txt', 'w+')
    # Записываем результат в документ
    for word in wordsList:
        if word != wordsList[len(wordsList) - 1]:
            result1.write(str(word[1]) + " " + str(word[0]) + "\n")
        else:
            result1.write(str(word[1]) + " " + str(word[0]))
    result1.close()
