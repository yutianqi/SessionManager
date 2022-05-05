#!/usr/bin/env python3
#encoding=utf8

import json


def main():
    with open("sessions.json") as f:
        lines = f.readlines()
        # print(lines)
        myDict = json.loads("".join(lines))	
        print(len(myDict))
        print(len(myDict[0].get("childNodes")[0].get("childNodes")))


if __name__ == "__main__":
    main()

