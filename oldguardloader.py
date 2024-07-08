from typing import Optional
from transformers import AutoModelForCausalLM, AutoTokenizer
from helperutil import read_yaml_conf,intializelogger
from prompttemplate import guardpromptbuilder
import torch
import os,json,sys
import logging 


class guardloader():


  def __init__(self,configfile, modelname:str, modelgenericconf:dict, logger) -> None:

    self.llmconf = read_yaml_conf(configfile)
    self.modelname = modelname
    self.modelgenericconf = modelgenericconf
    self.logger = logger


  def modelintializer(self):
      model = AutoModelForCausalLM.from_pretrained(self.modelname,
                                                      torch_dtype=torch.float16,
                                                      device_map="cuda",
                                                      trust_remote_code=False)
      tokenizer = AutoTokenizer.from_pretrained(self.modelname,use_fast=True)
      return model, tokenizer
    
  def generate_promptresponse(self,prompt):
      try:
          model, tokenizer = self.modelintializer()
          text_target = guardpromptbuilder(modelname=self.modelname,prompt=prompt)

          input_ids = tokenizer(text_target=text_target, return_tensors='pt').input_ids.cuda()
          output = model.generate(inputs=input_ids,
                                  temperature=self.modelgenericconf['temperature'],
                                  do_sample=self.modelgenericconf['do_sample'],
                                  max_new_tokens=self.modelgenericconf['max_new_tokens'], 
                                  pad_token_id=0)
          prompt_len = input_ids.shape[-1]
          self.logger.info(f"detected prompt length of {prompt_len}")
          response=tokenizer.decode(output[0][prompt_len:],skip_special_tokens=True)
          return response

      
      except Exception as e:
          self.logger.error(f"encountered issue while processing prompt: {e}")
          sys.exit(1)

