-- CREATE database capstone_lilly;
-- USE capstone_lilly;

CREATE TABLE user(
	id INT PRIMARY KEY auto_increment,
	username VARCHAR(50) UNIQUE KEY not null,
	email VARCHAR(50) UNIQUE KEY not null,
	password VARCHAR(120) not null
);

INSERT INTO user VALUES(1,'abc','abc@mail.com','$2b$12$Ej8nR7HRRFJKoWempY9URu70qFFE5DBFpU9kn.vYnvUVbJlzXaIHu');

CREATE TABLE book(
	id INT PRIMARY KEY auto_increment,
	title VARCHAR(50) not null,
	author VARCHAR(50) not null
);

INSERT INTO book VALUES(2,'The Silent Patient','Alex Michaelides');

-- SELECT id FROM User ORDER BY id DESC LIMIT 1;
-- select * from user;
-- truncate table user;

CREATE TABLE Borrow (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    book_id INT NOT NULL UNIQUE,
    borrow_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    return_date DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP + INTERVAL 14 DAY),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (book_id) REFERENCES book(id)
);
INSERT INTO Borrow(user_id,book_id,borrow_date,return_date) VALUES(1,2,current_timestamp(),current_timestamp()+interval 14 day);

select * from book;

-- drop table borrow;
-- drop table book;
-- drop table user;

-- SELECT user.username,book.title,book.author,borrow.borrow_date,borrow.return_date
--         FROM borrow left join user on borrow.user_id=user.id 
--         left join book on borrow.book_id=book.id

