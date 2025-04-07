select u.user_id from users u join works w 
on u.user_id =w.user_id 
union
select u.user_id from users u join duties d on u.user_id =d.user_id 
Выбрать инженеров у которых есть либо работы, либо дежурства, либо и то и то.
