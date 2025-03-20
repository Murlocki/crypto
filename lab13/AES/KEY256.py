from lab13.AES.KEYBASE import KEYBASE


class KEY256(KEYBASE):
    def __init__(self, key: str):
        KEYBASE.__init__(self, key, 8, 14)

    def calculateWordI(self,i,words,calcTemp) ->str:
        if i % 8 == 0:
            temp = calcTemp(words[i - 1], i)
            word = self._xor_calc(words[i - 8], temp)
        elif i%4 == 0:
            word = words[i] + words[i-8]
        else:
            word = self._xor_calc(words[i - 1], words[i - 8])
        return word