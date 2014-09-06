#!/usr/bin/python

import nltk

def parse(post):
    parse = Parser(post)
    print parse.sentences
    print parse.parse()
    message = Speaker(parse)
    print message.text
    return message.text

class Parser():
    '''
    Parsing the text. Analyzing it structure. English only.
    '''
    def __init__(self,text):
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        text = sent_detector.tokenize(text.strip())
        sentences = tuple([tuple(nltk.word_tokenize(sent)) for sent in text])
        self.text = text
        self.sentences = sentences
        self.parsed = []
    def parse(self):
        '''
        parsing the sentence
        '''
        personal_pronouns = set(('I', 'you', 'he', 'she', 'we', 'they'))
        for sent in self.sentences:
            parse_sent = [[el,'Funct','POS'] for el in sent]
            if set(sent) and personal_pronouns:
                for el in sent:
                    if el in personal_pronouns:
                        parse_sent[sent.index(el)][1] = 'Subject'
            self.parsed.append(parse_sent)
        return self.parsed
    def simple_sent(self):
        return len(self.parsed), self.parsed

class Speaker():
    '''
    Creating the output. Receives Parser object.
    Parser -> str
    '''
    def __init__(self,parsed_text):
        self.ptext = parsed_text
        self.text = 'lol'

#parse("I eat meatballs because they are tasty and you don't cause you are poor. So the things are")
