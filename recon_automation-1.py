#recon_automation-1.py

import json
import subprocess
import shlex
import os

target = input("enter target:").strip()
if not target:
	print("[-] Invalid domain.")
	exit(1)


t_details=target.split(".")
targ_host=t_details[0]

os.makedirs(f"./{targ_host}_{t_details[1]}",exist_ok=True)
directory=os.path.expanduser(f"./{targ_host}_{t_details[1]}")

subfinder_out = f"{directory}/{targ_host}-subdomains.jsonl"
httpx_out = f"{directory}/{targ_host}-httpx_out.txt"
only_subs = f"{directory}/{targ_host}-only_subs.txt"



subfinder_path=os.path.expanduser("~/go/bin/subfinder")

command_subfinder = f"{subfinder_path} -d {target}  -v -o {subfinder_out} -oJ"

args=shlex.split(command_subfinder)
process=subprocess.Popen(args,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

for p in process.stdout:
	print(p.strip())

process.wait()

with open(subfinder_out ,"r") as f:
	subdomains = [json.loads(line) for line in f]
	if not subdomains:
		print("[-] No subdomains found.")
		exit(1)
with open(only_subs,"w") as f:
	for sub in subdomains:
		f.write(f"{sub['host']}\n")
httpx_path = os.path.expanduser("~/go/bin/httpx")


command_httpx = f"{httpx_path} -list {only_subs} -title -status-code -tech-detect -ip -o {httpx_out}"
args2=shlex.split(command_httpx)
process_httpx =subprocess.Popen(args2 ,stdout= subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

for p in process_httpx.stdout:
	print(p.strip())

process_httpx.wait()
def filterfunc(filepath ,status_code):

	try:
		with open(filepath, "r") as f:
			all_of_contents=f.readlines()
	except FileNotFoundError:
		print("[!] File Not Found. :/")
		return 
	filtered_lines=[line.strip() for line in all_of_contents if status_code in line]
	if len(filtered_lines) == 0:
		return
	print(f"\nAll [{status_code}] Codes ({len(filtered_lines)} found)")
	for line in filtered_lines:
		print(line)




# 4xx CLIENT ERROR
print("\n------4xx CLIENT ERROR--------")
filterfunc(httpx_out, "400")
filterfunc(httpx_out, "401")
filterfunc(httpx_out, "403")
filterfunc(httpx_out, "404")
filterfunc(httpx_out, "405")
filterfunc(httpx_out, "408")
filterfunc(httpx_out, "409")
filterfunc(httpx_out, "410")
filterfunc(httpx_out, "413")
filterfunc(httpx_out, "429")
# 5xx SERVER ERROR
print("-------5xx SERVER ERROR-------")
filterfunc(httpx_out, "500")
filterfunc(httpx_out, "502")
filterfunc(httpx_out, "503")
filterfunc(httpx_out, "504")



# 3xx REDIRECT
print("\n------3xx REDIRECT--------")
filterfunc(httpx_out, "301")
filterfunc(httpx_out, "302")
filterfunc(httpx_out, "303")
filterfunc(httpx_out, "304")
filterfunc(httpx_out, "307")
filterfunc(httpx_out, "308")

# 2xx SUCCESSFUL
print("\n------2xx SUCCESSFUL--------")
filterfunc(httpx_out, "200")
#filterfunc(httpx_out, "201")
#filterfunc(httpx_out, "202")
#filterfunc(httpx_out, "204")

