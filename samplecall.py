def get_llmapi_model(api_endpoint, modelname, headers):
    try:

      url = api_endpoint+ "&modelname=" + modelname
      response = requests.get(api_endpoint, headers=headers)

      if response.status_code == 200:
          rspobj = response.json() 
          model = rspobj['model'] 
          tokenizer = rspobj['tokenizer']
          return model, tokenizer
      else:
          self.logger.error("Err status code:", response.status_code)

    except Exception as e:
      print(f"Encountered error while processing: {str(e)}") 
