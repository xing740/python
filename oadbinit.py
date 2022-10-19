#!/usr/bin/python
#coding:utf-8

import datetime

from pymysql import *


def main():

  now_time = datetime.datetime.now()
  time_str = datetime.datetime.strftime(now_time,'%Y%m%d %H:%M:%S')


  # 创建connection连接
  conn = connect(host='192.168.0.5', port=3306, database='oadb', user='root',
   password='123456', charset='utf8')
  # 获取cursor对象
  cs1 = conn.cursor()

  #合作伙伴
  # 执行sql语句
  partner = [
    ('W00001','我司','W','88888','海南海口','83712341234','海南银行','6101234','法人我司','无','xx',time_str,'xx',time_str),
    ('B00001','海南移动','B','12345','海南海口','83712341234','海南银行','6101234','法人李','无','xx',time_str,'xx',time_str),
    ('B00001','海南联通','B','12346','海南三亚','83712341235','海南银行','6101235','法人张','无','xx',time_str,'xx',time_str),
    ('B00001','海南电信','B','12347','海南海力','83712341236','海南银行','6101236','法人陈','无','xx',time_str,'xx',time_str),
    ('S00001','深信服','S','12347','海南海力','83712341236','海南银行','6101236','法人陈','无','xx',time_str,'xx',time_str),
    ('S00002','好又多配件','S','12347','海南海力','83712341236','海南银行','6101236','法人陈','无','xx',time_str,'xx',time_str)
    ]
  partnerSql = "insert into partner_info (code, name, value, tax_no, address, tel, bank_name, bank_account, legal_rep, desc_, created_by, date_created, updated_by, date_updated) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

  #用户
  user = [
    ('sw01', '00', '221018001','xx',time_str,'xx',time_str),
    ('sw02', '00', '221018002','xx',time_str,'xx',time_str),
    ('cw01', '00', '221018003','xx',time_str,'xx',time_str),
    ('cw02', '00', '221018004','xx',time_str,'xx',time_str),
    ('sx01', '00', '221018005','xx',time_str,'xx',time_str),
    ('sx02', '00', '221018006','xx',time_str,'xx',time_str),
    ('sxjl01', '00', '221018007','xx',time_str,'xx',time_str),
    ('sxjl02', '00', '221018008','xx',time_str,'xx',time_str),
    ('zjl01', '00', '221018009','xx',time_str,'xx',time_str),
    ('zjl02', '00', '221018010','xx',time_str,'xx',time_str),
    ]
  userSql = "insert into user_info (user_name, status, cust_no,created_by, date_created, updated_by, date_updated) values(%s,%s,%s,%s,%s,%s,%s)"

  #员工
  employee = [
    ('221018001','商务壹','145123198912291211','M','1989/12/29','C0003','SWRY','2021/10/18','2021/10/18','01','xx',time_str,'xx',time_str),
    ('221018002','商务贰','145123198912291212','F','1989/12/29','C0003','SWRY','2021/10/18','2021/10/18','01','xx',time_str,'xx',time_str),
    ('221018003','财务壹','145123198912291213','M','1989/12/29','C0002','CWRY','2021/10/18','2021/10/18','01','xx',time_str,'xx',time_str),
    ('221018004','财务贰','145123198912291214','F','1989/12/29','C0002','CWRY','2021/10/18','2021/10/18','01','xx',time_str,'xx',time_str),
    ('221018005','销售壹','145123198912291215','M','1989/12/29','C0004','XSRY','2021/10/18','2021/10/18','01','xx',time_str,'xx',time_str),
    ('221018006','销售贰','145123198912291216','F','1989/12/29','C0004','XSRY','2021/10/18','2021/10/18','01','xx',time_str,'xx',time_str),
    ('221018005','销售总壹','145123198912291217','M','1989/12/29','C0004','XSZG','2021/10/18','2021/10/18','01','xx',time_str,'xx',time_str),
    ('221018006','销售总贰','145123198912291218','F','1989/12/29','C0004','XSZG','2021/10/18','2021/10/18','01','xx',time_str,'xx',time_str),
    ('221018007','总经理壹','145123198912291219','M','1989/12/29','C0000','ZJL','2021/10/18','2021/10/18','01','xx',time_str,'xx',time_str),
    ('221018008','总经理贰','145123198912291220','F','1989/12/29','C0000','ZJL','2021/10/18','2021/10/18','01','xx',time_str,'xx',time_str),
    ]
  employeeSql = "insert into employee_info (work_code, name, idcard, sex, birthday, dept_code, posi_code, entry_date, regular_date, status,created_by, date_created, updated_by, date_updated) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"


  #部门信息
  department = [
    ('C0000', '总部', '总部','0',"xx",time_str,'xx',time_str),
    ('C0001', '人事部', '人事部','C0000',"xx",time_str,'xx',time_str),
    ('C0002', '财务部', '账务部','C0000',"xx",time_str,'xx',time_str),
    ('C0003', '商务部', '商务部','C0000',"xx",time_str,'xx',time_str),
    ('C0004', '销售部', '销售部','C0000',"xx",time_str,'xx',time_str),
    ('C0005', '技服部', '技服部','C0000',"xx",time_str,'xx',time_str),
  ]
  departmentSql = "insert into department_info (code, name, desc_, par_dpm, created_by, date_created, updated_by, date_updated) values(%s,%s,%s,%s,%s,%s,%s,%s)"


  #职务信息
  position = [
    ('SWRY', '商务', '商务',"xx",time_str,'xx',time_str),
    ('CWRY', '账务', '账务',"xx",time_str,'xx',time_str),
    ('ZJL', '总经理', '总经理',"xx",time_str,'xx',time_str),
    ('XSZG', '销售主管', '销售主管',"xx",time_str,'xx',time_str),
    ('XSRY', '销售人员', '销售人员',"xx",time_str,'xx',time_str),
  ]
  positionSql = "insert into position_info (code, name, desc_, created_by, date_created, updated_by, date_updated) values(%s,%s,%s,%s,%s,%s,%s)"


  taskDef = [
    ('项目立项流程', '项目立项流程', 'project_create','SWRY','xx',time_str,'xx',time_str),
  ]

  taskDefSql = "insert into task_def_info (name, desc_, code, posi_code, created_by, date_created, updated_by, date_updated) values(%s,%s,%s,%s,%s,%s,%s,%s)"

  #合作伙伴
  cs1.executemany(partnerSql, partner)
  print("创建合作伙伴成功")
  conn.commit()

  #用户
  cs1.executemany(userSql, user)
  print("创建用户成功")

  #员工
  cs1.executemany(employeeSql, employee)
  print("创建员工成功")
  conn.commit()

  #部门
  cs1.executemany(departmentSql, department)
  print("创建部门成功")

  #职位
  cs1.executemany(positionSql, position)
  print("创建职位成功")

  #任务定义
  cs1.executemany(taskDefSql, taskDef)
  print("创建任务成功")

  # 提交之前的操作，如果之前已经执行多次的execute，那么就都进行提交
  conn.commit()

  # 关闭cursor对象
  cs1.close()
  # 关闭connection对象
  conn.close()


if __name__ == '__main__':
  main()
