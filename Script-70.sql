select (select name from employees e where e.employee_id=p.employee_id) as  emp, sum(p.hours_payment),sum(s.summ)  from works w left join services s on w.work_id =s.work_id 
left join performers p on p.work_id =w.work_id 
where date_ like '2024-09%' and department_id =1 and s.nomenclature_id =1
group by emp, w.summ