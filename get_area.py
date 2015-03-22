from os import listdir

guns = {}

def add_gun(period, area, desc):

    if period in guns and guns[period][0] <= area:
        return

    guns[period] = (area, desc)

def divisors(n, compression):
    for x in range(1, n // compression + 1):
        if n % x == 0:
            yield n // x

def add_variable_gun(base, x, y, compression, factor):
    
    for d in range(100):
        area = (x+d) * (y+d)
        for p in divisors(base + 8 * d, compression):
            add_gun(p * factor, area, "p%d%s_%d" % (base, "__dtq"[factor], d))


# examine fixed guns
for filename in listdir("fixed"):
    try:
        if filename[-4:] != ".lif":
            continue

        period = int(filename[1:6])
        for line in open("fixed/" + filename):
            if line[0] == 'x':
                line = line.split(" ")
                area = int(line[2][:-1]) * int(line[5][:-1])
                add_gun(period, area, "fixed")
    except:
        print "***** Problem with gun %s" % filename
        raise

# examine variable guns
for filename in listdir("variable"):
    try:
        if filename[-4:] != ".lif":
            continue

        period = int(filename[1:6])
        compression = None
        factor = None

        if len(filename) == 10:
            factor = 1
        elif filename[6] == "d":
            factor = 2
        elif filename[6] == "t":
            factor = 3
        elif filename[6] == "q":
            factor = 4

        for line in open("variable/" + filename):
            if line[0] == 'x':
                line = line.split(" ")
                x = int(line[2][:-1])
                y = int(line[5][:-1])
            elif "compression" in line:
                compression = int(line.split()[-1])

        add_variable_gun(period, x, y, compression, factor)

    except:
        print "Problem with gun %s" % filename
        raise

stats = {}

for period in guns:
    if period < 1000:
        gun_type = guns[period][1].split("_")[0]
        stats[gun_type] = stats.get(gun_type, 0) + 1
        print period, guns[period]

print ""
print "*************"
print "Stats"
print "*************"

for gun_type in sorted(stats, key=stats.get, reverse=True):
    print gun_type, stats[gun_type]

print "variable %d" % (1000 - 14 - stats["fixed"])
