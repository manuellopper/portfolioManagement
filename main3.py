import pfmanager.engine as pm
import pfmanager.currency as cu
from datetime import date

curr1=cu.Currency(2.5)
curr2=cu.Currency(5)
print(curr1)
print(curr1.get_value("ASSET"),curr1.get_currency("ASSET"),curr1.get_value("LOCAL"),curr1.get_currency("LOCAL"))
print(curr2)
print(curr2.get_value("ASSET"),curr2.get_currency("ASSET"),curr2.get_value("LOCAL"),curr2.get_currency("LOCAL"))
curr3=curr2+curr1
print(curr3)
print(curr3.get_value("ASSET"),curr3.get_currency("ASSET"),curr3.get_value("LOCAL"),curr3.get_currency("LOCAL"))

pf=pm.Portfolio("De Giro")
pf.register_asset(pm.AssetEquity("Telefónica SA","EUR","TEF"))


tr1 = pm.TransactionBuy(10,cu.Currency(100),cu.Currency(2.5),date_transaction=date(2020,5,3) )

pf.get_asset(symbol="TEF").register_transaction(tr1)


tr2 = pm.TransactionBuy(5,cu.Currency(110),cu.Currency(2.5),date_transaction=date(2020,6,4) )

pf.get_asset(symbol="TEF").register_transaction(tr2)

tr3 = pm.TransactionSell(4,cu.Currency(115),cu.Currency(2.5),date_transaction=date(2021,2,10) )

pf.get_asset(symbol="TEF").register_transaction(tr3)

tr4 = pm.TransactionSell(10,cu.Currency(110),cu.Currency(2.5),date_transaction=date(2021,5,12) )

pf.get_asset(symbol="TEF").register_transaction(tr4)

tr5 = pm.TransactionDividend(cu.Currency(10),taxes=cu.Currency(1.5),date_transaction=date(2021,12,12) )

pf.get_asset(symbol="TEF").register_transaction(tr5)

pm.imprime_portfolio(pf)

