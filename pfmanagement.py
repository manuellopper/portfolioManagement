class Portfolio:
  def __init__(self,name):
    self.pf_name=name

class Asset:
  def __init__(self):
    self.dummie=0
    
class AssetEquity(Asset):
  def __init__(self):
    self.dummie=0
    
class Transaction:
  def __init__(self):
    self.dummie=0
    
class TransactionBuyEquity(Transaction):
  def __init__(self):
    self.dummie=0
    
class TransactionSellEquity(Transaction):
  def __init__(self):
    self.dummie=0
    
class TransactionDividendEquity(Transaction):
  def __init__(self):
    self.dummie=0
      
class TransactionDividendWithSharesEquity(Transaction):
  def __init__(self):
    self.dummie=0
  
