#!/usr/bin/env python
import json
import csv

def reformat(input_filename, output_filename):
    with open(input_filename, 'r') as csvfile:
        nodes = []
        links = []
        categories = {"sativa":1,"hybrid":2,"indica":3}
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            #strain_id = row["id"] TODO
            strain_id = "hybrid:"+row["name"]
            group = categories[strain_id.split(':')[0]]

            parent_list = []
            for parent in row["parents"].split(','):
                if len(parent):
                    parent_list.append(parent) 
                    # TODO what should the link value be?
                    links.append({ "source": parent, "target": strain_id, "value": 1 })
            row["parents"] = parent_list
            nodes.append({"id": strain_id, "name": row["name"], "group": group,"data":row}) # Optionally: 

        with open(output_filename,'w') as outfile:
            json.dump({"nodes":nodes, "links":links},outfile)


if __name__ == "__main__":
    reformat("strains_cleaned.csv","strains_formatted.json")