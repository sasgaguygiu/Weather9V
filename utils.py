def get_poll_handler(message):
    return lambda poll_answer: poll_answer.poll_id == message.poll.id

def get_handler(*args):
    return lambda message: message.text in args

def flat_params(params, prms):
    res = []

    for i in range(len(prms)):
        if prms[i] == 1:
            if type(params[i]) == list:
                res += params[i]
            else:
                res += [params[i]]

    return res

def get_wind_dir(angle):
    if angle >= 335 or angle < 25:
        return "северном"
    elif 25 <= angle < 65:
        return "северо-восточном"
    elif 65 <= angle < 115:
        return "восточном"
    elif 115 <= angle < 155:
        return "юго-восточном"
    elif 155 <= angle < 205:
        return "южном"
    elif 205 <= angle < 245:
        return "югозападном"
    elif 245 <= angle < 295:
        return "западном"
    else:
        return "северном"
