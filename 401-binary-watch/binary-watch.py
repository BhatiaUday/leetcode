class Solution:
    def readBinaryWatch(self, turnedOn: int) -> List[str]:
        l=[]
        for h in range(12):
            for m in range(60):
                if bin(h).count('1')+bin(m).count('1')==turnedOn:
                    if m<10:
                        m="0"+str(m)
                    l.append(f"{h}:{m}")
        return l