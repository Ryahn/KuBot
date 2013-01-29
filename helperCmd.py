def everything_between(text,begin,end):
    idx1=text.find(begin)
    idx2=text.find(end,idx1)
    return ' '.join(text[idx1+len(begin):idx2].strip().split())
