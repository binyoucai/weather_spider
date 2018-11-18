import datetime


def get_date_list(start_date='2011-01', end_date=datetime.datetime.now().strftime("%Y-%m")):
    '''
    构造年月函数
    :param start_date:开始日期
    :param end_date:结束日期
    :return:2011-01-future
    '''
    try:
        all_date_list = []  # 新建一个列表保存日期
        start_date = [int(x) for x in start_date.split('-')]
        start_year = start_date[0]  # 开始年份
        start_month = start_date[1]  # 开始月份
        end_year = int(end_date.split('-')[0])  # 终止年份
        year_list = [year for year in range(int(start_year), int(end_year) + 1)]  # 生成起始年份和终止年份的列表
        month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']  # 构造月份列表
        for year in year_list:
            temp_list = []  # 新建一个列表保存日期，中间变量
            # 做判断，保证起始年份的起始月是对的
            if year == start_year:
                new_month_list = month_list[start_month - 1:]
            else:
                new_month_list = month_list

            for month in new_month_list:
                temp_list.append('{}-{}'.format(year, month))
                year_month = '{}-{}'.format(year, month)  # 记录写入当前日期
                if end_date == year_month:
                    break
            all_date_list += temp_list
        return all_date_list
    except Exception:
        return [start_date, end_date]

date = get_date_list(start_date=datetime.datetime.now().strftime("%Y-%m"),
                     end_date=datetime.datetime.now().strftime("%Y-%m"))

