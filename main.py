# Import Required Modules
try:
  import hunspell
  import sys 
  from flask import Flask,request,json,jsonify
  from flask_restful import Resource,Api
  from flask_restful import reqparse
  from spellchecker import SpellChecker
except Exception as e:
  print("Module Missing {}".format(e))


app = Flask(__name__)
api = Api(app) 
parser = reqparse.RequestParser()
parser.add_argument('language', type=str,required = False)
parser.add_argument('word', type=str,required = True,help='please enter the word')

#Path For Dictonaries.
langMap = { 
  'en': hunspell.HunSpell('./english/assets_dicts_en_GB.dic',
                                './english/assets_dicts_en_GB.aff'), 
  'fr': hunspell.HunSpell('./french/fr-classique-reforme1990.dic',
                                   './french/fr-classique-reforme1990.aff'), 
  'it': hunspell.HunSpell('./italian/it_IT.dic',
                                './italian/it_IT.aff')
          }

class myapi(Resource):
  def __init__(self):
    self.__lang = parser.parse_args().get('language')
    self.__word = parser.parse_args().get('word')
  
#   Spellchecking Using GET method
  def get(self):  
    if self.__lang == None:
      self.__lang = 'en'
    spell = SpellChecker()
    if langMap.get(self.__lang) == None: 
       return "Can't found {} language".format(self.__lang)  
    lambda self : langMap.get()(self.__lang)
    return {"lang": self.__lang,"correctword":spell.correction(self.__word),"words":langMap.get(self.__lang).suggest(self.__word)} 

#   Spellchecking Using POST method
  def post(self):
    data = request.get_json()
    self.__word = data['word']
    if data.get('lang'):
      self.__lang = data.get('lang')
    else:
      self.__lang = 'en'
    spell = SpellChecker()  
    if(langMap.get(self.__lang) == None): 
        return "Can't found {} language".format(self.__lang) 
    return jsonify({'lang':self.__lang,'correct':spell.correction(self.__word),'word':langMap.get(self.__lang).suggest(self.__word)})

api.add_resource(myapi,'/',methods = ['GET','POST'])


if __name__ == "__main__":
#   You can change Debug mode and port here
    app.run(debug=True,port=5050)

