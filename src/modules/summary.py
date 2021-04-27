def printSummary(results):

    #column 1: index
    index_max_len = 3
    #column 2: name
    name_max_len = 4
    #column 3: enable
    enable_max_len = 7
    #column 4: status
    status_max_len = 6
    #column 5: Last-Update
    date_max_len = 11
    #column 6: ip count
    count_max_len = 5

    for result in results:
        tlen = len(result['name'])
        name_max_len = (name_max_len if(name_max_len > tlen) else tlen)
        if result['enable']:
            if result['status'] == 'OK':
                tlen = len(result['date'])
                date_max_len = (date_max_len if (date_max_len > tlen) else tlen)

    table_fmt = '| %%-%ds | %%-%ds | %%-%ds | %%-%ds | %%-%ds | %%-%ds |' % (index_max_len, name_max_len, enable_max_len, status_max_len, date_max_len, count_max_len)

    index = 0
    separator = '+-'+ '-'*index_max_len+ '-+-'+ '-'*name_max_len+ '-+-'+ '-'*enable_max_len+ '-+-'+ '-'*status_max_len+ '-+-'+ '-'*date_max_len+ '-+-'+ '-'*count_max_len+ '-+'
    print(separator)
    print(table_fmt % ('No.', 'Name', 'Enable', 'Status', 'Last Update', 'Count'))
    print(separator)

    for result in results:
        index = index + 1
        if result['enable']:
            if result['status'] == 'OK':
                print(table_fmt % (index, result['name'], result['enable'], result['status'], result['date'], result['count']))
            else:
                print(table_fmt % (index, result['name'], result['enable'], result['status'], result['message'], '-'))
        else:
            print(table_fmt % (index, result['name'], result['enable'], '-', '-', '-'))
    print(separator)

