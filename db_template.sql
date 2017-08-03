DROP TABLE IF EXISTS images;

CREATE TABLE images (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  PostUrl TEXT,
  ImageUrl TEXT,
  Filename TEXT,
  Domain TEXT,
  PostTitle TEXT,
  CommentSectionUrl TEXT,
  PostedOn TEXT,
  LastHtmlStatusCode INTEGER,
  Downloaded INTEGER,
  DownloadDate TEXT
);
