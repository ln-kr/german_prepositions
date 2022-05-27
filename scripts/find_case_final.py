import re
import spacy
from spacy.tokens import Span

from cut_pp import cut_pp
from cut_noun_phrases import cut_noun_phrases
from make_span_list import make_span_list
from define_structure import define_structure
from case_for_simplified_structure import case_for_simplified_structure

def find_case_final(structure, nouns, adjs, articles, span, doc, prep, writer, head, remark, number, gender, lemma_vs_token, flag_von, quelle_short):

    flag = 0
    remark = ""
    case_final = "unknown"
    number = ""
    gender = ""
    noun_end = ""
    
    """ Сначала помечаем фразы без существительного и с von .. wegen,
    определяем, постпозиция или норма,
    уточняем границы фразы слева и справа
    """
    # помечаем конструкции von ... wegen, оставляем для анализа
    von_wegen = re.findall("ADP_von.*wegen", structure)
    if len(von_wegen) > 0:
        remark = remark + " beginnt mit von "
        
    # во фразе есть существительное
    old_span = span
    new_span = span
    #  если нет сущ, помечаем и возвращаем датив, тк должно быть личное местоимение, дальше анализировать не надо
    if not structure.count("NOUN"):
        if not structure.count("PROPN"): 
            if structure.count("PRON"):  
                remark = remark + " ohne Nomen, Pronomen, "
                flag = 1
                case_final = "Dat"
                #print("! pronoun found - ", span, structure, doc)
                data = (old_span, new_span, case_final, structure, head, noun_end, remark, flag_von, number, gender, quelle_short, doc)    
                writer.writerow(data)
                return case_final, number, gender, remark
            else:
                remark = remark + " ohne Nomen, "
                case_final = "Fehler"
                #print("! no noun - ", span, structure, doc)
                data = (old_span, new_span, case_final, structure, head, noun_end, remark, flag_von, number, gender, quelle_short, doc)    
                writer.writerow(data)
                return case_final, number, gender, remark
    

    
    # определяем тип фразы: wegen в постпозиции или нет
    wegen_norm = re.findall("wegen.*(NOUN|PROPN)", structure)
    if len(wegen_norm) == 0:
        wegen_post = re.findall("(NOUN|PROPN).*wegen", structure)
        if len(wegen_post) == 0:
            print("wrong example - ", span, structure)
            return case_final, number, gender, remark
        else:
            #print("wegen in postposition - ", span, structure)
            remark = remark + " postposition "
            end_wegen = [token.i for token in span if token.text == "wegen"][0]
            new_span.end = end_wegen
            #print("span modified - ", new_span)
    else:
        start_wegen = [token.i for token in span if token.text == "wegen"][0]
        new_span.start = start_wegen
        
        nouns_wegen = []
        for token in new_span:
            if token.pos_ in ["NOUN", "PROPN"]:
                if token.text.isalpha():
                    nouns_wegen.append(token.i)
                elif token.text.isdigit():
                    print("strange noun - ", new_span)
                    return case_final, flag, remark
                else:
                    if token.text.count('-'):
                        nouns_wegen.append(token.i)
                    #print("noun with hyphen? - ", new_span)
                    #nouns_wegen.append(token.i)
        
        if len(nouns_wegen) == 0:
            print("lost nouns! ", new_span)
            return case_final, number, gender, remark
        else:
            #print(nouns_wegen)
            last_noun = nouns_wegen[-1]
            #print("last_noun - ", last_noun)
            new_span.end = last_noun + 1
    
    #print("span modified - ", new_span)
    # Следующий шаг: отрезать предложную группу, если она не входит в причастный оборот
    
    new_span, remark, structure = cut_pp(new_span, structure, remark)
    #print("after cut pp - ", new_span)
    
    # делим спан на несколько, если в нем есть перечисления
    
    span_list, remark = make_span_list(new_span, structure, remark, doc)
    #print("span_list ", span_list)
    
    new_span_list = []
    for item in span_list:
        item, remark, structure = cut_pp(item, structure, remark)
        #print("after pp", item)
        item, remark, structure = cut_noun_phrases(item, structure, remark)
        #print("after np",item)
        flag = 0
        for token in item:
            if token.text.count("(") > 0 or token.text.count(")") > 0 :
                flag = 0
                break
            if token.pos_ == "NOUN" or token.pos_ == "PROPN":
                #print("pos noun propn", token)
                flag = 1
        if flag == 1:
            new_span_list.append(item)
        #new_span_list.append(item)
        
    #print("new_span_list - ", new_span_list)
    
    # для каждого отдельного спана создаем его структуру
    for span_last in new_span_list:
        nouns, adjs, articles, span_last, structure, remark, number, gender, lemma_vs_token = define_structure(span_last, remark, prep)
        #print(nouns)
        # Для каждого отдельного спана определяем ключевое существительное. Определяем падеж
        case_final, number, gender, lemma_vs_token, noun_end = case_for_simplified_structure(nouns, adjs, articles, span_last, structure, remark, number, gender, lemma_vs_token)
        
        data = (old_span, span_last, case_final, structure, head, noun_end, remark, flag_von, number, gender, quelle_short, doc)
                        
        writer.writerow(data)
        #print("data - ", span_last, case_final, structure)
    
        #print("CASE FINAL", case_final)
        
    #return writer # cases_list[0]