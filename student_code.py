import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact):
        """Retract a fact from the KB

        Args:
            fact (Fact) - Fact to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact])
        ####################################################
        # Student code goes here

        if isinstance(fact, Fact):
            if fact in self.facts :
                ind = self.facts.index(fact)
                fact = self.facts[ind]
                if len(fact.supported_by) == 0:
                    print('CASE :if fact is  not supported by another facts ')

                    #################### remove the fact from the kb ###################
                    self.facts.remove(fact)
                    
                    # remove in supported by facts and rules
                    for f in self.facts:
                        for s in f.supported_by:
                            if s[0]==fact:
                                ind = f.supported_by.index(s)
                                f.supported_by.remove(s)
                    for r in self.rules:
                        for s in r.supported_by:   # s=[fact, rule]
                            if  s[0]==fact:
                                ind = r.supported_by.index(s)
                                r.supported_by.remove(s)  

                    ################# for each fact it supports  ######################################               
                    for f in fact.supports_facts :
                        self.kb_retract(f)
                    ################### for each rule that it supports  ###########################
                    for r in fact.supports_rules:
                        self.remove_rules(r)
                else: #if Fact is supported by other facts
                    if fact.asserted :
                        print('CASE : Fact is asserted + supported by other facts')
                        fact.asserted = False
                    else:
                        print('CASE : Fact is not asserted but supported by other facts')
   
                    
    def remove_rules(self, rule):
        if rule in self.rules:
            if not rule.asserted :
                ind = self.rules.index(rule)
                rule = self.rules[ind]
                if len(rule.supported_by) == 0:
                    print('CASE : Rule is not asserted + not supported by other facts')

                     #################### remove the rule from the kb ###################
                    self.rules.remove(rule)

                    # remove in supported by facts and rules 
                    for f in self.facts:
                        for s in f.supported_by:  # s=[fact, rule]
                            if s[1]==rule:
                                f.supported_by.remove(s)
                    for r in self.rules:
                        for s in r.supported_by:
                            if s[1]==rule:
                                r.supported_by.remove(s)

                                
                    ################# for each fact it supports  ######################################  
                    for f in rule.supports_facts :
                        self.kb_retract(f)
                    ################### for each rule that it supports  ###########################
                    for r in rule.supports_rules:
                        self.remove_rules(r)
                else:
                    print('CASE : Rule is not asserted but supported by other facts')
            else:
                print('CASE : Rule is asserted so will never be removed')
                

class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # Student code goes here
        #
                ############## implementing Forward_chain ###################
        #  for_loop in kb_add 

        # 1.) Get first statement in LHSof rule
        first_lhs_stat=rule.lhs[0]

        # 2.) Unify fact with first statement
        bindings=match(first_lhs_stat,fact.statement)
        # Matches two statements and return the associated bindings or False if there
        # is no binding


        # 3.)If substitution found
        if bindings!=False:  # if bindings found via match 
            # If LHS has only 1 statement
            if len(rule.lhs)==1:
                 # Create new fact using the substitution on RHS
                new_stat_rhs=instantiate(rule.rhs, bindings)   # Generate Statement from given statement and bindings
                # Add new fact to KB
                newfact=Fact(new_stat_rhs,[[fact,rule]])   #fact arguments :statement, supported_by=[])
                # appending new fact to your supports_facts list in both fact and rule.
                fact.supports_facts.append(newfact)
                rule.supports_facts.append(newfact)
                newfact.asserted=False
                kb.kb_add(newfact)

             
                
            else:
                list=[]

                # Infer new rule with LHS starting from 1  a
                for l in rule.lhs[1:]:
                    each_stat_lhs=instantiate(l,bindings)
                    list.append(each_stat_lhs)

                 # Infer  new rule with RHS 
                new_stat_rhs=instantiate(rule.rhs, bindings)
                newrule=Rule([list,new_stat_rhs],[[fact,rule]])
                # appending new fact to your supports_facts list in both fact and rule.
                fact.supports_rules.append(newrule)
                rule.supports_rules.append(newrule)
                newrule.asserted=False
                # Add new rule to KB
                kb.kb_add(newrule)
