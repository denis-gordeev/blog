def parse(text):
    text = text.split(' ')
    history.append(text)
    return text
def reply(parsed_text):
    if flags['greeting'] == 0:
        flags['greeting'] = 1
        return 'Hi'
    else:
        return '''I'm just a simple ChatBot, yet to be implemented'''
flags = {'greeting':0}

history = []

def main(text):
    parsed_text = parse(text)
    answer = reply(parsed_text)
    return answer
