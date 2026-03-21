#!/bin/bash
hyperfine --parameter-list size 10,20,30,40,50,100,200,300,400,500,600,700,800,900,1000 './sortedlist array {size}' './sortedlist set {size}' './sortedlist binary {size}' --export-csv output/benchmark.sh
