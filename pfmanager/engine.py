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

  def add_asset(self, asset_aux, copy_transactions=True):
    
    asset_type = asset_aux.get_asset_type()
    
    if asset_type == "Equity":
      if self.asset_exist(symbol=asset_aux.get_symbol()):
        return "Error: ya existe" ## esto se puede transformar en una fusión.
      else:
        self.assets_list.append(asset_aux)
        asset_aux.set_portfolio(self)
        if copy_transactions == True:
          self.copy_transactions_from_asset(self,asset_aux)
        
  def copy_transactions_from_asset(self, asset_aux):
    self.transactions_list += asset_aux.get_transactions(copy=True)
    ## !! Aquí habría que ordena la lista de transacciones.. por fecha, por ejemplo






class Asset:
  seed_id = [0]
  asset_type="Undertermined"
  
  def __init__(self, name, currency, pf_father=None):
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

  def get_portfolio(self):
    return self.porfolio

  def set_portfolio(self, portfolio):
    if not (type(portfolio) == Portfolio):
      return "Error"
    else:
      self.portfolio=portfolio
  
  def get_transactions(self, start = 0, end = len(self.transactions_list), copy = False):
    
    if copy == True:
      return self.transactions_list[start:end].copy()
    else:
      return self.transactions_list[start:end]

     


    
class AssetEquity(Asset):

  def __init__(self, name, currency, symbol, pf_father=None, sector=None,market_type=None, size=None, caract=None,add_to_porfolio = True):
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
    if add_to_porfolio == True and not(pf_father == None) :
      self.portfolio.add_asset(self)


  def get_symbol(self):
    return self.symbol

  def buy(self):
    pass

  

    
class Transaction:
  seed_id = [0]
  def __init__(self, asset_currency=system_local_currency,local_currency = system_local_currency,asset_father=None):
    self.set_new_id()
    self.asset_currency=asset_currency
    self.local_currency=local_currency
    self.taxes = Currency(self.asset_currency,0,self.local_currency,0)
    self.commissions = Currency(self.asset_currency,0,self.local_currency,0)
    self.gross_cashflow = Currency(self.asset_currency,0,self.local_currency,0)
    self.net_cashflow = Currency(self.asset_currency,0,self.local_currency,0)

  def set_new_id(self):     
    self.id=int(self.seed_id[0])+1
    self.seed_id[0]=self.id

  def get_id(self):
    return self.id

  def set_asset(self, )
    
class TransactionBuy(Transaction):
  def __init__(self, number, price_per_share, commissions=0, taxes=0, asset_father=None):
    
    if (not( type(price_per_share) == Currency)) or (not(commissions == None) and not(type(commissions) == Currency)) or (not(taxes == None) and not(type(taxes) == Currency)):
      return "Error"

    super().__init__(price_per_share.get_currency("ASSET"),price_per_share.get_currency("LOCAL"))
    self.number_of_shares = number
    self.price_per_share=price_per_share
    
    if not( commissions == 0 ):
      self.commissions = commissions
    
    if not( taxes == 0 ):
      self.taxes = taxes
    
    self.gross_cashflow = (-number) * price_per_share
    self.net_cashflow = self.gross_cashflow - self.commissions - self.taxes

    ######### Actualizar gross cash flow y net cash flow

    
    
class TransactionSell(Transaction):
  def __init__(self):
    self.set_new_id()
    
class TransactionDividend(Transaction):
  def __init__(self):
    self.set_new_id()
      
class TransactionDividendWithShares(Transaction):
  def __init__(self):
    self.set_new_id()
  
