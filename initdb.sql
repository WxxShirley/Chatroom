DROP TABLE IF EXISTS "userinfo";
CREATE TABLE "userinfo"(
"username" TEXT not NULL,
"password" TEXT not NULL,
PRIMARY KEY("username")
);


DROP TABLE IF EXISTS "private_history_text";
CREATE TABLE "private_history_text"(
"id" INTEGER not NULL,
"target_user" TEXT not NULL,
"source_user" TEXT not NULL,
"time" DATETIME not NULL,
"text" TEXT not NULL,
PRIMARY KEY("id"),
FOREIGN KEY ("target_user") REFERENCES "userinfo"("username"),
FOREIGN KEY ("source_user") REFERENCES "userinfo"("username")
);


DROP TABLE IF EXISTS "history_bigGroup_text";
CREATE TABLE "history_bigGroup_text"(
"id" INTEGER not NULL,
"source_user" TEXT not NULL,
"target_user" TEXT not NULL,
"time" DATETIME not NULL,
"text" TEXT  not NULL,
PRIMARY KEY("id"),
FOREIGN KEY ("source_user") REFERENCES "userinfo"("username"),
FOREIGN KEY ("target_user") REFERENCES "userinfo"("username")
);


DROP TABLE IF EXISTS "groups";
CREATE TABLE "groups"(
"group_id" INTEGER not NULL,
"group_name" TEXT not NULL,
PRIMARY KEY("group_id")
);


DROP TABLE IF EXISTS "group_member";
CREATE TABLE "group_member"(
"group_id" INTEGER not NULL,
"username" TEXT not NULL,
FOREIGN KEY("group_id") REFERENCES "groups"("group_id"),
FOREIGN KEY("username") REFERENCES "userinfo"("username"),
);


DROP TABLE IF EXISTS "friends";
CREATE TABLE "friends"(
"username1" TEXT not NULL,
"username2" TEXT not NULL,
PRIMARY KEY("username1","username2"),
FOREIGN KEY("username1") REFERENCES "userinfo"("username"),
FOREIGN KEY("username2") REFERENCES "userinfo"("username"),
);