class PastebinUtil:
    
    def base36_encode(link):
        assert link >= 0, 'Positive integer is required'
        if link == 0:
            return '0'
        base36 = []
        while link != 0:
            link, i = divmod(link, 36)
            base36.append('0123456789abcdefghijklmnopqrstuvwxyz'[i])
        return ''.join(reversed(base36))