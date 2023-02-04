DOES_EXIST_USER = "select UserTelegramID from UserAccount where UserTelegramID = '{user_telegram_id}' limit 1"
REGISTER_USER = "insert into UserAccount (UserTelegramID) values ('{user_telegram_id}')"

DOES_EXIST_CATEGORY = '''
    select 
        CategoryID
    from Category c
    join UserAccount ua on ua.UserTelegramID = c.UserTelegramID
        and ua.UserTelegramID = '{user_telegram_id}'
        and c.CategoryName like '{category_name}'
    limit 1
    '''

ADD_CATEGORY = '''
    insert into 
        Category (UserTelegramID, CategoryName)
    values (
        '{user_telegram_id}',
        '{category_name}'
        )
    '''

DELETE_CATEGORY = '''
    delete from
        Category
    where CategoryName like '{category_name}'
        and UserTelegramID = '{user_telegram_id}'
    '''

GET_ALL_CATEGORIES = '''
    select 
        CategoryID,
        CategoryName
    from Category 
    where UserTelegramID = '{user_telegram_id}'
    '''

ADD_OPERATION = '''
    insert into UserOperation (
        UserTelegramID,
        CategoryID,
        Description,
        Amount,
        IsEnrollment,
        DateCreated
    )
    values (
        '{user_telegram_id}',
        (select CategoryID from Category where CategoryName like '{category_name}' limit 1),
        '{description}',
        '{amount}',
        '{is_enrollment}',
        date('now')
    )
    '''
