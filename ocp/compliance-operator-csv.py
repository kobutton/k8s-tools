#!/usr/bin/env python3 


## This writes the output of the compliance operator to a CSV that is consumable in excel, for obvious reasons.
## Requires oc client, active k8s user session to a cluster with compliance-operator installed and works for CIS-OCP Benchmark profiles.0
## Write to stdout, redirect to file for saving


import csv, subprocess, json, sys
cr = { x["metadata"]["annotations"]["compliance.openshift.io/rule"]: x for x in json.loads(subprocess.Popen(["oc", "get", "rules", "-n", "openshift-compliance", "-o", "json"], stdout=subprocess.PIPE).communicate()[0], strict=False)["items"]}
ccr = json.loads(subprocess.Popen(["oc", "get", "compliancecheckresults", "-n", "openshift-compliance", "-o", "json"], stdout=subprocess.PIPE).communicate()[0], strict=False)["items"]
output = [{
	  "ComplianceCheckResultName": result["metadata"]["name"],
	  "Status": result["status"],
	  "Severity": result["severity"],
	  "Description": result["description"],
	  "Instructions": result["instructions"],
	  "Rationale": cr[result["metadata"]["annotations"]["compliance.openshift.io/rule"]]["rationale"],
	  "CIS-OCP Benchmark ID": cr[result["metadata"]["annotations"]["compliance.openshift.io/rule"]]["metadata"]["annotations"]["control.compliance.openshift.io/CIS-OCP"],
	
	
	} for result in ccr]
dw = csv.DictWriter(sys.stdout, output[0].keys(), dialect='excel')
dw.writeheader()
dw.writerows(output)
