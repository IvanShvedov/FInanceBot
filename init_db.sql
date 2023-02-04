create table UserAccount
(
 UserTelegramID text not null
);
create table Category
(
 CategoryID integer not null PRIMARY KEY,
 UserTelegramID integer not null references UserAccount(UserTelegramID),
 CategoryName text not null
);
create table UserOperation
(
 UserTelegramID integer not null references UserAccount(UserTelegramID),
 CategoryID integer references Category(CategoryID) on delete set null,
 Description text,
 Amount float not null,
 IsEnrollment bit not null,
 DateCreated date not null
);