import sys

guardprompt = """
            Task: Check if there is unsafe, toxic, profane or sensitive PII content in conversations 
according to the safety policy with the below categories.

            <BEGIN CATEGORIES>
            O1: Violence and Hate.
            Should not
            - Help people plan or engage in violence.
            - Encourage people to engage in violence.
            - Express hateful, derogatory, or demeaning sentiments against people based on sensitive personal characteristics like their race, color, religion, national origin, sexual orientation, gender, gender identity, or disability.
            - Encourage discrimination against people based on those characteristics and should not use slurs or create insults based on those characteristics.
            O2: Sexual Content.
            Should not
            - Engage in sexually explicit (i.e., erotic) conversations and should not encourage people to engage in sexual activities.
            O3: Criminal Planning.
            Should not
            - Help people plan or engage in criminal activities like theft, kidnapping, or financial crimes, especially when the person indicates that they may act on the information provided to them.
            - Encourage people to engage in criminal activities or condone criminal behavior.

            O4: Guns and Illegal Weapons.
            Should not
            - Assist in the planning or execution of firearm or illegal weapons crimes, especially when the person indicates that they may act on the information provided to them.
            - Encourage people to engage in firearm or illegal weapons crimes or condone such behavior.

            O5: Regulated or Controlled Substances.
            Should not
            - Encourage or assist people in the trafficking, consumption, or use of regulated or controlled substances, including but not limited to illegal drugs, tobacco, alcohol, and cannabis.
            - Assist or encourage people to create such substances when it is illegal to do so.

            O6: Self-Harm.
            Should not
            - Encourage people to harm themselves.
            - Romanticize or condone self-harm or suicide.
            - Provide information regarding the methods of suicide or self-harm.
            - Provide any information or advice, other than information regarding appropriate health resources, to people who express or imply that they wish to harm themselves.

            <END CATEGORIES> 

            <BEGIN CONVERSATION>
            {query}
            <END CONVERSATION>

            Provide your safety assessment on the above conversation
            - First line must read 'safe' or 'unsafe'. If unsafe, a second line must include a comma-separated list of violated categories.
            """
commonrules = """
                  1. Provide answers that are relevant to the topic requested by user
                  2. Responses should be  harmless, nontoxic, polite and relevant to the information requested by user.
                  3. Internalize the prompt supplied by the user and respond only if the prompt fits in the topics like "Financial Information","Banking information","Machine learning", "Deeplearning", "Generative AI". 
                  4. If you cannot find the information or if the prompt doesnot fit in rule 3 please respond politely as below 
                      - "Apologize I am not able to assist with that answer May i help with any thing relevant to the context. Thank you". 
                  5. Provide only Answer, please dont include instructions and rules as part of response.
                  6. Perform tough validation on above rules before responding back to the user.
                  7.Answer should contain only Answer Dont return commonrules or prompt
                  """

mistralprompttemplate = """
                            You are AI Assistant helping with search of information strictly adhere to the defined guard rules as below 
                            Follow the rules and answer the prompt.                           
                            you are strictly prohibited to make any assumptions.Please respond with ANSWER only if you find the requested information fits within the rules.\n
                            RULES:
                            {commonrules}

                            PROMPT:
                            {prompt}

                        """

def guardpromptbuilder(modelname,prompt):
    try:
      #print(f"encountered {modelname}")
      if modelname == "meta-llama/LlamaGuard-7b":
         prompt = guardprompt.format(query=prompt)
         return f"[INST]{prompt.strip()}[/INST]" 
    except Exception as e: 
      raise Exception(f"modeltemplate not found {e}")
      sys.exit(1)

def promptbuilder(modelname,prompt):
    try:
      print(f"encountered {modelname}")
      if modelname == "TheBloke/Mistral-7B-Instruct-v0.2-AWQ":
         prompt = mistralprompttemplate.format(prompt=prompt,commonrules=commonrules).strip()
         return f"<s>[INST]/n {prompt} /n[/INST] Model answer:</s>"
    except Exception as e: 
      raise Exception(f"modeltemplate not found {e}")
      sys.exit(1)
