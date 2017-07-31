DROP IF EXISTS images;

CREATE TABLE images (
  id INT PRIMARY KEY AUTOINCREMENT,
  PostUrl TEXT,
  ImageUrl TEXT,
  Filename TEXT,
  Domain TEXT,
  PostTitle TEXT,
  CommentSectionUrl TEXT,
  PostedOn TEXT,
  LastHtmlStatusCode INT,
  Downloaded INT,
  DownloadDate TEXT
);
