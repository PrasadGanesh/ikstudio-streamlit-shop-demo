# Synthetic sample data for the demo (fully made up, seeded).
import numpy as np, pandas as pd
rng = np.random.default_rng(42)
days = pd.date_range("2026-05-01", "2026-10-31", freq="D")
products = {"Kurti":899,"Saree":2499,"Dupatta":449,"Jhumka":299,"Potli bag":599}
channels = ["Instagram","WhatsApp","Website","Offline"]
cities = ["Delhi","Jaipur","Lucknow","Pune","Kolkata","Bengaluru"]
rows=[]
for d in days:
    n = rng.poisson(14 + (8 if d.month in (10,) else 0) + (4 if d.weekday()>=5 else 0))
    for _ in range(n):
        p = rng.choice(list(products))
        q = int(rng.integers(1,4))
        disc = float(rng.choice([0,0,0,0.1,0.2]))
        rows.append(dict(date=d.date(), product=p, channel=rng.choice(channels,p=[.4,.3,.2,.1]),
                         city=rng.choice(cities), qty=q, unit_price=products[p],
                         discount=disc, revenue=round(q*products[p]*(1-disc),2)))
pd.DataFrame(rows).to_csv("sample_orders.csv", index=False)
print(len(rows))
