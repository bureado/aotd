#!/usr/bin/python

"""
aotd - motd powered by Azure Advisor
    (C) 2017 Jose Miguel Parrella Romero <j@bureado.com>

Released under the terms of the Apache License, 2.0

"""

import json
import re
import hashlib

import requests
import click

URI = "http://169.254.169.254/metadata/instance?api-version=2017-04-02"


def retrieve_metadata(uri, metadata=True):
    """Retrieve metadata from Azure"""
    request = requests.get(uri, headers={"Metadata": metadata})

    if request.status_code == 200:
        # TODO: Raise exception if status_code != 200
        return request.json()


@click.command()
@click.option("--high-impact", "-i", is_flag=True, help="Only high impact.")
@click.option("--uri", "-u", default=URI, required=False, help="Azure Instance Metadata Service URI")
@click.argument("config", type=click.File("r"), required=True)
def main(config, high_impact, uri):
    """Azure Advisor-powered MOTDs"""
    msgs = []
    problems = {}

    meta_json = retrieve_metadata(uri)
    vm_name = meta_json["compute"]["name"]
    vm_location = meta_json["compute"]["location"]

    msg = "This is {name} in {location}. Here's a couple friendly reminders:\n"
    msgs.append(msg.format(name=vm_name, location=vm_location))

    recos = json.loads(config.read())

    for reco in recos:
        if re.search("virtualMachines", reco['impactedField']) and re.search(vm_name, reco['impactedValue']):
            if high_impact and not re.match("High", reco["impact"]):
                continue
            problem = reco["shortDescription"]["problem"]

            if hashlib.md5(problem).hexdigest() not in problems:
                data = {
                    "impact": reco["impact"],
                    "category": reco["category"],
                    "problem": problem,
                    "solution": reco["shortDescription"]["solution"]
                }

                msg = "* [{category}/{impact}]: {problem}".format(**data)
                msgs.append(msg)
                problems[hashlib.md5(problem).hexdigest()] = True

    for msg in msgs:
        print(msg)


if __name__ == "__main__":
    main()
