# -*- coding: UTF-8 -*-                                                                                                            

		
import sqlite3


con = sqlite3.connect("/tmp/user.db")

cur = con.cursor()

fin = file( "prefer_test_usr_list2.txt" , "rU" )

sql = "CREATE TABLE IF NOT EXISTS User ( Sn Auto_increment INTEGER , Uid , Passwd , Grp , PtScore )"
cur.execute( sql )

sql = "CREATE TABLE IF NOT EXISTS Log ( Sn Auto_increment INTEGER , Uid , Query , Time )"
cur.execute( sql )



for line in fin:
	#uid , score , level = line.strip().split("\t")
	uid = line.strip()
	cur.execute( "INSERT INTO User ( Uid , Passwd , Grp , PtScore ) VALUES ( ? , ? , ? , ? )" , ( uid , uid , "" , "" ) )
	
con.commit()
con.close()




