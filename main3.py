import pfmanager.engine as pm
import pfmanager.currency as cu
from datetime import date


c=cu.Currency(1,"EUR",convert="USD")
print(c)

pf=pm.Portfolio("De Giro")
acc=pm.Account("Cuenta de accciones")
acc.register_portfolio(pf)

pf.register_asset(pm.AssetEquity("Telefónica SA","EUR","TEF.MC"))



tr1 = pm.TransactionBuy(10,cu.Currency(100),cu.Currency(2.5),date_transaction=date(2020,5,3) )

pf.get_asset(symbol="TEF.MC").register_transaction(tr1)


tr2 = pm.TransactionBuy(5,cu.Currency(110),cu.Currency(2.5),date_transaction=date(2020,6,4) )

pf.get_asset(symbol="TEF.MC").register_transaction(tr2)

tr3 = pm.TransactionSell(4,cu.Currency(115),cu.Currency(2.5),date_transaction=date(2021,2,10) )

pf.get_asset(symbol="TEF.MC").register_transaction(tr3)

tr4 = pm.TransactionSell(10,cu.Currency(110),cu.Currency(2.5),date_transaction=date(2021,5,12) )

pf.get_asset(symbol="TEF.MC").register_transaction(tr4)

tr5 = pm.TransactionDividend(cu.Currency(10),taxes=cu.Currency(1.5),date_transaction=date(2021,12,12) )

pf.get_asset(symbol="TEF.MC").register_transaction(tr5)

pm.imprime_portfolio(pf)

