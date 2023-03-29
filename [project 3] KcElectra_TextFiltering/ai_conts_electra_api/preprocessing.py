import re

class Preprocessing():

    def __init__(self, sent):
        self.sent = sent

    def clean_sentence(self):
        try:  # 무성의
            self.sent = re.sub('[^\w\s]', ' ', self.sent).strip()
            self.sent = re.sub('[.,?!ᆢ~]', ', ', self.sent)
            self.sent = re.sub('[ㄱ-ㅎ|ㅏ-ㅣ]', 'ㅋ', self.sent)
            self.sent = re.sub('니다', '니다. ', self.sent)
            self.sent = re.sub('어요', '어요. ', self.sent)
            self.sent = re.sub('\n', ' ', self.sent).strip()

        except:
            # log.Log(f"clean_sentence error : Request - mem_no : {i.memNo} - mateConts : {i.mateConts} - familyConts : {i.familyConts}")
            pass

        return self.sent

    def f_clean_sentence(self):
        try:
            self.sent = re.sub('[^\w\s]', ' ', self.sent).strip()
            self.sent = re.sub('[.,?!ᆢ~]', ', ', self.sent)
            self.sent = self.return_text(self.sent)

        except:
            # log.Log(f"f_clean_sentence errer : Request - mem_no : {i.memNo} - mateConts : {i.mateConts} - familyConts : {i.familyConts}")
            pass
        return self.sent

    def sub_num(self, sent):
        hannum_list = ['일', '이', '삼', '사', '오', '육', '륙', '칠', '팔', '구', '십', '영']
        sent = re.sub(r'[0-9]', ' ', sent)

        for i in hannum_list:
            sent = re.sub(rf'{i}', '  ', sent)
        return sent

    def return_target_list(self, pattern, sent):
        word_list = []
        for i in pattern.finditer(sent):
            target_word = sent[i.start(): i.end()]
            word_list.append(target_word)
        return word_list

    def return_text(self, sent):

        nam = '[남]+'
        nyeo = '[녀]+'
        yeo = '[여]+'
        son = '[아들]+'
        ddal = '[딸]+'
        num = '[\s]*(\d){1,2}[\s]*'
        han_num = '[일이삼사오육륙칠팔구십]+'

        person_list = [nam, son, nyeo, yeo, ddal]
        num_list = [num, han_num]

        for person_pattern in person_list:
            for num_pattern in num_list:
                pattern_list = [person_pattern + num_pattern, num_pattern + person_pattern]
                target_list = []

                for pattern in pattern_list:
                    add_pattern = re.compile(pattern)
                    m = add_pattern.findall(sent)
                    if m != []:
                        target_words = self.return_target_list(add_pattern, sent)
                        target_list += target_words
                    else:
                        pass

                for i in target_list:
                    sent = sent.replace(i, self.sub_num(i))
        return sent