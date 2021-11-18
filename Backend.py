import temp_backend


def RegisterUser(number, password):
    return True


def LogInUser(number, password):
    '''
    Отладочная система входа
    В релизной версии заменить на работы с базой данных
    '''
    return temp_backend.Login_from_json(number, password)


