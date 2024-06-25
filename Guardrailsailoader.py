from typing import Optional
from transformers import AutoModelForCausalLM, AutoTokenizer
from helperutil import read_yaml_conf,intializelogger
from guardrails.hub import (
    ToxicLanguage,
    RegexMatch,
    GibberishText,
    DetectPII,
    NSFWText,
    FinancialTone,
    ProfanityFree, 
    SensitiveTopic, 
    RestrictToTopic
)
from guardrails import Guard
#from prompttemplate import guardpromptbuilder
import torch
import os,json,sys
import logging 

class guardloader:


  def __init__(self,configfile, contextinp:str, validation_args="full" logger) -> None:

      self.llmconf = read_yaml_conf(configfile)
      self.contextinp = contextinp
      self.logger = logger
      self.allowedvalidations = self.llmconf[allowedvalidations]

  def evalrunner(self,validation_args):
      """
      wrapper runner to invoke deterministic and probabilistic eval functions 
      allowedvalidations list("full", "deterministic", "probablistic") will be consumed from conf
      """    
      if validation_args not in self.allowedvalidations:
            raise ValueError('selected {validation_args} not allowed. please select from {allowedvalidations}')
      
      try:

           if validation_args == "deterministic":
              self.deterministiceval(self.contextinp)

           elif validation_args == "probablistic":
              self.probablisticeval(self.contextinp)

           else:    
              self.deterministiceval(self.contextinp)
              self.logger.info("Proceeding with probablisticeval")
              self.probablisticeval(self.contextinp)

      except Exception as errmsg:
             logger.info("encountered issue while evaluating {validation_args}")
          

  def deterministiceval(self, self.contextinp):
          """
          input: Accepts sentence input and performs relevant deterministic evaluvation checks 
          return json repsonse

          """
          try:

              # refer pii_entities from conf 
              self.pii_entities = self.llmconf[pii_entities]

              guard = Guard().use_many(

                  FinancialTone(
                      threshold=0.5,
                      on_fail="exception"
                  ),

                  ToxicLanguage(
                      validation_method='sentence',
                      threshold=0.5
                  ),
                  RegexMatch(
                  regex="^[A-Z].*",
                  on_fail="exception"
                  ),
                  GibberishText(
                      threshold=0.5,
                      validation_method="sentence",
                      on_fail="exception"
                  ),
                  DetectPII(
                      pii_entities=self.pii_entities,
                      on_fail="exception"
                    ),
                  NSFWText(
                      threshold=0.8, validation_method="sentence", on_fail="exception"
                  ),
                  ProfanityFree(on_fail="exception")

              )
              response = guard.validate(contextinp)
              response = json.loads(response.json())
              return response
          except Exception as errmsg:
              logger.error("error while validating deterministiceval")
              return errmsg.args[0]


  def probablisticeval(self, self.contextinp):
          """
          input: Accepts context input and performs relevant probalistic evaluvation checks 
          return json repsonse

          """
          try:
              # read the list of restricted from conf 
              self.restrictedtopics = llmconf[restrictedtopics]
              self.senstivetopics = llmconf[senstivetopics]

              guard = Guard().use_many(

                        RestrictToTopic(
                                        valid_topics=self.restrictedtopics,
                                        disable_classifier=True,
                                        disable_llm=True,
                                        on_fail="exception"
                                      )

                        SensitiveTopic(
                                       sensitive_topics=["politics"],
                                       disable_classifier=False,
                                       disable_llm=False,
                                       on_fail="exception",

                          )
 
              )

              response = guard.validate(contextinp)
              response = json.loads(response.json())
              return response
          except Exception as errmsg:
              logger.error("error while validating probablisticeval")
              return errmsg.args[0]
    
