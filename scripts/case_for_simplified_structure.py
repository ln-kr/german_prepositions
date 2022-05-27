import re
import spacy
from spacy.tokens import Span
from correct_wrong_parse import correct_wrong_parse



""" case_final -  1. генитив, 2. датив, 3. не можем сказать, это генитив или датив, 
            4. падеж вообще никак не маркирован, то есть его как бы и нет.
            Группа 3 у нас просто выпадает из игры.
"""
def case_for_simplified_structure(nouns, adjs, articles, span, structure, remark, number, gender, lemma_vs_token):

    case_final = "unknown"
    noun_end = ""
    
    #print("nouns - ", nouns)
    #print("adjs - ", adjs)
    #print("articles - ", articles)
    #print("number - ", number)
    #print("gender - ", gender)
    if len(number) > 0: # существительное должно быть обязательно
        number = number[0]
        if len(gender) == 0: # возможно для propn? (wegen Meckerns) - ошибка парсера
            gender = ""
        else:
            gender = gender[0]

        sorted_nouns_number = list(sorted(nouns))[-1] # выбираем наибольший
        #print("sorted_nouns_number", sorted_nouns_number)
        
        noun_end = nouns[sorted_nouns_number][0]
        #print("orig number", number)
        number, gender, lemma_vs_token = correct_wrong_parse(noun_end, number, gender, lemma_vs_token)
        

        #print("noun_end - ", noun_end)
        #print("number after ", number)

        if bool(articles):
            sorted_articles_number = list(sorted(articles))[0] # выбираем наименьший
            #print('sorted_articles_number', sorted_articles_number)
            article = articles[sorted_articles_number][0]
            #print('article', article)
            article_end = article[-2:]
            #print('article_end', article_end)

            if number == 'Plur':
                #print("is plur")
                if article_end == 'en':
                    #print("article_end == 'en'")
                    if noun_end.endswith("n"):
                        #print('noun_end.endswith("n")')
                        case_final = "Dat"
                    elif noun_end.endswith("s") and lemma_vs_token is "same":
                        case_final = "Dat"
                        #print("check if Dat - ", span)
                    else:
                        #print("noun_end problem")
                        case_final = "Fehler"

                elif article_end == 'er': # wegen der Verletzungen
                    case_final = "Gen"

                else: # wegen die Verletzungen
                    case_final = "null"

            else: # sing
                if gender == "Fem":
    #                    print("gender Fem")
                    if article_end == 'er':
                        case_final = "Gen|Dat" # wegen der Verletzung, wegen einer Verletzung

                    else:
                        case_final = "Fehler"

                else: # neut Mask
                    #print("gender Mask neut")
                    if article_end == 'es':
                        if noun_end.endswith("s"):
                            case_final = "Gen"
                        elif noun_end.endswith('n') and lemma_vs_token is "not":
                            case_final = "Gen"
                        else:
                            case_final = "Fehler"
                    elif article_end == 'em':
                        if noun_end.endswith("s"):
                            case_final = "Fehler"
                        else:
                            case_final = "Dat"
                    else:
                        case_final = "Fehler"

        elif bool(adjs): 

            sorted_adjs_number = list(sorted(adjs))[-1] # выбираем наибольший
            #print('sorted_adjs_number', sorted_adjs_number)
            adj = adjs[sorted_adjs_number][0]
            #print('adj', adj)
            adj_end = adj[-2:]
            #print('adj_end', adj_end)

            if number == 'Plur':
                if noun_end.endswith("n") or noun_end.endswith("s"):  
                    if adj_end == "en":
                        case_final = "Dat" 
                    elif adj_end == "er":
                        case_final = "Gen|Dat"
                    else:
                        case_final = "Fehler" # wegen verschiedene Problemen

                else:
                    if adj_end == "en": # wegen verschiedenen Probleme
                        case_final = "Fehler"
                    elif adj_end == "er": # wegen verschiedener Probleme
                        case_final = "Gen"
                    else:
                        case_final = "Fehler" # wegen verschiedene Probleme, раньше это считалось генитивом, теперь беспадежный

            else: # sing
                if gender == "Fem": # wegen starker Verletzung
                    if adj_end == "er":
                        case_final = "Gen|Dat"
                    else:
                        case_final = "Fehler"
                else: # mask, neut
                    if noun_end.endswith("s"): # wegen Problems
                        if adj_end == "en":
                            case_final = "Gen" # или все-таки беспадежный?
                        else:
        #                                print("possible mistake - ", span)
                            case_final = "null" # wegen Autos
                    else:    
                        if adj_end == "em":
                            case_final = "Dat"
                        else:
                            case_final = "Fehler"
                    #break

        # если нет ни артиклей, ни прил
        else:
            if gender == "Fem": # wegen Verletzung
                case_final = "null"
            #print("no articles and adjs - ", span)
            elif number == 'Plur':
                if noun_end.endswith("n"): # wegen Problemen, wegen Anzeichen
                    if lemma_vs_token is "not": # wegen Problemen
    #                    print("? Dat - ", span)
                        case_final = "Dat" 
                    else: # wegen Anzeichen
                        case_final = "null" # раньше это считалось генитивом, теперь беспадежный
                else:
                    case_final = "null" # wegen Probleme

            else: # sing
#                 if gender == "Fem": # wegen Verletzung
#                     case_final = "null"
#                 else: # mask, neut
                if noun_end.endswith("s"): # wegen Problems
                    #if lemma_vs_token is "not":
                    case_final = "Gen" # или все-таки беспадежный?
#                     else:
#                         print("possible mistake - ", span)
#                         case_final = "null" # wegen Autos
                else:     
                    case_final = "null"
    else:
        print("no nouns? - ", nouns, span)
    
    return case_final, number, gender, lemma_vs_token, noun_end