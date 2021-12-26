from datetime import datetime
from datetime import date

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



class Portfolio:
  def __init__(self,name):
    self.pf_name=name
    self.assets_list=[]
    self.transactions_list=[]

  def asset_exist(self, symbol=None, id=None):

    if symbol == None and id == None:
     return "Error: se debe indicar un identificador del activo (id o símbolo)"
    elif not(symbol == None) and not(id == None):
      return "Error: se debe indicar sólo uno de los parámetros symbol o id. No está permitido los dos"
    elif not(symbol == None):      
      for asset_aux in self.assets_list:
        if asset_aux.get_symbol().upper() == symbol.upper():
          return True, asset_aux   
      return False, None
    else:
      for asset_aux in self.assets_list:
        if asset_aux.get_id() == id:
          return True , asset_aux   
      return False, None

  def register_asset(self, asset_aux, copy_transactions=True):
    
    asset_type = asset_aux.get_asset_type()

    if asset_type == "Equity":
      response, r_asset = self.asset_exist(symbol=asset_aux.get_symbol())
      if response:        
        return "Error: ya existe" ## esto se puede transformar en una fusión.
      else:        
        self.assets_list.append(asset_aux)
        asset_aux.set_portfolio(self)
        if copy_transactions == True:
          self.copy_transactions_from_asset(asset_aux)
        
  def copy_transactions_from_asset(self, asset_aux):
    
    self.transactions_list.extend(asset_aux.get_transactions(copy=True))   
    self.transactions_list.sort(key=self.get_transaction_date)
    
  def register_transaction(self, transaction_aux):
    
    transaction_aux.set_portfolio(self)
    self.transactions_list.append(transaction_aux)
    if transaction_aux.get_date() < self.transactions_list[len(self.transactions_list)-1].get_date():      
      self.transactions_list.sort(key=self.get_transaction_date)  

  def get_transaction_date(self, trans): return trans.get_date()

  def get_asset(self, symbol=None, id=None):
    if symbol == None and id == None:
     return "Error: se debe indicar un identificador del activo (id o símbolo)"
    elif not(symbol == None) and not(id == None):
      return "Error: se debe indicar sólo uno de los parámetros symbol o id. No está permitido los dos"
    elif not(symbol == None):
      result, asset = self.asset_exist(symbol=symbol)
      return asset
    else:
      result, asset = self.asset_exist(id=id)
      return asset
      



class Asset:
  
  asset_type="Undertermined"
  
  def __init__(self, name, currency):
    self.set_new_id()
    self.asset_name=name    
    self.transactions_list=[]
    self.portfolio = None
    if is_currency_valid(currency):
      self.currency=currency
    else:
      return "Error" #### !!!!Hay que establecer cómo se retornan cosas
       
  def set_new_id(self): self.id=datetime.timestamp(datetime.now())    
  
  def get_id(self): return self.id

  def get_asset_type(self): return self.asset_type

  def get_portfolio(self): return self.portfolio

  def set_portfolio(self, portfolio):
    if not (type(portfolio) == Portfolio):
      return "Error"
    else:
      self.portfolio=portfolio
  
  def get_transactions(self, start = 0, end = 0, id = None, copy = False):
    

    if not(id == None) and type(id) == float:
      for trans in self.transactions_list:
        if trans.get_id() == id:
          return trans

    if end == 0:
      end = len(self.transactions_list)

    if copy == True:
      return self.transactions_list[start:end].copy()
    else:
      return self.transactions_list[start:end]
   
  def get_transaction_date(self,trans): return trans.get_date()

   
class AssetEquity(Asset):

  def __init__(self, name, currency, symbol, sector=None,market_type=None, size=None, caract=None):
    # Main information
    super().__init__(name,currency)  
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

  def get_symbol(self): return self.symbol

  def register_transaction(self, transaction_aux, add_to_porfolio = True):
    
    print("registrando transacción")
    type_arg= type(transaction_aux)
    if not (type_arg == TransactionBuy or type_arg == TransactionSell or type_arg== TransactionDividend or type_arg == TransactionSharesAsDividend):
      return "Error: tipo pasado no es correcto"
    
    id = transaction_aux.get_id()
    transaction_aux.set_asset(self)
    self.transactions_list.append(transaction_aux)
    self.transactions_list.sort(key=self.get_transaction_date)  
    
    if type(transaction_aux) == TransactionBuy:
      number = transaction_aux.get_number()
      self.curr_shares += number
      self.total_buy_shares += number      
      self.total_buy_cost = self.total_buy_cost + number * transaction_aux.get_price_per_share()
      self.process_buy_sell_transactions()
    elif type(transaction_aux) == TransactionSell:
      number = transaction_aux.get_number()
      self.curr_shares -= number
      self.total_sell_shares += number    
      self.total_sell_rev = self.total_sell_rev + number * transaction_aux.get_rev_per_share()
      self.process_buy_sell_transactions()
    elif type(transaction_aux) == TransactionDividend:
      self.total_dividends += transaction_aux.get_dividends()
    else:
      self.curr_shares += number
      self.total_buy_shares += number      
      self.total_buy_cost = self.total_buy_cost + number * transaction_aux.get_price_per_share()
      self.process_buy_sell_transactions()
      
    self.total_taxes = self.total_taxes + transaction_aux.get_taxes() 
    self.total_commissions = self.total_commissions + transaction_aux.get_commissions()
    
    if add_to_porfolio == True and not(self.portfolio == None):
      self.portfolio.register_transaction(self.get_transactions(id=id)) 
  
  def get_current_shares(self): return self.curr_shares

  def process_buy_sell_transactions(self):
    buy_list = [ transaction for transaction in self.transactions_list if ( type(transaction)==TransactionBuy or type(transaction)==TransactionSharesAsDividend )]
    sell_list = [ transaction for transaction in self.transactions_list if type(transaction)==TransactionSell ]
  
    self.curr_cost = Currency(self.currency,0,system_local_currency,0)
    
    for buy_oper in buy_list:
      buy_oper.set_buy_closed(0) #primero borro las variables buy_closed de todas las operacoines buy
      self.curr_cost = self.curr_cost + buy_oper.get_price_per_share() * buy_oper.get_number()
    
  
    for sell_oper in sell_list:
      num_sell = sell_oper.get_number()
      remaining_sell = num_sell
      underlying_cost = Currency(self.currency,0,system_local_currency,0)
      for buy_oper in buy_list:        
        remaining_buy=buy_oper.get_number() - buy_oper.get_buy_closed() 
        if remaining_sell >= remaining_buy:          
          buy_oper.set_buy_closed(buy_oper.get_number())      
          
          underlying_cost += buy_oper.get_price_per_share() * remaining_buy
          remaining_sell -= remaining_buy
          buy_list.remove(buy_oper)
          continue
        elif remaining_sell < remaining_buy:          
          buy_oper.set_buy_closed(buy_oper.get_buy_closed() + remaining_sell)            
          underlying_cost += buy_oper.get_price_per_share() * remaining_sell
          remaining_sell = 0
          break
        
      if remaining_sell > 0:
        return "Error: se está intentando vender más de las acciones en posesión"
      
      sell_oper.set_underlying_cost(underlying_cost)
      sell_oper.set_operation_benefit(sell_oper.get_rev_per_share()*sell_oper.get_number()-underlying_cost)
      self.curr_cost = self.curr_cost - underlying_cost

  
class Transaction:
  
  transaction_type="Undefined"

  def __init__(self, asset_currency=system_local_currency,local_currency = system_local_currency, date_transaction = date.today()):
        
    self.set_new_id()
    self.asset_currency=asset_currency
    self.local_currency=local_currency
    self.portfolio_father = None
    self.asset_father = None
    self.date = date_transaction
    self.taxes = Currency(self.asset_currency,0,self.local_currency,0)
    self.commissions = Currency(self.asset_currency,0,self.local_currency,0)
    self.gross_cashflow = Currency(self.asset_currency,0,self.local_currency,0)
    self.net_cashflow = Currency(self.asset_currency,0,self.local_currency,0)    
    
  def set_new_id(self): self.id=datetime.timestamp(datetime.now())

  def get_id(self): return self.id

  def set_asset(self, asset_aux):
    ## comprobar si es algún tipo de asset.. es decir si el typo es hijo de Asset
    self.asset_father=asset_aux

  def get_commissions(self): return self.commissions

  def get_taxes(self): return self.taxes

  def get_date(self): return self.date

  def set_portfolio(self, pf): self.portfolio_father = pf 


   
class TransactionBuy(Transaction):
  
  transaction_type="BUY"
  
  def __init__(self, number, price_per_share, commissions=0, taxes=0, date_transaction = date.today()):
    
    if (not( type(price_per_share) == Currency)) or (not(commissions == 0) and not(type(commissions) == Currency)) or (not(taxes == 0) and not(type(taxes) == Currency)):
      return "Error"

    super().__init__(price_per_share.get_currency("ASSET"),price_per_share.get_currency("LOCAL"), date_transaction)
    self.number_of_shares = number
    self.price_per_share=price_per_share
    self.buy_closed=0

    if not( commissions == 0 ):
      self.commissions = commissions
    
    if not( taxes == 0 ):
      self.taxes = taxes
    
    self.gross_cashflow = (-number) * price_per_share
    self.net_cashflow = self.gross_cashflow - self.commissions - self.taxes
  
  def get_number(self): return self.number_of_shares

  def get_price_per_share(self): return self.price_per_share

  def get_buy_closed(self): return self.buy_closed

  def set_buy_closed(self,number_closed):
    if not(type(number_closed) == int):
      return "Error"
    
    self.buy_closed = number_closed

  
class TransactionSell(Transaction):

  transaction_type="SELL"

  def __init__(self, number, rev_per_share, commissions=0, taxes=0, date_transaction = date.today()):
    
    if (not( type(rev_per_share) == Currency)) or (not(commissions == 0) and not(type(commissions) == Currency)) or (not(taxes == 0) and not(type(taxes) == Currency)):
      return "Error"

    super().__init__(rev_per_share.get_currency("ASSET"),rev_per_share.get_currency("LOCAL"), date_transaction)

   
    self.number_of_shares = number
    self.underlying_cost = None # El coste subyacente se establece cuando se registra la operación
    self.rev_per_share=rev_per_share
    self.operation_benefit = None  # El beneficio se establece cuando se registra la operación
    
    if not( commissions == 0 ):
      self.commissions = commissions
    
    if not( taxes == 0 ):
      self.taxes = taxes
    self.gross_cashflow = number * rev_per_share
    self.net_cashflow = self.gross_cashflow - self.commissions - self.taxes

  def get_number(self): return self.number_of_shares

  def get_rev_per_share(self): return self.rev_per_share

  def set_operation_benefit(self, benefit):
    if not(type(benefit)==Currency):
      return "Error"
    
    self.operation_benefit=benefit
  
  def get_number(self): return self.number_of_shares

  def set_underlying_cost(self, uc): 
    if not(type(uc)==Currency):
      return "Error"
    
    self.underlying_cost=uc

    
class TransactionDividend(Transaction):

  transaction_type="DIVIDENDS"

  def __init__(self, dividends, commissions=0, taxes=0, date_transaction = date.today()):
    
    if (not( type(dividends) == Currency)) or (not(commissions == 0) and not(type(commissions) == Currency)) or (not(taxes == 0) and not(type(taxes) == Currency)):
      return "Error"

    super().__init__(dividends.get_currency("ASSET"),dividends.get_currency("LOCAL"),date_transaction)

    self.dividends=dividends
    
    if not( commissions == 0 ):
      self.commissions = commissions
    
    if not( taxes == 0 ):
      self.taxes = taxes
    
    self.gross_cashflow = dividends
    self.net_cashflow = self.gross_cashflow - self.commissions - self.taxes

  def get_dividends(self): return self.dividends
    
      
class TransactionSharesAsDividend(Transaction):

  transaction_type="SHARES AS DIVIDENDS"

  def __init__(self, number, price_per_share, commissions=0, taxes=0, date_transaction = date.today()):
    
    if (not( type(price_per_share) == Currency)) or (not(commissions == 0) and not(type(commissions) == Currency)) or (not(taxes == 0) and not(type(taxes) == Currency)):
      return "Error"

    super().__init__(price_per_share.get_currency("ASSET"),price_per_share.get_currency("LOCAL"), date_transaction)
    self.number_of_shares = number
    self.price_per_share=price_per_share
    self.buy_closed=0
    
    if not( commissions == 0 ):
      self.commissions = commissions
    
    if not( taxes == 0 ):
      self.taxes = taxes
    
    self.gross_cashflow = (-number) * price_per_share
    self.net_cashflow = self.gross_cashflow - self.commissions - self.taxes
  
  def get_number(self): return self.number_of_shares

  def get_price_per_share(self): return self.price_per_share

  def get_buy_closed(self): return self.buy_closed

  def set_buy_closed(self,number_closed):
    if not(number_closed == int):
      return "Error"
    
    self.buy_closed = number_closed
  
