import pfmanager.engine as pm
from datetime import date

pf=pm.Portfolio("De Giro")
pf.register_asset(pm.AssetEquity("Telefónica SA","EUR","TEF"))


tr1 = pm.TransactionBuy(10,pm.Currency("EUR",100),pm.Currency("EUR",2.5),date_transaction=date(2020,5,3) )

pf.get_asset(symbol="TEF").register_transaction(tr1)


tr2 = pm.TransactionBuy(5,pm.Currency("EUR",110),pm.Currency("EUR",2.5),date_transaction=date(2020,6,4) )

pf.get_asset(symbol="TEF").register_transaction(tr2)

tr3 = pm.TransactionSell(4,pm.Currency("EUR",115),pm.Currency("EUR",2.5),date_transaction=date(2021,2,10) )

pf.get_asset(symbol="TEF").register_transaction(tr3)

tr4 = pm.TransactionSell(10,pm.Currency("EUR",110),pm.Currency("EUR",2.5),date_transaction=date(2021,5,12) )

pf.get_asset(symbol="TEF").register_transaction(tr4)

tr5 = pm.TransactionDividend(pm.Currency("EUR",10),taxes=pm.Currency("EUR",1.5),date_transaction=date(2021,12,12) )

pf.get_asset(symbol="TEF").register_transaction(tr5)

pm.imprime_portfolio(pf)

