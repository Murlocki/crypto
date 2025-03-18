from lab13.AES.KEYBASE import KEYBASE


class KEY128(KEYBASE):
    def __init__(self, key: str):
        KEYBASE.__init__(self, key, 4, 10)

    def calculateWordI(self,i,words,calcTemp) ->str:
        if i % 4 == 0:
            temp = calcTemp(words[i - 1], i)
            word = self._xor_calc(words[i - 4], temp)
        else:
            word = self._xor_calc(words[i - 1], words[i - 4])
        return word