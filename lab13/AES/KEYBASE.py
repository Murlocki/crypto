class KEYBASE:
    def __init__(self, key:str, word_in_key_count:int, round_count:int):
        self.key = key
        self.word_in_key_count = word_in_key_count
        self.round_count = round_count
    def calculateWordI(self,i,words,calcTemp)->str:
        pass
    # Функция xor по строкам
    @staticmethod
    def _xor_calc(first: str, second: str) -> str:
        return "".join([str(int(first[i]) ^ int(second[i])) for i in range(len(first))])
