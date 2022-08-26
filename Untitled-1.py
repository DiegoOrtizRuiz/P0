string = "while (canWalk ( north ,1) ) do { walk( north ,1) } od"
print(string.count("("))
print(string.strip().replace("(","").replace(")","").replace(",","").replace("{","").replace("}","").split())