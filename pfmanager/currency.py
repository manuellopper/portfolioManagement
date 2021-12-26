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
  def __init__(self,asset_currency,value_asset_currency, local_currency=None, value_local_currency=None ):
    
    if is_currency_valid(asset_currency):      
      self.asset_curr=asset_currency       
    else:
      return "Error" #### !!!!Hay que establecer cómo se retornan cosas
    
    self.value_asset_curr = value_asset_currency

    if local_currency == None and value_local_currency == None:
      ## La moneda local es igual que la del activo
      self.local_curr = asset_currency
      self.value_local_curr = value_asset_currency
    elif not (local_currency == None) and value_local_currency == None:
      if is_currency_valid(local_currency):    
        self.local_curr = local_currency
        self.value_local_curr= convert_currency(value_asset_currency,asset_currency,local_currency)
      else:
        return "Error" #### !!!!Hay que establecer cómo se retornan cosas
    else:
      if is_currency_valid(local_currency):    
        self.local_curr = local_currency
        self.value_local_curr= value_local_currency
      else:
        return "Error" #### !!!!Hay que establecer cómo se retornan cosas    

  def __add__(self, other):
    return Currency(self.asset_curr,self.value_asset_curr + other.get_value("ASSET"),self.local_curr,self.value_local_curr + other.get_value("LOCAL") )
  
  def __sub__(self,other):
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
    string_aux = self.asset_curr + ": " + str(self.value_asset_curr) +" / " + self.local_curr + ": "+ str(self.value_local_curr)
    return string_aux
      
  def set_value (self, value, currency ="ASSET"):    
    if currency.upper()=="ASSET":
      self.value_asset_curr = value
    elif currency.upper()=="LOCAL":
      self.value_local_curr = value
    else:
      return "Error" #### !!!!Hay que establecer cómo se retornan cosas

  def get_value (self, currency ="ASSET"):    
    if currency.upper()=="ASSET":
      return self.value_asset_curr
    elif currency.upper()=="LOCAL":
      return self.value_local_curr
    else:
      return "Error" #### !!!!Hay que establecer cómo se retornan cosas

  def get_currency (self, currency ="ASSET"):
    if currency.upper()=="ASSET":
      return self.asset_curr
    elif currency.upper()=="LOCAL":
      return self.local_curr
    else:
      return "Error" #### !!!!Hay que establecer cómo se retornan cosas

