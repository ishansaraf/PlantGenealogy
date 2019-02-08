#!/usr/bin/env python
import json
import csv
import argparse

def category(strain_id):
    categories = {"sativa":1,"hybrid":2,"indica":3}
    return categories[strain_id.split(':')[0]]
def distance(s1, s2):
    d=1+abs(category(s1)-category(s2))
    return d*d*d
def reformat(input_filename, output_filename):
    # Handle name changes that redirect but the backend was never updated
    substituition_dict = {"hybrid:girl-scout-cookie":"hybrid:gsc","hybrid:platinum-girl-scout-cookies":"hybrid:platinum-gsc","hybrid:platinum-girl-scout-cookie":"hybrid:platinum-gsc"}

    found_ids=set()
    missing_ids=set()
    parent_ids=set() # All ids that show up in parents, thus we need them even if they don't have children

    with open(input_filename, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            found_ids.add(row["id"])

            for p in row["parents"].split(','):
                if not len(p):
                    continue
                elif p in substituition_dict:
                    parent_ids.add(substituition_dict[p])
                else:
                    parent_ids.add(p)


    with open(input_filename, 'r') as csvfile:
        nodes = []
        links = []
        info = {}

        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            strain_id = row["id"]
            group = category(strain_id)
            parent_list = []
            for p in row["parents"].split(','):
                if not len(p):
                    continue
                elif p in substituition_dict:
                    parent = substituition_dict[p]
                elif p not in found_ids:
                    missing_ids.add(p)
                    print("Strain %s is missing parent %s"%(strain_id,p))
                    continue
                else:
                    parent = p
                parent_list.append(parent) 
                # TODO what should the link value be? Do we even want one?
                links.append({ "source": parent, "target": strain_id, "value": distance(strain_id,parent) })
            row["parents"] = parent_list
            if len(parent_list) or strain_id in parent_ids:
                nodes.append({"id": strain_id, "name": row["name"], "group": group,"hasparent":len(parent_list) > 0})
                info[strain_id]=row
            else:
                print("Strain %s has no parents or children, discarding record" % strain_id,)
        if len(missing_ids):
            print("Warning, the following ids are missing and were ignored:")
            print(missing_ids)
        print("Total number of nodes output: %d" %len(nodes),) 
        with open(output_filename,'w') as outfile:
            json.dump({"nodes":nodes, "links":links,"info":info},outfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Reformat data into better format for visualization')
    parser.add_argument('--infile',
                        default='strains_reduced.csv',
                       help='input filename (should end in .csv)')
    parser.add_argument('--outfile',
                       default='strains_formatted.json',
                       help='output filename (should end in .json)')

    args = parser.parse_args()
    reformat(args.infile, args.outfile)