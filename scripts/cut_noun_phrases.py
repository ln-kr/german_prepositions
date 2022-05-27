import re
import spacy
from spacy.tokens import Span

def cut_noun_phrases(new_span, structure, remark):
    
    # ищем случаи, где после существительного идет артикль и другое существительное 
    
    #print(structure)
    np = re.findall("(NOUN|PROPN)_([0-9]{1,}).*DET.*(NOUN|PROPN)", structure)
    

    if len(np) > 0:
        #print(np, int(np[0][1]))
        find_adp = re.findall("ADP.*(NOUN|PROPN).*DET.*(NOUN|PROPN)", structure)
        #print(find_adp)
        if len(find_adp) == 0:
            new_span.end = int(np[0][1]) + 1 
            remark = remark + " Substantive nacheinander, "
            
    return new_span, remark, structure