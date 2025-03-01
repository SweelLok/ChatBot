CREATE TABLE IF NOT EXISTS users (
      user_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
      username TEXT NOT NULL UNIQUE,
      password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS history (
      history_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
      user_id INTEGER NOT NULL,
      name TEXT NOT NULL,
      answer TEXT NOT NULL,
      FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS profile (
      profile_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
      user_id INTEGER NOT NULL UNIQUE,
      photo TEXT,
      description TEXT,
      FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
);