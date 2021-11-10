import pandas as pd
import cfg
from cfg import check_if_file_exist
from datetime import datetime
import logging


logging.basicConfig(
    format='%(threadName)s %(name)s %(levelname)s: %(message)s', level=logging.INFO)


def read_input_output_write_diff():
    input_excel = cfg.input_xlsx
    output_excel = cfg.output_xlsx
    sorted_sheets = cfg.sorted_sheets
    diff_data_dict = dict()
    if all([check_if_file_exist(input_excel), check_if_file_exist(output_excel)]):
        for sheet in sorted_sheets:
            if 'groups' in sheet:
                df1 = pd.read_excel(input_excel, sheet, na_values=['NA'])
                df2 = pd.read_excel(output_excel, sheet, na_values=['NA'])
                df1 = excel_sorting_groups(df1)
                df2 = excel_sorting_groups(df2)
                
                df = df2.merge(df1, how='outer', indicator=True).loc[lambda x: x['_merge'] != 'both']
                if not df.empty:
                    # df = df.replace("left_only", f"in input file {input_excel}", regex=True).replace("right_only", f"in output file {output_excel}", regex=True)
                    tmp_dict = df.to_dict()
                    domain_name = sheet.replace('.groups', '').replace('.', '/')
                    if diff_data_dict.get(domain_name):
                        diff_data_dict[domain_name] = {**diff_data_dict.get(domain_name), **tmp_dict}
                    else:
                        diff_data_dict.update({domain_name: tmp_dict})
                    pass
            elif 'urlgrps' in sheet:
                df1 = pd.read_excel(input_excel, sheet, na_values=['NA'])
                df2 = pd.read_excel(output_excel, sheet, na_values=['NA'])

                df1 = excel_sorting_urlgrps(df1)
                df2 = excel_sorting_urlgrps(df2)

                df = df2.merge(
                    df1, how='outer', indicator=True).loc[lambda x: x['_merge'] != 'both']
                if not df.empty:
                    # df = df.replace("left_only", f"in input file {input_excel}", regex=True).replace("right_only", f"in output file {output_excel}", regex=True)
                    tmp_dict = df.to_dict()
                    domain_name = sheet.replace('.urlgrps', '').replace('.', '/')
                    # diff_data_dict.update({domain_name: tmp_dict})
                    if diff_data_dict.get(domain_name):
                        diff_data_dict[domain_name] = {**diff_data_dict.get(domain_name), **tmp_dict}
                    else:
                        diff_data_dict.update({domain_name: tmp_dict})
                    pass
            elif not 'groups' in sheet and not 'urlgrps' in sheet:
                df1 = pd.read_excel(input_excel, sheet, na_values=['NA'])
                df2 = pd.read_excel(output_excel, sheet, na_values=['NA'])
                df1 = excel_sorting_objects(df1)
                df2 = excel_sorting_objects(df2)
                df = df2.merge(
                    df1, how='outer', indicator=True).loc[lambda x: x['_merge'] != 'both']
                if not df.empty:
                    # df = df.replace("left_only", f"in input file {input_excel}", regex=True).replace("right_only", f"in output file {output_excel}", regex=True)
                    tmp_dict = df.to_dict()
                    domain_name = sheet.replace('.', '/')
                    # diff_data_dict.update({domain_name: tmp_dict})
                    if diff_data_dict.get(domain_name):
                        diff_data_dict[domain_name] = {**diff_data_dict.get(domain_name), **tmp_dict}
                    else:
                        diff_data_dict.update({domain_name: tmp_dict})
                    pass
    return diff_data_dict


def create_diff_excel_file(output_file):
    diff_data_dict = read_input_output_write_diff()
    if diff_data_dict:
        with pd.ExcelWriter(output_file) as writer:
            for domain, diff_data in diff_data_dict.items():
                df = pd.DataFrame.from_dict(diff_data)
                df.to_excel(writer, sheet_name=domain)
        logging.info(f'\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} diff was written to file {output_file}\n')  
    
                
def excel_sorting_objects(df):
    if not df.empty:
        df = df.sort_values('object_name')
        df.reset_index(inplace=True)
        df = df.reindex(['object_name', 'object'], axis='columns')
        return df


def excel_sorting_groups(df):
    if not df.empty:
        df = df.sort_values('object_group_name')
        df.reset_index(inplace=True)
        df = df.reindex(['object_group_name', 'object'], axis='columns')
        return df


def excel_sorting_urlgrps(df):
    if not df.empty:
        df = df.sort_values('url_group_name')
        df.reset_index(inplace=True)
        df = df.reindex(['url_group_name', 'url'], axis='columns')
        return df

