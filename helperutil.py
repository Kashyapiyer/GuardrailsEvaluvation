import logging
import yaml 

def read_yaml_conf(configfile,key=None):
    try:
      with open(configfile, "r") as f: 
        config = yaml.safe_load(f)
      if key is None:
         return config
      else:
         return config[key]
    except Exception as e:
      raise Exception("Encountered issue while processsing {e}") 
    
def read_txt(inputfile):
    with open(inputfile, 'r') as file:
        content = ''.join(line.strip() for line in file.readlines())
    return content

def intializelogger():
    """
    Intializing basic logic 
    """
    logging.basicConfig(
     filename='log_file_name'+'%Y-%m-%d %H:%M:%S'+'.log',
     level=logging.INFO, 
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt="%Y-%m-%d %H:%M:%S"
     )
    logger = logging.getLogger()
    return logger 

def get_prmptresponse(guardloader,prompt):
    try:
        response = guardloader.generate_promptresponse(prompt)        
        violatedmap = {'1': 'Violence and Hate', 
                       '2': 'Sexual Content', 
                       '3': 'Criminal Planning', 
                       '4': 'Guns and Illegal Weapons', 
                       '5': 'Regulated or Controlled Substances', 
                       '6': 'Self-Harm'
        }
        rspjson={}
        if len(response.splitlines()) > 1:
           violationno = response.split("\n")[1].strip()
           rspjson['safetyeval'] = response.split("\n")[0]
           rspjson['Violatedcategory'] =  violatedmap[violationno]
           rspjson['inputquery'] = prompt
           return rspjson
        else: 
           #print("######from else block########")
           rspjson['safetyeval'] = response
           rspjson['Violatedcategory'] = 'NoViolation'
           rspjson['inputquery'] = prompt
           return rspjson

    except Exception as e:
        print(f'Encountered issue while processing{e}')
      

def importclass(modulename, classname):
    module = __import__(modulename, fromlist=[classname])
    clsobj = getattr(module, classname)
    return clsobj
