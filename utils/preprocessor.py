import sys
from tqdm import tqdm
import pandas as pd
import re

class Preprocessor():

    def __init__(self,
                max_length,
                indreg,
                semantic,
                syntax,
                cased) -> None:

        self.vocab = ['[PAD]']

        self.max_length = max_length
        self.cased = cased
        self.corpus = []
        self.tokens = []

        self.indreg = indreg
        self.semantic = semantic
        self.syntax = syntax

    def clean_sentence(self, sentence):
            # Membersihkan dari karakter tidak standard
            sentence = re.sub(r"[^A-Za-z(),!?\'\`]", " ", sentence)

            sentence = re.sub(r"\'s", " \'s", sentence)
            sentence = re.sub(r"\'ve", " \'ve", sentence)
            sentence = re.sub(r"n\'t", " n\'t", sentence)
            sentence = re.sub(r"\n", "", sentence)
            sentence = re.sub(r"\'re", " \'re", sentence)
            sentence = re.sub(r"\'d", " \'d", sentence)
            sentence = re.sub(r"\'ll", " \'ll", sentence)
            sentence = re.sub(r",", " , ", sentence)
            sentence = re.sub(r"!", " ! ", sentence)
            sentence = re.sub(r"'", "", sentence)
            sentence = re.sub(r'""', "", sentence)
            sentence = re.sub(r"\(", "", sentence)
            sentence = re.sub(r"\)", "", sentence)
            sentence = re.sub(r"\?", " \? ", sentence)
            sentence = re.sub(r"\,", "", sentence)
            sentence = re.sub(r"\s{2,}", " ", sentence)

            if not self.cased:
                sentence = sentence.lower()

            return sentence.strip()
    
    def load_indreg(self):

        villages = []
        districts = []
        regencies = []
        provinces = []

        path_vil = "villages.csv"
        path_dis = "districts.csv"
        path_reg = "regencies.csv"
        path_prov = "provinces.csv"

        with open(self.indreg+path_vil, "r", encoding="utf-8") as rd:
            for i, line in enumerate(tqdm(rd)):
                item = line.split(",")
                kelurahan = self.clean_sentence(item[2])
                kelurahan = kelurahan.title()
                villages.append(kelurahan)

        with open(self.indreg+path_dis, "r", encoding="utf-8") as rd:
            for i, line in enumerate(tqdm(rd)):
                item = line.split(",")
                kecamatan = self.clean_sentence(item[2])
                kecamatan = kecamatan.title()
                districts.append(kecamatan)

        with open(self.indreg+path_reg, "r", encoding="utf-8") as rd:
            for i, line in enumerate(tqdm(rd)):
                item = line.split(",")
                kabupaten = self.clean_sentence(item[2])
                kabupaten = kabupaten.title()
                regencies.append(kabupaten)

        with open(self.indreg+path_prov, "r", encoding="utf-8") as rd:
            for i, line in enumerate(tqdm(rd)):
                item = line.split(",")
                provinsi = self.clean_sentence(item[1])
                provinsi = provinsi.title()
                provinces.append(provinsi)

    def load_semantic(self):
        antonym_data = {}
        country_capital = {}
        country_currency = {}
        gender = {}

        path_antonym = "antonyms.txt"
        path_councap = "country-capitals.txt"
        path_councur = "country-currencies.txt"
        path_gender = "gender-specific-words.txt"

        with open(self.semantic+path_antonym, "r", encoding="utf-8") as f:
            for i, line in enumerate(tqdm(f)):
                item = line.split("\t")
                
                k1 = self.clean_sentence(item[0])
                k2 = self.clean_sentence(item[1])

                if k1 != "Word":
                    antonym_data[k1] = k2
        
        with open(self.semantic+path_councap, "r", encoding="utf-8") as f:
            for i, line in enumerate(tqdm(f)):
                item = line.split("\t")
                
                k1 = self.clean_sentence(item[0]).capitalize()
                k2 = self.clean_sentence(item[1]).capitalize()

                if k1 != "Country":
                    country_capital[k1] = k2
        
        with open(self.semantic+path_councur, "r", encoding="utf-8") as f:
            for i, line in enumerate(tqdm(f)):
                item = line.split("\t")
                
                k1 = self.clean_sentence(item[0]).capitalize()
                k2 = self.clean_sentence(item[1]).capitalize()

                if k1 != "Country":
                    country_currency[k1] = k2
        
        with open(self.semantic+path_gender, "r", encoding="utf-8") as f:
            for i, line in enumerate(tqdm(f)):
                item = line.split("\t")
                
                k1 = self.clean_sentence(item[0])
                k2 = self.clean_sentence(item[1])

                if k1 != "Male":
                    gender[k1] = k2

    def load_syntax(self):
        noun = []

        path_noun = "nouns.txt"

        with open(self.syntax+path_noun, "r", encoding="utf-8") as f:
            for i, line in enumerate(tqdm(f)):
                item = line.clean_sentence()
                # item = line.split("\t")

                
                

                print(item)

        
        sys.exit(0)

    def prepare_corpus(self, sentence):
        token = sentence.split(" ")
        # Create Vocab
        for t in token:
            if t not in self.vocab:
                self.vocab.append(t)

        # Create clean corpus
        self.corpus.append(token)

    def tokenizer(self):
        for cp in self.corpus:
            tkn = []
            for tk in cp:
                tkn.append(self.word2idx[tk])

            # Menyamakan panjang sentence
            if len(tkn) < self.max_length:
                tkn += [0] * (self.max_length - len(tkn))
            elif len(tkn) > self.max_length:
                tkn = tkn[:self.max_length]
            
            print("Size : ", len(tkn))
            
            self.tokens.append(tkn)
            

        print(len(self.tokens))

    def preprocessor(self):
        self.load_syntax()

        # self.tokenizer()
    