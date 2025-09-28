import argparse, math, csv

def apr_to_apy(apr_pct, compound='daily'):
    n = {'daily':365, 'weekly':52, 'monthly':12, 'quarterly':4, 'yearly':1}.get(compound, 365)
    return ( (1 + apr_pct/100/n)**(n) - 1 ) * 100

def apy_to_apr(apy_pct, compound='daily'):
    n = {'daily':365, 'weekly':52, 'monthly':12, 'quarterly':4, 'yearly':1}.get(compound, 365)
    return ( (1 + apy_pct/100)**(1/n) - 1 ) * n * 100

def simulate(principal, rate_pct, days, compound='daily', is_apy=False):
    if is_apy:
        daily_rate = (1 + rate_pct/100)**(1/365) - 1
    else:
        # APR to daily simple -> compounding per-day
        daily_rate = (rate_pct/100)/365
    amount = principal * ((1 + daily_rate) ** days)
    return amount

def compare(csv_path, principal, days):
    rows = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            name = r['name']
            apr = float(r['apr'])
            end = simulate(principal, apr, days, is_apy=False)
            pnl = end - principal
            rows.append((name, apr, round(end,2), round(pnl,2)))
    rows.sort(key=lambda x: x[3], reverse=True)
    print("Name,APR%,End Value,PNL")
    for r in rows:
        print(",".join(map(str,r)))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apr', type=float)
    ap.add_argument('--apy', type=float)
    ap.add_argument('--principal', type=float, default=1000)
    ap.add_argument('--days', type=int)
    ap.add_argument('--months', type=int)
    ap.add_argument('--compound', default='daily', choices=['daily','weekly','monthly','quarterly','yearly'])
    ap.add_argument('--compare', help='CSV path for multiple pools')
    args = ap.parse_args()

    if args.apr and args.apy:
        raise SystemExit("Use either --apr or --apy, not both.")

    if args.compare:
        if not args.days and not args.months:
            raise SystemExit("Provide --days or --months when using --compare.")
        days = args.days or int(args.months*30)
        compare(args.compare, args.principal, days)
        return

    if args.apr:
        apy = apr_to_apy(args.apr, args.compound)
        days = args.days or int((args.months or 0)*30)
        print(f"APR {args.apr:.2f}% => APY (compounded {args.compound}) = {apy:.2f}%")
        if days>0:
            end = simulate(args.principal, args.apr, days, args.compound, is_apy=False)
            print(f"Simulated end value in {days} days: {end:.2f} (PNL {end-args.principal:.2f})")
    elif args.apy:
        apr = apy_to_apr(args.apy, args.compound)
        days = args.days or int((args.months or 0)*30)
        print(f"APY {args.apy:.2f}% ~ APR (approx) = {apr:.2f}% (for {args.compound})")
        if days>0:
            end = simulate(args.principal, args.apy, days, args.compound, is_apy=True)
            print(f"Simulated end value in {days} days: {end:.2f} (PNL {end-args.principal:.2f})")
    else:
        print("Provide --apr or --apy. Try -h for help.")

if __name__ == '__main__':
    main()
