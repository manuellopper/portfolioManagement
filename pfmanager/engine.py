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

# ---------------- Classes

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
      else:
        return "Error" #### !!!!Hay que establecer cómo se retornan cosas
      
      self.value_local_curr= self.convert(value_asset_currency,asset_currency,local_currency) 

  def convert(self,value_asset_currency, asset_currency, local_currency):
    #### !!!!Aquí hay que hacer la conversión
    return value_asset_currency

  def setValue (self, value, currency ="ASSET"):    
    if currency.upper()=="ASSET":
      self.value_asset_curr = value
    elif currency.upper()=="LOCAL":
      self.value_local_curr = value
    else:
      return "Error" #### !!!!Hay que establecer cómo se retornan cosas

  def getValue (self, value, currency ="ASSET"):    
    if currency.upper()=="ASSET":
      return self.value_asset_curr
    elif currency.upper()=="LOCAL":
      return self.value_local_curr
    else:
      return "Error" #### !!!!Hay que establecer cómo se retornan cosas



class Portfolio:
  def __init__(self,name):
    self.pf_name=name
    self.assets_list=[]
    self.transactions_list=[]

  def asset_exist(self, symbol=None):
    for i in range(len(self.assets_list)):
      if self.assets_list[i].get_symbol().upper() == symbol.upper():
        return True    
    return False

  def add_asset_to_porfolio(self, asset_aux):
    asset_type = asset_aux.get_asset_type()
    
    if asset_type == "Equity":
      if self.asset_exist(symbol=asset_aux.get_symbol()):
        return "Error: ya existe"
      else:
        self.assets_list.append(asset_aux)





class Asset:
  seed_id = [0]
  asset_type="Undertermined"
  
  def __init__(self, name, currency, pf_father):
    self.set_new_id()
    self.asset_name=name    
    self.portfolio = pf_father
    self.transactions_list=[]
    if is_currency_valid(currency):
      self.currency=currency
    else:
      return "Error" #### !!!!Hay que establecer cómo se retornan cosas
     
     
  def set_new_id(self):     
    self.id=int(self.seed_id[0])+1
    self.seed_id[0]=self.id
  
  def get_id(self):
    return self.id

  def get_asset_type(self):
    return self.asset_type


    
class AssetEquity(Asset):

  def __init__(self, name, currency, symbol, pf_father, sector=None,market_type=None, size=None, caract=None,add_to_porfolio = False):
    # Main information
    super().__init__(name,currency,pf_father)  
    self.asset_type="Equity"
    self.symbol = symbol
    #Asset general information
    self.sector=sector
    self.market_type=market_type
    self.size=size
    self.caract=caract
    #Asset internal KPI
    self.curr_shares = 0
    self.market_value = Currency(currency,0,system_local_currency,0)
    self.curr_cost= Currency(currency,0,system_local_currency,0)    
    self.total_dividends = Currency(currency,0,system_local_currency,0)
    self.total_taxes= Currency(currency,0,system_local_currency,0)
    self.total_commissions = Currency(currency,0,system_local_currency,0)
    #Auxiliar variables
    self.total_buy_shares =0
    self.total_sell_shares =0 
    self.total_buy_cost = Currency(currency,0,system_local_currency,0)
    self.total_sell_rev = Currency(currency,0,system_local_currency,0)

    ##Add to porfolio if indicated
    if add_to_porfolio == True:
      self.portfolio.add_asset_to_porfolio(self)


  def get_symbol(self):
    return self.symbol

  

    
class Transaction:
  seed_id = [0]
  def __init__(self):
    self.set_new_id()

  def set_new_id(self):     
    self.id=int(self.seed_id[0])+1
    self.seed_id[0]=self.id

  def get_id(self):
    return self.id
    
class TransactionBuyEquity(Transaction):
  def __init__(self):
    self.set_new_id()
    
class TransactionSellEquity(Transaction):
  def __init__(self):
    self.set_new_id()
    
class TransactionDividendEquity(Transaction):
  def __init__(self):
    self.set_new_id()
      
class TransactionDividendWithSharesEquity(Transaction):
  def __init__(self):
    self.set_new_id()
  
