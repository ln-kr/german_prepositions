import re
import spacy
from spacy.tokens import Span

def cut_pp(new_span, structure, remark):
    
    # ищем случаи, где после wegen есть существительное, перед существительным нет другого предлога
    """wegen ADJ ADJ ADJ NOUN_24 PUNCT_,_25 NOUN_26 PUNCT_,_27 NOUN_28 ADP_gegen_29 DET X CCONJ_und_32 NOUN_33 
    span modified -  wegen gemeinschaftlicher schwerer räuberischer Erpressung, 
    Freiheitsberaubung, Verstößen gegen das Betäubungsmittel- und Waffengesetz
    """
    #print(structure)
    pp = re.findall("(wegen.*)ADP_[^_]{1,}_([0-9]{1,})", structure)
    #print(pp)

    if len(pp) > 0:
        find_noun = re.findall("(NOUN|PROPN)", pp[0][0])
        #print("find_noun", find_noun)
        if len(find_noun) > 0:
            new_span.end = int(pp[0][1]) 
            remark = remark + " cut pp, "
            structure = pp[0][0]
    return new_span, remark, structure