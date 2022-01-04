#!/usr/bin/env python
import unittest
import read
from student_code import KnowledgeBase
from logical_classes import *

class CustomTests4(unittest.TestCase):

    def setUp(self):
        file = 'statements_kb4.txt'
        self.data = read.read_tokenize(file)
        data = read.read_tokenize(file)
        self.KB = KnowledgeBase([], [])
        for item in data:
            if isinstance(item, Fact) or isinstance(item, Rule):
                self.KB.kb_assert(item)

# ###########################  checkin retract ########################         
    # def test1(self):
        
    #     ask1 = read.parse_input("fact: (motherof ?X ?Y)")
    #     answer1 = self.KB.kb_ask(ask1)
    #     self.assertEqual(len(answer1), 4)
    #     self.assertEqual(str(answer1[0]), "?X : ada, ?Y : bing")
    #     self.assertEqual(str(answer1[1]), "?X : bing, ?Y : chen")
    #     self.assertEqual(str(answer1[2]), "?X : dolores, ?Y : chen")
    #     self.assertEqual(str(answer1[3]), "?X : greta, ?Y : felix")

    #     ask2 = read.parse_input("fact: (sisters ?X ?Y)")
    #     answer2 = self.KB.kb_ask(ask2)
    #     self.assertEqual(len(answer2), 1)
    #     self.assertEqual(str(answer2[0]), "?X : ada, ?Y : eva")

    # def test2(self):
    #     ask1 = read.parse_input("fact: (parentof ?X ?Y)")
    #     answer1 = self.KB.kb_ask(ask1)
    #     self.assertEqual(len(answer1), 4)
    #     self.assertEqual(str(answer1[0]), "?X : ada, ?Y : bing")
    #     self.assertEqual(str(answer1[1]), "?X : bing, ?Y : chen")
    #     self.assertEqual(str(answer1[2]), "?X : dolores, ?Y : chen")
    #     self.assertEqual(str(answer1[3]), "?X : greta, ?Y : felix")

    # def test3(self):
    #     ask1 = read.parse_input("fact: (auntof ?X ?Y)")
    #     answer1 = self.KB.kb_ask(ask1)
    #     self.assertEqual(len(answer1), 1)
    #     self.assertEqual(str(answer1[0]), "?X : eva, ?Y : bing")

    # def test4(self):
    #     ask1 = read.parse_input("fact: (grandmotherof ?X ?Y)")
    #     answer1 = self.KB.kb_ask(ask1)
    #     self.assertEqual(len(answer1), 2)
    #     self.assertEqual(str(answer1[0]), "?X : ada, ?Y : felix")
    #     self.assertEqual(str(answer1[1]), "?X : ada, ?Y : chen")


# ###########################  checkin retract ########################
    def test5(self):
        r1 = read.parse_input("fact: (motherof dolores chen")
        print(' Retracting', r1)
        self.KB.kb_retract(r1)
        ask1 = read.parse_input("fact: (parentof dolores ?X)")
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        # print(answer)
        self.assertEqual(len(answer), 0)


    def test4_6(self):
        print('\nTest 6')
        r1 = read.parse_input("fact: (sisters ada eva)")
        print(' Retracting', r1)
        self.KB.kb_retract(r1)
        ask1 = read.parse_input("fact: (auntof eva ?X)")
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        # print(answer)
        self.assertEqual(len(answer), 0)


    def test7(self):
        ask1 = read.parse_input("fact: (greatgrandmotherof ada ?X)")
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertEqual(str(answer[0]), "?X : bob")
        r1 = read.parse_input("fact: (motherof felix bob)")
        print(' Retracting', r1)
        self.KB.kb_retract(r1)
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertEqual(str(answer), "[]")

    def test8(self):
        r1 = read.parse_input("fact: (parentof felix bob)")
        print(' Retracting', r1)
        self.KB.kb_retract(r1)
        ask1 = read.parse_input("fact: (greatgrandmotherof ada ?X)")
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertEqual(str(answer[0]), "?X : bob")


    def test9(self):
        r1 = read.parse_input("rule: ((parent felix ?y)) -> (greatgrandmother ada ?y)")
        print(' Retracting', r1)
        self.KB.kb_retract(r1)
        ask1 = read.parse_input("fact: (greatgrandmotherof ada ?X)")
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertEqual(str(answer[0]), "?X : bob")

    # def test10(self):
    #     fact = read.parse_input("fact: (grandmotherof ada felix)")
    #     self.KB.kb_retract(fact)
    #     ask1 = read.parse_input("fact: (grandmotherof ?X ?Y)")
    #     answer1 = self.KB.kb_ask(ask1)
    #     self.assertEqual(len(answer1), 1)
    #     self.assertEqual(str(answer1[0]), "?X : ada, ?Y : chen")
    #     fact = read.parse_input("fact: (grandmotherof ada chen)")
    #     self.KB.kb_retract(fact)
    #     ask1 = read.parse_input("fact: (grandmotherof ?X ?Y)")
    #     answer1 = self.KB.kb_ask(ask1)
    #     self.assertEqual(len(answer1), 1)
    #     self.assertEqual(str(answer1[0]), "?X : ada, ?Y : chen")
    #     fact = read.parse_input("fact: (motherof bing chen)")
    #     self.KB.kb_retract(fact)
    #     ask1 = read.parse_input("fact: (grandmotherof ?X ?Y)")
    #     answer1 = self.KB.kb_ask(ask1)
    #     self.assertEqual(len(answer1), 0)

    # def test6(self):
    #     fact = read.parse_input("fact: (grandmotherof ada felix)")
    #     self.KB.kb_retract(fact)
    #     ask1 = read.parse_input("fact: (grandmotherof ?X ?Y)")
    #     answer1 = self.KB.kb_ask(ask1)
    #     self.assertEqual(len(answer1), 1)
    #     self.assertEqual(str(answer1[0]), "?X : ada, ?Y : chen")
    #     fact = read.parse_input("fact: (grandmotherof ada chen)")
    #     self.KB.kb_retract(fact)
    #     ask1 = read.parse_input("fact: (grandmotherof ?X ?Y)")
    #     answer1 = self.KB.kb_ask(ask1)
    #     self.assertEqual(len(answer1), 1)
    #     self.assertEqual(str(answer1[0]), "?X : ada, ?Y : chen")
    #     fact = read.parse_input("fact: (motherof ada bing)")
    #     self.KB.kb_retract(fact)
    #     ask1 = read.parse_input("fact: (grandmotherof ?X ?Y)")
    #     answer1 = self.KB.kb_ask(ask1)
    #     self.assertEqual(len(answer1), 0)

    # def test7(self):
    #     fact = read.parse_input("fact: (sisters ada eva)")
    #     self.KB.kb_retract(fact)
    #     ask1 = read.parse_input("fact: (auntof ?X ?Y)")
    #     answer1 = self.KB.kb_ask(ask1)
    #     self.assertEqual(len(answer1), 0)
        
if __name__ == '__main__':
    unittest.main()