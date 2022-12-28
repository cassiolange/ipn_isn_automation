import pandas
import time
import yaml
import excel_to_yaml_config
import glob
import os

def generate_yaml():
    yaml_data = {}
    hosts = {
        'all': {
            'children':{
                'switches':{
                    'children':{
                        'switches_ios' : {'hosts': {}},
                        'nxos' : {'hosts': {}},
                    }
                },
                'routers':{
                    'children':{
                        'routers_ios' : {'hosts': {}},
                        'ios_xr' : {'hosts': {}},
                    }
                }
            }
        }
    }
    ###loop all the input file and folder to determine if the input file or folder exist
    excel_files =[]
    for input in excel_to_yaml_config.config:
        if os.path.exists(input):
            if os.path.isfile(input):
                excel_files.append(input)
            else:
                #get all xlsx files from the folde
                if input.endswith('/') == False:
                    input = input+'/'
                files = glob.glob(input+'[!~]*.xlsx')
                for file in files:
                    excel_files.append(file)
        else:
            print('Input %s does not exist' % input)

    for excel_file in excel_files:
        excel = pandas.read_excel(excel_file, None, engine='openpyxl')
        sheets = list(excel.keys())
        excel = pandas.read_excel(excel_file, sheet_name='devices', engine='openpyxl')
        for line in excel.index:
            yaml_data.update({str(excel['HOSTNAME'][line]): {}})
            if excel['DEVICE_TYPE'][line] == 'router' and excel['DEVICE_OS'][line] == 'IOS_XE':
                hosts['all']['children']['routers']['children']['routers_ios']['hosts'][excel['HOSTNAME'][line]] = {
                    'ansible_host': str(excel['MGMT_IP'][line]).split('/')[0]
                }
            elif excel['DEVICE_OS'][line] == 'NXOS':
                hosts['all']['children']['switches']['children']['nxos']['hosts'][excel['HOSTNAME'][line]] = {
                    'ansible_host': str(excel['MGMT_IP'][line]).split('/')[0]
                }
                if excel['USERNAME'].isnull()[line] == False:
                    hosts['all']['children']['switches']['children']['nxos']['hosts'][excel['HOSTNAME'][line]].update(
                        {
                            'ansible_user': excel['USERNAME'][line]
                        }
                    )
                if excel['PASSWORD'].isnull()[line] == False:
                    hosts['all']['children']['switches']['children']['nxos']['hosts'][excel['HOSTNAME'][line]].update(
                        {
                            'ansible_password': excel['PASSWORD'][line]
                        }
                    )
            elif excel['DEVICE_OS'][line] == 'IOS_XR':
                hosts['all']['children']['routers']['children']['ios_xr']['hosts'][excel['HOSTNAME'][line]] = {
                    'ansible_host': str(excel['MGMT_IP'][line]).split('/')[0]
                }
            else:
                hosts['all']['children']['switches']['children']['switches_ios']['hosts'][excel['HOSTNAME'][line]] = {
                    'ansible_host': str(excel['MGMT_IP'][line]).split('/')[0]
                }

        for sheet in sheets:
            print('Sheet: %s' %sheet)
            excel = pandas.read_excel(excel_file, sheet_name=sheet, engine='openpyxl')
            columns = list(excel.keys())
            for line in excel.index:
                current_line = {}
                if ('STATUS' not in columns or excel['STATUS'][line] != 'ignored') and 'HOSTNAME' in columns and excel['HOSTNAME'].isnull()[line] == False:
                    for column in columns:
                        if excel[column].isnull()[line] == False:
                            current_line.update(
                                {
                                    str(column).lower(): str(excel[column][line]).strip().lstrip()
                                }
                            )
                        elif column == 'STATUS':
                            current_line.update(
                                {
                                    str(column).lower(): 'present'
                                }
                            )
                    if not sheet in yaml_data[excel['HOSTNAME'][line]]:
                        yaml_data[(excel['HOSTNAME'][line])].update({str(sheet): []})
                    yaml_data[excel['HOSTNAME'][line]][str(sheet)].append(current_line)

    #print(yaml_data)
    for i in yaml_data:
        file = open('../host_vars/'+i+'.yml','w')
        yaml.safe_dump(yaml_data[i], file)
        #print(routers[i])
        file.close()

    file = open('../hosts.yml','w')
    yaml.safe_dump(hosts, file)
    file.close()

def main():
    start = time.time()
    generate_yaml()
    print("Elapsed time %s" % str(time.time()-start))

if __name__ == '__main__':
    main()