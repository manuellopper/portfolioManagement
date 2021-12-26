# --------------- Global variables

system_local_currency = "EUR"

# --------------- Global functions

def get_sys_local_currency():
  return system_local_currency

def set_sys_local_currency(currency):
  if is_currency_valid(currency):
    system_local_currency = currency
  else:
    return "Error" #### !!!!Hay que establecer cómo se retornan cosas

def is_currency_valid(currency):
  return True

def convert_currency(value, orig_curr, dest_curr):
    #### !!!!Aquí hay que hacer la conversión
  if is_currency_valid(orig_curr) and is_currency_valid(dest_curr):
    return value
  else:
    return "Error"



class Currency:


** CASE 1
Currency(numero)
- value_asset_curr = value_local_curr = número
- asset_curr = local_curr = system_local_currency

** CASE 2
Currency(numero, currency, validate=True/False)
- value_asset_curr = value_local_curr = número
- asset_curr = local_curr = currency -> Es validada o no en función de parámetro "validate"

** CASE 3
Currency(numero1, currency1, convert=currency2, validate=True/False)
- value_asset_curr = numero1
- asset_curr = currency1 -> Es validada o no en función de parámetro "validate"
- local_curr = currency2 -> currency2 puede ser get_sys_local_currency() -> Es validada o no en función de parámetro "validate"
- value_local_curr = conversión de currency1 a currency2 de la unidades de moneda indicadas por numero1

** CASE 4
Curency(numero1, currency1, numero2, validate=True/False)
- value_asset_curr = numero1
- value_local_curr = numero2
- asset_curr = currency1 -> Es validada o no en función de parámetro "validate"
- local_curr = system_local_currency
si system_local_currency == a currency1 pero numero2 es distinto de numero1 entonces error

** CASE 5
Curency(numero1, currency1, numero2, currency2, validate=True/False)
- value_asset_curr = numero1
- asset_curr = currency1 -> Es validada o no en función de parámetro "validate"
- local_curr = currency2 -> Es validada o no en función de parámetro "validate"
- value_local_curr= numero 2


  def __init__(self,value_asset_currency, asset_currency=None, value_local_currency=None, local_currency=None, convert=None, validate=False ):
    
    if not (type(value_asset_currency) == int or type(value_asset_currency) == float):
      return "Error: tipo de la variable pasada no es correcto"
   
    if asset_currency == None and value_local_currency==None and local_currency == None:
      ## CASE 1
      self.value_asset_curr = value_asset_currency
      self.value_local_curr = value_asset_currency
      self.asset_curr = system_local_currency
      self.local_curr = system_local_currency

    elif not(asset_currency == None) and value_local_currency == None and local_currency == None and convert == None:
      ## CASE 2
      if validate == True and not(is_currency_valid(asset_currency)):
        return "Error: la currency no se ha encontrado"
      self.value_asset_curr = value_asset_currency
      self.value_local_curr = value_asset_currency
      self.asset_curr = asset_currency
      self.local_curr = asset_currency
    
    elif not(asset_currency == None) and value_local_currency == None and local_currency == None and not (convert == None) :
      ## CASE 3
      if validate == True and ( not(is_currency_valid(asset_currency)) or not(is_currency_valid(convert) ) ):
        return "Error: la currency no se ha encontrado"
      self.value_asset_curr = value_asset_currency
      self.asset_curr = asset_currency      
      self.local_curr = convert
      self.value_local_curr= convert_currency(value_asset_currency,asset_currency,convert)
    
    elif not(asset_currency == None) and not(value_local_currency) == None and local_currency == None:
      ## CASE 4
      if validate == True and not(is_currency_valid(asset_currency)):
        return "Error: la currency no se ha encontrado"
      if not (type(value_local_currency) == int or type(value_local_currency) == float):
        return "Error: tipo de la variable pasada no es correcto"
      if system_local_currency.upper() == asset_currency.upper() and not(value_asset_currency == value_local_currency):
        return "Error: parametros incoherentes"      
      self.value_asset_curr = value_asset_currency
      self.asset_curr = asset_currency 
      self.value_local_curr = value_asset_currency
      self.local_curr = system_local_currency
    
    elif not(asset_currency == None) and not(value_local_currency) == None and not(local_currency == None):
      ## CASE 5
      if validate == True and ( not(is_currency_valid(asset_currency)) or not(is_currency_valid(local_currency) ) ):
        return "Error: la currency no se ha encontrado"
      if not (type(value_local_currency) == int or type(value_local_currency) == float):
        return "Error: tipo de la variable pasada no es correcto"
      self.value_asset_curr=value_asset_currency
      self.value_local_curr=value_local_currency
      self.asset_curr=asset_currency
      self.local_curr=local_currency
    
    else:
      return "Error: forma no válida de generar el objeto Currency"


  def __add__(self, other):
    if not (self.asset_curr.upper() == other.asset_curr.upper() ) or (self.local_curr.upper() == other.local_curr.upper() ):
      return "Error: las currencies deben coincidir para ser sumadas"
    return Currency(self.asset_curr,self.value_asset_curr + other.get_value("ASSET"),self.local_curr,self.value_local_curr + other.get_value("LOCAL") )
  
  def __sub__(self,other):

    if not (self.asset_curr.upper() == other.asset_curr.upper() ) or (self.local_curr.upper() == other.local_curr.upper() ):
      return "Error: las currencies deben coincidir para ser sumadas"
      
    return Currency(self.asset_curr,self.value_asset_curr - other.get_value("ASSET"),self.local_curr,self.value_local_curr - other.get_value("LOCAL") )

  def __mul__(self, other):
    num_type = type(other)
    if not (num_type == int or num_type == float or num_type == Currency):
      return "Error"
    elif num_type == int or num_type == float:
      return Currency(self.asset_curr,self.value_asset_curr * other,self.local_curr,self.value_local_curr * other )
    elif num_type == Currency:
      return Currency(self.asset_curr,self.value_asset_curr * other.get_value("ASSET"),self.local_curr,self.value_local_curr * other.get_value("LOCAL") )
    else:
      return "Error"

  def __rmul__(self, other):
    num_type = type(other)
    if not (num_type == int or num_type == float):
      return "Error"
    else:      
      return Currency(self.asset_curr,self.value_asset_curr * other,self.local_curr,self.value_local_curr * other )

  def __str__ (self):
    string_aux = str(self.value_asset_curr) + " " + self.asset_curr
    if not(self.asset_curr.upper() == self.local_curr.upper()):
      string_aux = string_aux + " / " + str(self.value_local_curr) + " " + self.local_curr    
    return string_aux
      
  def set_value (self, value, currency =None):    

    if not (type(value)== int or type(value)== float):
      return "Error: el valor debe ser un numero"
      
    if currency == None and self.local_curr.upper() == self.asset_curr.upper():
      self.value_local_curr = value
      self.value_asset_curr = value
    elif currency.upper()=="ASSET":
      self.value_asset_curr = value
    elif currency.upper()=="LOCAL":
      self.value_local_curr = value
    else:
      return "Error: argumentos no válidos" #### !!!!Hay que establecer cómo se retornan cosas

  def get_value (self, currency =None):    

    if currency == None and self.local_curr.upper() == self.asset_curr.upper():
      return self.value_asset_curr
    elif currency.upper()=="ASSET":
      return self.value_asset_curr
    elif currency.upper()=="LOCAL":
      return self.value_local_curr
    else:
      return "Error: argumentos no válidos" #### !!!!Hay que establecer cómo se retornan cosas

  def get_currency (self, currency =None):
    if currency == None and self.local_curr.upper() == self.asset_curr.upper():
      return self.asset_curr
    if currency.upper()=="ASSET":
      return self.asset_curr
    elif currency.upper()=="LOCAL":
      return self.local_curr
    else:
      return "Error: argumentos no válidos" #### !!!!Hay que establecer cómo se retornan cosas

