class Currency:
  def __init__(self,asset_currency,local_currency):
    self.dummie=[]


class Portfolio:
  def __init__(self,name):
    self.pf_name=name
    self.assets_list=[]
    self.transactions_list=[]


class Asset:
  seed_id = [0]
  asset_type="Undertermined"
  
  def __init__(self,name,currency,pf_father):
    self.set_new_id()
    self.asset_name=name
    self.currency=currency
    self.portfolio = pf_father
    self.transactions_list=[]
    #Hay que añadir un argumento que sirva para indicar si se quiere o no que se actualice la lista de activos del porfolio pasado 
    
  def set_new_id(self):     
    self.id=int(self.seed_id[0])+1
    self.seed_id[0]=self.id
  
  def get_id(self):
    return self.id


    
class AssetEquity(Asset):

  def __init__(self, name, currency, symbol, pf_father, sector=None,market_type=None, size=None, caract=None):
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
    self.market_value = {currency : 0}
    self.curr_cost= {currency : 0 }    
    self.total_dividends = {currency : 0}
    self.total_taxes= {currency : 0}
    self.total_commissions = {currency : 0}
    #Auxiliar variables
    self.total_buy_shares =0
    self.total_sell_shares =0 
    self.total_buy_cost = {currency : 0}
    self.total_sell_rev = {currency : 0}

  

    
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
  
