#PC Builder API

##Requirements

-User and authentication
-Parts management
-PC Build management

==========================================

###User and authentication
[x] Create model user 0.5h
[x] Register, login user 1h
[x] Authorization for user and admin 1h


###Parts management
[x] Create model parts 0.5h
[x] API filter those parts by type or by name 0.5h
[x] API get the list of all the part is in the system 0.5h

#admin only:
[x] API create edit delete parts in the system 0.5h

###PC Build management
[x] Create model PC BUILD 2h
[x] API create a new PC 2h
[x] API view list of the PC that user created 1h
[x] API filter by name 0.5h
[] API edit their builds 2h
[x] API delete their builds 0.5h
[x] Do not allow the admin to delete a part if that part is used inside any PC builds. 1h
[x] Automatically update the price of the related PC builds where this part is used. 2h
[] A component type can only take 1 corresponding part to go with it, but the quantity of that part can be more than 1. 4h

buffer: 4h

total : 23h