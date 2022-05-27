import re
import spacy
from spacy.tokens import Span


def make_span_list(new_span, structure, remark, doc):
    # Следующий шаг: делим спан на несколько, если в нем есть перечисления
    if structure.count("CCONJ_und") > 0 or structure.count("PUNCT_,") > 0:
        #print("Aufzählung - ", span)
        remark = remark + " Aufzählung, "
        boundaries = re.findall("(NOUN|PROPN)_[0-9]{1,} (CCONJ|PUNCT)_[^_]{1,}_([0-9]{1,})", structure)
        #print("boundaries - " , boundaries) # [('PUNCT', '25'), ('PUNCT', '27'), ('CCONJ', '32')]
        # wegen ADJ NOUN_12 CCONJ_und_13 NOUN_14 
        # [wegen schweren Diebstahls und Hehlerei]
        span_list = []
        start = new_span.start
        end_span = new_span.end
        try:
            for item in boundaries:
                end = int(item[2])
                #print("start, end - ", start, end)
            
                new_span = Span(doc, start=start, end=end)
                flag = 0
                for token in new_span:
                    if token.pos_ == "NOUN" or token.pos_ == "PROPN":
                        flag = 1
                if flag == 1:
                    span_list.append(new_span)
                start = end
            
            new_span = Span(doc, start=start, end=end_span)
            span_list.append(new_span)
            
        except:
            print("cannot create span list - ", doc)
            span_list = [new_span]
    else:
        span_list = [new_span]
    return span_list, remark