import re
import spacy
from spacy.tokens import Span


def define_structure(span, remark, prep):

    phrase, structure, head = "", "", ""
    article, adj_token, adj_endung, verb = "null", "null", "null", "null"
    lemma_vs_token = "same"       
    article_num = 0
    nouns, adjs, articles = {}, {}, {}
    token_table, lemma, case, gender, number, lemma_vs_token = "", "", "", "", "", ""
    for token in span:
        if token.text == prep:
            structure = structure + prep + " "
        elif token.text == "bis":
            structure = structure + "ADP" + "_"  + token.lemma_ + "_" + str(token.i) + " "
        elif token.pos_ == "ADP":
            structure = structure + token.pos_ + "_"  + token.lemma_ + "_" + str(token.i) + " "
        elif token.pos_ == "CCONJ":
            structure = structure + token.pos_ + "_" + token.lemma_ + "_" + str(token.i) + " "
        elif token.pos_ == "PUNCT":
            structure = structure + token.pos_ + "_" + token.lemma_ + "_" + str(token.i) + " "
        elif token.pos_ == "NOUN" or token.pos_ == "PROPN":
            structure = structure + token.pos_ + "_" + str(token.i) + " "
        else:
            structure = structure + token.pos_ + " "

        if token.pos_ == "NOUN" or token.pos_ == "PROPN":
            token_table = token.text
            lemma = token.lemma_
            case = token.morph.get("Case")
            gender = token.morph.get("Gender")
            number = token.morph.get("Number")
            if token_table != lemma:
                lemma_vs_token = "not"
            nouns[token.i] = ([token_table, lemma, case, gender, number, lemma_vs_token])

        if token.pos_ == "DET":
            article = token.text
            if article.isalpha():
                article_endung = article[-2] + article[-1]
                articles[token.i] = ([article, article_endung])
        if token.pos_ == "ADJ":
            adj_token = token.text
            if adj_token.isalpha():
                adj_endung = adj_token[-2] + adj_token[-1]
                adjs[token.i] = ([adj_token, adj_endung])
    return nouns, adjs, articles, span, structure, remark, number, gender, lemma_vs_token
# case_for_simplified_structure2(nouns, adjs, articles, span, structure, remark, number, gender, noun_end)