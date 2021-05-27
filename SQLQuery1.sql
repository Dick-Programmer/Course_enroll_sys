
create table s_College
	(yxh char(2) not null,
	name varchar(50) not null,
	adress varchar(100) not null,
	p_no char(8) not null,
	primary key(yxh));

create table s_Student
	(xh char(8) not null,
	name varchar(20) not null,
	sex varchar(10),
	birthday date,
	hometown varchar(10),
	mp_no char(11),
	yxh char(2),
	pwd varchar(16),
	foreign key(yxh)references s_College(yxh),
	primary key(xh));

create table s_Teacher
	(gh char(4) not null,
	name varchar(20) not null,
	sex varchar(10),
	birthday date,
	education varchar(10),
	salary numeric(7,2),
	yxh char(2),
	pwd varchar(16),
	foreign key(yxh)references s_College(yxh),
	primary key(gh));

create table s_Course
	(kh char(8) not null,
	name varchar(20) not null,
	credit smallint not null,
	period smallint,
	psrate float,
	yxh varchar(2),
	foreign key(yxh)references s_College(yxh),
	primary key(kh));

create table s_Class
	(semester varchar(14) not null,
	kh char(8) not null,
	gh char(4) not null,
	class_time varchar(12) not null,
	maxsize smallint,
	nowsize smallint,
	foreign key(gh)references s_Teacher(gh),
	foreign key(kh)references s_Course(kh), 
	primary key(semester,kh,gh));

create table s_SelectC
	(xh char(8) not null,
	semester varchar(14) not null,
	kh char(8) not null,
	gh char(4) not null,
	pscj smallint,
	kscj smallint,
	zpcj smallint,
	foreign key(xh)references s_Student(xh),
	foreign key(kh)references s_Class(kh),
	foreign key(gh)references s_Class(gh),
	primary key(xh,semester,kh));

Create table s_Manager
	(gh char(5),
	pwd varchar(16),
	primary key(gh));

Create table s_Semester
	(semester varchar(14) not null,
	weeks varchar(6) not null,
	now TINYINT not null,
	primary key(semester));

Create table s_Inform
	(gh char(5),
	title varchar(100),
	time datetime,
	detail text,
	preview text,
	foreign key(gh)references s_Manager(gh),
	primary key(gh,title));
	
Create table s_SelectCtime
	(semester varchar(14) not null,
	bigin datetime,
	end datetime,
	primary key(semester));

Create table Massage
	(time datetime not null,
	from TINYINT not null,
	gh char(5) not null,
	xh char(8) not null,
	msg varchar(200),
	foreign key(gh)references s_Teacher(gh),
	foreign key(xh)references s_Student(xh),
	primary key(time,gh,xh));

Create table ApplyCourse
	(gh char(5) not null,
	name varchar(20) not null,
	credit smallint not null,
	period smallint,
	psrate float,
	yxh varchar(2) not null,
	detail text,
	time datetime,
	status smallint not null,
	foreign key(gh)references s_Teacher(gh),
	foreign key(yxh)references s_College(yxh),
	primary key(gh,name));

Delimiter //
Create procedure update_zpcj(IN semesterh char(14))
Begin
Update s_SelectC,s_Course Set zpcj=pscj*psrate+kscj*(1-psrate) where semester=semesterh and s_SelectC.kh=s_Course.kh;
END
//
Delimiter;

call update_zpcj('2017-2018 �＾');


Drop Trigger if Exists update_nowsize
Delimiter $
Create Trigger update_nowsize
Before insert on s_SelectC 
For each row
Begin
Declare now int;
Declare max int;
Declare msg varchar(100);
Set now=(Select nowsize from s_Class where kh=new.kh and semester=new.semester);
Set max=(Select maxsize from s_Class where kh=new.kh and semester=new.semester);
If now < max then
	Update s_Class Set nowsize = nowsize+1 where kh=new.kh and semester=new.semester;
Else 
	set msg = "Class_SizeIsFull";  
    SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = msg;  
End if;
End$
Delimiter ;

Drop Trigger if Exists del_nowsize
Delimiter $
Create Trigger del_nowsize
Before Delete on s_SelectC 
For each row
Begin
	Update s_Class Set nowsize = nowsize-1 where kh=old.kh and semester=old.semester;
End$
Delimiter ;


insert into s_College values('01','�����ѧԺ','�ϴ�У������¥','65347567');
insert into s_College values('02','ͨ��ѧԺ','�ϴ�У������¥','65341234');
insert into s_College values('03','����ѧԺ','�ϴ�У���ĺ�¥','65347890');
insert into s_College values('04','����ѧԺ','�ϴ�У�����¥','65347213');
insert into s_College values('05','����ѧԺ','�ϴ���У���ߺ�¥','65232344');

insert into s_Student values('1501234','����','��','1993-03-06','�Ϻ�','13613005486','01','1501234');
insert into s_Student values('1501235','������','��','1992-12-08','����','18913457890','01','1501235'); 
insert into s_Student values('1501236','�ų��','��','1993-01-05','����','18826490423','01','1501236');
insert into s_Student values('1501237','������','Ů','1994-11-06','�Ϻ�','13331934111','01','1501237'); 
insert into s_Student values('1501829','���ɸ�','��','1991-06-07','�Ϻ�','18015872567','03','1501829');
insert into s_Student values('1506232','�����','Ů','1993-05-04','����','18107620945','01','1506232');
insert into s_Student values('1507232','������','��','1992-08-16','�㽭','13912341078','05','1507232');
insert into s_Student values('1601234','�����','��','1993-03-06','�Ϻ�','13623435486','01','1601234');
insert into s_Student values('1601235','����','��','1992-12-08','����','18913342490','04','1601235'); 
insert into s_Student values('1601236','������','Ů','1993-01-05','����','18123290423','01','1601236');
insert into s_Student values('1601237','������','Ů','1994-11-06','�Ϻ�','13435434111','02','1601237'); 
insert into s_Student values('1601829','������','��','1991-06-07','�Ϻ�','18023412567','01','1601829');
insert into s_Student values('1606232','�뱦��','Ů','1993-05-04','����','18123230945','02','1606232');
insert into s_Student values('1607232','����','Ů','1992-08-16','�㽭','13914351078','04','1607232');

insert into s_Teacher values('0101','�µ�ï','��','1973-03-06','������',3567.00,'02','0101');
insert into s_Teacher values('0102','��С��','Ů','1972-12-08','��ʦ',2845.00,'02','0102');
insert into s_Teacher values('0201','����ӱ','Ů','1960-01-05','����',4200.00,'04','0201');
insert into s_Teacher values('0143','�ⱦ��','��','1980-11-06','��ʦ',2554.00,'03','0143');
insert into s_Teacher values('0401','�µ���','��','1978-03-06','������',4982.00,'05','0401');
insert into s_Teacher values('0302','������','Ů','1972-02-08','��ʦ',2845.00,'01','0302');
insert into s_Teacher values('0304','����','Ů','1967-04-05','����',4200.00,'01','0304');
insert into s_Teacher values('0303','�����','��','1977-12-06','��ʦ',2554.00,'01','0303');
insert into s_Teacher values('0305','��¸�','Ů','1972-02-08','��ʦ',2845.00,'01','0305');
insert into s_Teacher values('0306','������','Ů','1967-04-05','����',4200.00,'01','0306');
insert into s_Teacher values('0307','����','��','1977-12-06','��ʦ',2554.00,'01','0307');

insert into s_Course values('08305001','��ɢ��ѧ',4,40,0.4,'01');
insert into s_Course values('08305002','���ݿ�ԭ��',4,50,0.4,'01'); 
insert into s_Course values('08305003','���ݽṹ',4,50,0.5,'01');
insert into s_Course values('08305004','ϵͳ�ṹ',6,60,0.3,'01');
insert into s_Course values('08301001','��������ѧ',4,40,0.3,'03'); 
insert into s_Course values('08305013','����ԭ��',3,30,0.4,'01');
insert into s_Course values('08305124','ϵͳ�ṹ',3,30,0.4,'01');
insert into s_Course values('03302001','���ֱ���',3,30,0.5,'05');
insert into s_Course values('08302001','ͨ��ѧ',3,30,0.3,'02');
insert into s_Course values('02304301','����',3,30,0.3,'04');
insert into s_Course values('08302101','ģ���·',3,30,0.3,'04');

insert into s_Class values('2017-2018 �＾','08305001','0302','������ 5-8',0,10); 
insert into s_Class values('2017-2018 ����','08305002','0303','������ 1-4',0,10);
insert into s_Class values('2017-2018 ����','08305002','0304','������ 1-4',0,10);
insert into s_Class values('2017-2018 ����','08305002','0305','������ 1-4',0,10);
insert into s_Class values('2017-2018 ����','08305003','0303','������ 5-8',0,10);
insert into s_Class values('2018-2019 �＾','08305004','0306','���ڶ� 1-4',0,10);
insert into s_Class values('2018-2019 �＾','08305013','0307','������ 5-8',0,10);
insert into s_Class values('2018-2019 ����','08305124','0201','����һ 5-8',0,10);
insert into s_Class values('2018-2019 ����','08302101','0201','���ڶ� 5-8',0,10);

insert into s_SelectC values('1501234','2017-2018 �＾','08305001','0302',60,60,60); 
insert into s_SelectC values('1501235','2017-2018 �＾','08305001','0302',87,87,87); 
insert into s_SelectC values('1501235','2017-2018 ����','08305002','0303',82,82,82); 
insert into s_SelectC values('1501235','2018-2019 �＾','08305004','0306',null,null,null); 
insert into s_SelectC values('1501236','2017-2018 �＾','08305001','0302',56,56,56); 
insert into s_SelectC values('1501236','2017-2018 ����','08305002','0304',75,75,75); 
insert into s_SelectC values('1501236','2017-2018 ����','08305003','0303',84,84,84); 
insert into s_SelectC values('1501236','2018-2019 �＾','08305001','0302',null,null,null); 
insert into s_SelectC values('1501236','2018-2019 �＾','08305004','0306',null,null,null);
insert into s_SelectC values('1501237','2017-2018 �＾','08305001','0302',74,74,74); 
insert into s_SelectC values('1501237','2018-2019 ����','08305124','0201',null,null,null); 
insert into s_SelectC values('1501829','2017-2018 �＾','08305001','0302',85,85,85); 
insert into s_SelectC values('1501829','2017-2018 ����','08305002','0305',66,66,66); 
insert into s_SelectC values('1506232','2017-2018 �＾','08305001','0302',90,90,90); 
insert into s_SelectC values('1506232','2017-2018 ����','08305003','0303',79,79,79); 
insert into s_SelectC values('1506232','2018-2019 �＾','08305004','0306',null,null,null);
insert into s_SelectC values('1601236','2017-2018 �＾','08305001','0302',60,60,60); 
insert into s_SelectC values('1601829','2017-2018 �＾','08305001','0302',60,60,60); 

insert into s_Manager values('10001','admin'); 
insert into s_Manager values('10002','10002'); 
insert into s_Manager values('10003','10003'); 