from pfmanager.engine import *


pf=Portfolio("Portfolio de Prueba")
as1=Asset("Telefónica SA","EUR",pf)
as2=AssetEquity("Iberdrola","EUR","IBR",pf)
d=Transaction()
e=TransactionBuyEquity()
f=TransactionSellEquity()
g=TransactionDividendEquity()
h=TransactionDividendWithSharesEquity()

print(pf.pf_name)
print(f"Asset - Id: {as1.get_id()} Asset Type: {as1.asset_type} Nombre: {as1.asset_name} Currency: {as1.currency} Portfolio: {as1.portfolio.pf_name}")
print(f"Asset - Id: {as2.get_id()} Asset Type: {as2.asset_type} Nombre: {as2.asset_name} Symbol: {as2.symbol} Currency: {as2.currency} Portfolio: {as2.portfolio.pf_name}")


print(d.get_id())
print(e.get_id())
print(f.get_id())
print(g.get_id())
print(h.get_id())

