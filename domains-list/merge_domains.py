import os

domains_list = list()
domains_list_duplicates = list()

# Get all files in current directory
files = [f for f in os.listdir('.') if os.path.isfile(f)]

# We only want to merge txt files
for file in files:
   if '.txt' in file:
      with open(file) as domian_names_file:
        for line in domian_names_file:
          domain = line.rstrip('\n').lower()
          if domain in domains_list:
              print (domain + ":exits")
              domains_list_duplicates.append(domain)
          else:
              domains_list.append(domain)

# Sort our list
domains_list.sort()

# Write out merged file
with open('merged_domains.txt', 'w') as f:
    for item in domains_list:
        f.write("%s\n" % item)

print "Total domains: " + str(len(domains_list))
print "Duplicates removed: " + str(len(domains_list_duplicates))
#print domains_list