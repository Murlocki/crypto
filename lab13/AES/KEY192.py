from lab13.AES.KEYBASE import KEYBASE


class KEY192(KEYBASE):
    def __init__(self, key: str):
        KEYBASE.__init__(self, key, 6, 12)

    def calculateWordI(self,i,words,calcTemp) ->str:
        if i % 6 == 0:
            temp = calcTemp(words[i - 1], i)
            word = self._xor_calc(words[i - 6], temp)
        else:
            word = self._xor_calc(words[i - 1], words[i - 6])
        return word