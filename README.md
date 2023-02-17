# ipn_isn_automation
1) clone the repo<br> 
 git clone https://github.com/cassiolange/ipn_isn_automation/
2) install the python requirements - Recommended use virtual environment (venv)<br>
pip install -r python_requirements.txt 
3) install the ansible galaxy module<br>
ansible-galaxy install -r galaxy_requirements.yaml
4) Copy the excel file to the spreadsheet folder
5) Execute the playbooks 
ansible-playbook 0.management.yml<br>
ansible-playbook 1.enable_nxos_features.yml<br>
ansible-playbook 2.po.yml<br>
ansible-playbook 3.vrfs.yml<br>
ansible-playbook 4.loopbacks.yml<br>
ansible-playbook 5.l3-interfaces.yml<br>
ansible-playbook 6.1.ospf.yml<br>
ansible-playbook 6.2.bgp.yml<br>
ansible-playbook 6.6.multicast.yml<br>
